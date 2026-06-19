from __future__ import annotations

import tkinter as tk
from typing import Callable

from models.menu import MenuItem
from models.options import OptionGroup, calc_extra_price, default_selection, normalize_selection
from ui import styles
from ui.widgets import create_button


class OptionDialog(tk.Toplevel):
    """메뉴 옵션 선택 팝업."""

    def __init__(
        self,
        parent: tk.Widget,
        app,
        menu_item: MenuItem,
        option_groups: list[OptionGroup],
        on_confirm: Callable[[dict[str, str]], None],
        initial_selection: dict[str, str] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(parent)
        self.app = app
        self.menu_item = menu_item
        self.option_groups = option_groups
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.selected = normalize_selection(option_groups, initial_selection or default_selection(option_groups))

        self._vars: dict[str, tk.StringVar] = {}
        self._group_frames: dict[str, tk.Frame] = {}
        self._price_label: tk.Label | None = None
        self._options_frame: tk.Frame | None = None
        self._options_canvas: tk.Canvas | None = None

        self.title(menu_item.localized_name(self.app.language))
        self.configure(bg=styles.BG)
        self.geometry("520x680")
        self.minsize(520, 480)
        self.resizable(False, False)
        self.transient(parent.winfo_toplevel())
        self.grab_set()

        self._build()
        self._refresh_groups()
        self._center_on_parent(parent)
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _center_on_parent(self, parent: tk.Widget) -> None:
        self.update_idletasks()
        parent_widget = parent.winfo_toplevel()
        px = parent_widget.winfo_x()
        py = parent_widget.winfo_y()
        pw = parent_widget.winfo_width()
        ph = parent_widget.winfo_height()
        w = self.winfo_width()
        h = self.winfo_height()
        x = px + max(0, (pw - w) // 2)
        y = py + max(0, (ph - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _cancel(self) -> None:
        if self.on_cancel:
            self.on_cancel()
        self.destroy()

    def _build(self) -> None:
        header = tk.Frame(self, bg=styles.HEADER_BG, highlightbackground=styles.BORDER, highlightthickness=1)
        header.pack(fill="x", side="top")

        tk.Label(
            header,
            text=self.menu_item.localized_name(self.app.language),
            font=styles.FONT_HEADING,
            fg=styles.HEADER_TEXT,
            bg=styles.HEADER_BG,
        ).pack(anchor="w", padx=25, pady=(20, 5))

        tk.Label(
            header,
            text=self.menu_item.localized_description(self.app.language),
            font=styles.FONT_SMALL,
            fg=styles.HEADER_TEXT_MUTED,
            bg=styles.HEADER_BG,
        ).pack(anchor="w", padx=25, pady=(0, 20))

        footer = tk.Frame(self, bg=styles.PANEL)
        footer.pack(fill="x", side="bottom")

        self._price_label = tk.Label(
            footer,
            text="",
            font=styles.FONT_PRICE,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        )
        self._price_label.pack(pady=(20, 10))

        btn_row = tk.Frame(footer, bg=styles.PANEL)
        btn_row.pack(fill="x", padx=25, pady=(0, 25))

        tk.Button(
            btn_row,
            text=self.app.t("cancel"),
            font=styles.FONT_BODY,
            fg=styles.TEXT,
            bg=styles.BG,
            relief="flat",
            padx=20,
            pady=14,
            cursor="hand2",
            command=self._cancel,
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        create_button(
            btn_row,
            text=self.app.t("add"),
            style="primary",
            command=self._confirm,
            padx=20,
            pady=14,
        ).pack(side="right", fill="x", expand=True, padx=(8, 0))

        scroll_wrap = tk.Frame(self, bg=styles.BG)
        scroll_wrap.pack(fill="both", expand=True, side="top")

        self._options_canvas = tk.Canvas(scroll_wrap, bg=styles.BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_wrap, orient="vertical", command=self._options_canvas.yview)
        self._options_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._options_canvas.pack(side="left", fill="both", expand=True)

        self._options_frame = tk.Frame(self._options_canvas, bg=styles.BG)
        self._canvas_window = self._options_canvas.create_window(
            (0, 0), window=self._options_frame, anchor="nw"
        )
        self._options_frame.bind("<Configure>", self._on_options_configure)
        self._options_canvas.bind("<Configure>", self._on_canvas_configure)
        self._options_canvas.bind("<MouseWheel>", self._on_mousewheel)

        for group in self.option_groups:
            frame = tk.Frame(self._options_frame, bg=styles.BG)
            frame.pack(fill="x", pady=(0, 18), padx=25)
            self._group_frames[group.id] = frame

            tk.Label(
                frame,
                text=group.localized_name(self.app.language),
                font=styles.FONT_BODY,
                fg=styles.TEXT,
                bg=styles.BG,
            ).pack(anchor="w", pady=(0, 8))

            choices_frame = tk.Frame(frame, bg=styles.BG)
            choices_frame.pack(fill="x")

            var = tk.StringVar(value=self.selected.get(group.id, group.default_choice_id()))
            self._vars[group.id] = var

            for choice in group.choices:
                price_text = self.app.t("extra_price", price=choice.extra_price) if choice.extra_price else ""
                tk.Radiobutton(
                    choices_frame,
                    text=f"{choice.localized_name(self.app.language)}{price_text}",
                    variable=var,
                    value=choice.id,
                    font=styles.FONT_BODY,
                    fg=styles.TEXT,
                    bg=styles.BG,
                    activebackground=styles.BG,
                    selectcolor=styles.PANEL,
                    cursor="hand2",
                    command=self._on_option_changed,
                ).pack(anchor="w", pady=3)

        self._update_price()

    def _on_options_configure(self, _event=None) -> None:
        if self._options_canvas:
            self._options_canvas.configure(scrollregion=self._options_canvas.bbox("all"))

    def _on_canvas_configure(self, event) -> None:
        if self._options_canvas:
            self._options_canvas.itemconfigure(self._canvas_window, width=event.width)

    def _on_mousewheel(self, event) -> None:
        if self._options_canvas:
            self._options_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_option_changed(self) -> None:
        for group_id, var in self._vars.items():
            self.selected[group_id] = var.get()
        self._refresh_groups()
        self._update_price()

    def _refresh_groups(self) -> None:
        for group in self.option_groups:
            frame = self._group_frames.get(group.id)
            if frame is None:
                continue
            visible = group.is_visible(self.selected)
            if visible:
                frame.pack(fill="x", pady=(0, 18), padx=25)
            else:
                frame.pack_forget()
                if group.id in self.selected:
                    del self.selected[group.id]

        for group in self.option_groups:
            if group.is_visible(self.selected) and group.id not in self.selected:
                self.selected[group.id] = group.default_choice_id()
                if group.id in self._vars:
                    self._vars[group.id].set(self.selected[group.id])

        self._on_options_configure()

    def _update_price(self) -> None:
        if self._price_label is None:
            return
        extra = calc_extra_price(self.option_groups, self.selected)
        total = self.menu_item.price + extra
        self._price_label.configure(text=self.app.t("won", amount=f"{total:,}"))

    def _confirm(self) -> None:
        final = normalize_selection(self.option_groups, self.selected)
        self.on_confirm(final)
        self.destroy()
