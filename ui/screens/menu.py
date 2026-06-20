from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from models.menu import MenuItem, get_categories, get_menu_loader
from ui import styles
from ui.i18n import category_key
from ui.dialogs.option_dialog import OptionDialog
from ui.screens.base import BaseScreen
from ui.widgets import create_button


class MenuScreen(BaseScreen):
    """메뉴 선택 및 장바구니 화면."""

    DEFAULT_CATEGORY = "coffee"

    def __init__(self, app) -> None:
        super().__init__(app)
        self.menu_items, self.option_groups_map = get_menu_loader()
        self.categories = get_categories(self.menu_items)
        self.selected_category = self.DEFAULT_CATEGORY if self.categories else ""
        self._category_buttons: dict[str, tk.Button] = {}
        self._category_wrappers: dict[str, tk.Frame] = {}
        self._menu_frame: tk.Frame | None = None
        self._cart_list_frame: tk.Frame | None = None
        self._total_label: tk.Label | None = None
        self._count_label: tk.Label | None = None
        self._idle_timer: str | None = None
        self._home_btn: tk.Button | None = None
        self._title_label: tk.Label | None = None
        self._cart_title: tk.Label | None = None
        self._clear_btn: tk.Button | None = None
        self._pay_btn: tk.Button | None = None
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self, bg=styles.HEADER_BG, height=70, highlightbackground=styles.BORDER, highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)

        self._home_btn = create_button(
            header,
            text="",
            style="header",
            font=styles.FONT_BODY,
            command=self._go_home,
        )
        self._home_btn.pack(side="left", padx=20, pady=15)

        self._title_label = tk.Label(
            header,
            text="",
            font=styles.FONT_HEADING,
            fg=styles.HEADER_TEXT,
            bg=styles.HEADER_BG,
        )
        self._title_label.pack(side="left", padx=10)

        self._count_label = tk.Label(
            header,
            text="장바구니 0개",
            font=styles.FONT_BODY,
            fg=styles.HEADER_TEXT,
            bg=styles.HEADER_BG,
        )
        self._count_label.pack(side="right", padx=30)

        body = tk.Frame(self, bg=styles.BG)
        body.pack(fill="both", expand=True, padx=20, pady=20)

        left = tk.Frame(body, bg=styles.BG)
        left.pack(side="left", fill="both", expand=True)

        category_bar = tk.Frame(left, bg=styles.BG)
        category_bar.pack(fill="x", pady=(0, 15))

        for cat_id, cat_name in self.categories:
            wrapper = tk.Frame(
                category_bar,
                bg=styles.PANEL,
                highlightthickness=2,
                highlightbackground=styles.BORDER,
            )
            wrapper.pack(side="left", padx=(0, 10))
            self._category_wrappers[cat_id] = wrapper

            btn = tk.Button(
                wrapper,
                text=cat_name,
                font=styles.FONT_BUTTON,
                fg=styles.TEXT,
                bg=styles.PANEL,
                activebackground=styles.ACCENT_LIGHT,
                relief="flat",
                bd=0,
                padx=20,
                pady=10,
                cursor="hand2",
                command=lambda cid=cat_id: self._select_category(cid),
            )
            btn.pack(padx=2, pady=2)
            self._category_buttons[cat_id] = btn

        menu_scroll_wrap = tk.Frame(left, bg=styles.BG)
        menu_scroll_wrap.pack(fill="both", expand=True)

        self._menu_canvas = tk.Canvas(menu_scroll_wrap, bg=styles.BG, highlightthickness=0)
        menu_scrollbar = tk.Scrollbar(menu_scroll_wrap, orient="vertical", command=self._menu_canvas.yview)
        self._menu_canvas.configure(yscrollcommand=menu_scrollbar.set)
        menu_scrollbar.pack(side="right", fill="y")
        self._menu_canvas.pack(side="left", fill="both", expand=True)

        self._menu_frame = tk.Frame(self._menu_canvas, bg=styles.BG)
        self._menu_canvas_window = self._menu_canvas.create_window((0, 0), window=self._menu_frame, anchor="nw")
        self._menu_frame.bind("<Configure>", self._on_menu_frame_configure)
        self._menu_canvas.bind("<Configure>", self._on_menu_canvas_configure)
        self._menu_canvas.bind("<MouseWheel>", self._on_menu_mousewheel)
        self.bind("<Button-1>", self._touch_activity, add="+")
        self.bind("<MouseWheel>", self._touch_activity, add="+")

        right = tk.Frame(body, bg=styles.PANEL, width=320, highlightbackground=styles.BORDER, highlightthickness=1)
        right.pack(side="right", fill="y", padx=(20, 0))
        right.pack_propagate(False)

        self._cart_title = tk.Label(
            right,
            text="",
            font=styles.FONT_HEADING,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        )
        self._cart_title.pack(pady=(20, 10))

        cart_scroll = tk.Frame(right, bg=styles.PANEL)
        cart_scroll.pack(fill="both", expand=True, padx=15)

        self._cart_list_frame = tk.Frame(cart_scroll, bg=styles.PANEL)
        self._cart_list_frame.pack(fill="both", expand=True)

        footer = tk.Frame(right, bg=styles.PANEL)
        footer.pack(fill="x", padx=15, pady=15)

        self._total_label = tk.Label(
            footer,
            text="합계  0원",
            font=styles.FONT_PRICE,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        )
        self._total_label.pack(anchor="w", pady=(0, 15))

        btn_row = tk.Frame(footer, bg=styles.PANEL)
        btn_row.pack(fill="x")

        self._clear_btn = create_button(
            btn_row,
            text="",
            style="ghost",
            font=styles.FONT_BODY,
            command=self._clear_cart,
            padx=15,
            pady=12,
        )
        self._clear_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self._pay_btn = create_button(
            btn_row,
            text="",
            style="primary",
            font=styles.FONT_BUTTON,
            command=self._go_payment,
            padx=15,
            pady=12,
        )
        self._pay_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        self._select_category(self.selected_category)

    def reset_to_default_category(self) -> None:
        self.selected_category = self.DEFAULT_CATEGORY

    def on_show(self) -> None:
        self._refresh_texts()
        self._refresh_cart()
        self._start_idle_timer()

    def _refresh_texts(self) -> None:
        if self._home_btn:
            self._home_btn.configure(text=self.app.t("home"))
        if self._title_label:
            self._title_label.configure(text=self.app.t("menu_select"))
        if self._cart_title:
            self._cart_title.configure(text=self.app.t("cart"))
        if self._clear_btn:
            self._clear_btn.configure(text=self.app.t("clear_cart"))
        if self._pay_btn:
            self._pay_btn.configure(text=self.app.t("pay"))
        for cat_id, btn in self._category_buttons.items():
            btn.configure(text=self.app.t(category_key(cat_id)))
        self._select_category(self.selected_category)

    def on_hide(self) -> None:
        self._cancel_idle_timer()

    def _start_idle_timer(self) -> None:
        self._cancel_idle_timer()
        self._idle_timer = self.after(styles.MENU_IDLE_SECONDS * 1000, self._idle_timeout)

    def _cancel_idle_timer(self) -> None:
        if self._idle_timer:
            self.after_cancel(self._idle_timer)
            self._idle_timer = None

    def _touch_activity(self, _event=None) -> None:
        if self.app._current_screen_name == "menu":
            self._start_idle_timer()

    def _idle_timeout(self) -> None:
        self._idle_timer = None
        if self.app._current_screen_name == "menu":
            self.app.reset_to_welcome()

    def _go_home(self) -> None:
        self._touch_activity()
        self.app.reset_to_welcome()

    def _on_menu_frame_configure(self, _event=None) -> None:
        self._menu_canvas.configure(scrollregion=self._menu_canvas.bbox("all"))

    def _on_menu_canvas_configure(self, event) -> None:
        self._menu_canvas.itemconfigure(self._menu_canvas_window, width=event.width)

    def _on_menu_mousewheel(self, event) -> None:
        self._touch_activity()
        if self._menu_canvas.winfo_containing(event.x_root, event.y_root):
            self._menu_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _select_category(self, category_id: str) -> None:
        self._touch_activity()
        self.selected_category = category_id

        for cat_id, btn in self._category_buttons.items():
            wrapper = self._category_wrappers[cat_id]
            if cat_id == category_id:
                wrapper.configure(highlightbackground=styles.PRIMARY_DARK, highlightthickness=3)
                btn.configure(
                    bg=styles.ACCENT_LIGHT,
                    fg=styles.PRIMARY_DARK,
                    font=styles.FONT_BUTTON,
                )
            else:
                wrapper.configure(highlightbackground=styles.BORDER, highlightthickness=1)
                btn.configure(
                    bg=styles.PANEL,
                    fg=styles.TEXT,
                    font=styles.FONT_BODY,
                )

        self._render_menu_items()

    def _render_menu_items(self) -> None:
        if self._menu_frame is None:
            return

        for widget in self._menu_frame.winfo_children():
            widget.destroy()

        filtered = [item for item in self.menu_items if item.category_id == self.selected_category]

        for index, item in enumerate(filtered):
            row, col = divmod(index, 3)
            card = self._create_menu_card(item)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        for col in range(3):
            self._menu_frame.columnconfigure(col, weight=1)

        self._menu_canvas.yview_moveto(0)
        self._on_menu_frame_configure()

    def _create_menu_card(self, item: MenuItem) -> tk.Frame:
        card = tk.Frame(
            self._menu_frame,
            bg=styles.PANEL,
            highlightbackground=styles.BORDER,
            highlightthickness=1,
            cursor="hand2",
        )

        tk.Label(
            card,
            text=item.localized_name(self.app.language),
            font=styles.FONT_HEADING,
            fg=styles.TEXT,
            bg=styles.PANEL,
        ).pack(anchor="w", padx=15, pady=(15, 5))

        tk.Label(
            card,
            text=item.localized_description(self.app.language),
            font=styles.FONT_SMALL,
            fg=styles.TEXT_LIGHT,
            bg=styles.PANEL,
            wraplength=200,
            justify="left",
        ).pack(anchor="w", padx=15)

        bottom = tk.Frame(card, bg=styles.PANEL)
        bottom.pack(fill="x", padx=15, pady=15)

        tk.Label(
            bottom,
            text=self.app.t("price_from", price=item.price),
            font=styles.FONT_PRICE,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        ).pack(side="left")

        select_btn = create_button(
            bottom,
            text=self.app.t("select_options") if item.has_options else self.app.t("add"),
            style="accent",
            font=styles.FONT_BODY,
            command=lambda: self._open_item(item),
            padx=12,
            pady=4,
        )
        select_btn.pack(side="right")

        card.bind("<Button-1>", lambda _: self._open_item(item))
        for child in card.winfo_children():
            if child is not select_btn:
                child.bind("<Button-1>", lambda _: self._open_item(item))

        return card

    def _open_item(self, item: MenuItem) -> None:
        self._touch_activity()
        option_groups = item.get_option_groups(self.option_groups_map)
        if not option_groups:
            self.app.cart.add(item, option_groups, {})
            self._refresh_cart()
            return

        self._cancel_idle_timer()

        def on_confirm(selected: dict[str, str]) -> None:
            self._add_with_options(item, option_groups, selected)
            self._start_idle_timer()

        OptionDialog(
            parent=self,
            app=self.app,
            menu_item=item,
            option_groups=option_groups,
            on_confirm=on_confirm,
            on_cancel=self._start_idle_timer,
        )

    def _add_with_options(self, item: MenuItem, option_groups, selected: dict[str, str]) -> None:
        self.app.cart.add(item, option_groups, selected)
        self._refresh_cart()

    def _add_same_item(self, cart_item) -> None:
        self._touch_activity()
        self.app.cart.add(
            cart_item.menu_item,
            cart_item.option_groups,
            cart_item.selected_options,
        )
        self._refresh_cart()

    def _remove_from_cart(self, cart_key: str) -> None:
        self._touch_activity()
        self.app.cart.remove(cart_key)
        self._refresh_cart()

    def _clear_cart(self) -> None:
        self._touch_activity()
        if self.app.cart.is_empty:
            return
        if messagebox.askyesno(self.app.t("clear_cart_title"), self.app.t("clear_cart_msg")):
            self.app.cart.clear()
            self._refresh_cart()

    def _refresh_cart(self) -> None:
        if self._cart_list_frame is None or self._total_label is None or self._count_label is None:
            return

        for widget in self._cart_list_frame.winfo_children():
            widget.destroy()

        if self.app.cart.is_empty:
            tk.Label(
                self._cart_list_frame,
                text=self.app.t("cart_empty"),
                font=styles.FONT_BODY,
                fg=styles.TEXT_LIGHT,
                bg=styles.PANEL,
            ).pack(pady=40)
        else:
            for cart_item in self.app.cart.items.values():
                self._create_cart_row(cart_item)

        self._total_label.configure(text=self.app.t("total", amount=f"{self.app.cart.total:,}"))
        self._count_label.configure(text=self.app.t("cart_count", count=self.app.cart.count))

    def _create_cart_row(self, cart_item) -> None:
        row = tk.Frame(self._cart_list_frame, bg=styles.PANEL)
        row.pack(fill="x", pady=6)

        info = tk.Frame(row, bg=styles.PANEL)
        info.pack(side="left", fill="x", expand=True)

        tk.Label(
            info,
            text=cart_item.menu_item.localized_name(self.app.language),
            font=styles.FONT_BODY,
            fg=styles.TEXT,
            bg=styles.PANEL,
        ).pack(anchor="w")

        if cart_item.option_summary:
            tk.Label(
                info,
                text=cart_item.option_summary_for(self.app.language),
                font=styles.FONT_SMALL,
                fg=styles.TEXT_LIGHT,
                bg=styles.PANEL,
                wraplength=180,
                justify="left",
            ).pack(anchor="w")

        tk.Label(
            info,
            text=self.app.t("price_line", price=cart_item.unit_price, qty=cart_item.quantity),
            font=styles.FONT_SMALL,
            fg=styles.TEXT_LIGHT,
            bg=styles.PANEL,
        ).pack(anchor="w")

        controls = tk.Frame(row, bg=styles.PANEL)
        controls.pack(side="right")

        create_button(
            controls,
            text="-",
            style="ghost",
            font=styles.FONT_BODY,
            command=lambda: self._remove_from_cart(cart_item.cart_key),
            width=2,
        ).pack(side="left", padx=2)

        tk.Label(
            controls,
            text=str(cart_item.quantity),
            font=styles.FONT_BODY,
            fg=styles.TEXT,
            bg=styles.PANEL,
            width=2,
        ).pack(side="left")

        create_button(
            controls,
            text="+",
            style="accent",
            font=styles.FONT_BODY,
            command=lambda: self._add_same_item(cart_item),
            width=2,
        ).pack(side="left", padx=2)

    def _go_payment(self) -> None:
        self._touch_activity()
        if self.app.cart.is_empty:
            messagebox.showwarning(self.app.t("menu_select"), self.app.t("alert_empty_cart"))
            return
        self.app.show_screen("order_confirm")
