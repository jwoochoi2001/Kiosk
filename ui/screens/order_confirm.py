from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from ui import styles
from ui.i18n import category_key
from ui.order_types import ORDER_TYPES
from ui.screens.base import BaseScreen
from ui.widgets import create_button


class OrderConfirmScreen(BaseScreen):
    """결제 전 매장/포장 재확인 화면."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self._selected: str | None = None
        self._card_frames: dict[str, tk.Frame] = {}
        self._card_labels: dict[str, tuple[tk.Label, tk.Label]] = {}
        self._confirm_btn: tk.Button | None = None
        self._back_btn: tk.Button | None = None
        self._header_label: tk.Label | None = None
        self._title_label: tk.Label | None = None
        self._subtitle_label: tk.Label | None = None
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self, bg=styles.HEADER_BG, height=70, highlightbackground=styles.BORDER, highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)

        self._back_btn = create_button(
            header,
            text="",
            style="header",
            font=styles.FONT_BODY,
            command=lambda: self.app.show_screen("menu"),
        )
        self._back_btn.pack(side="left", padx=20, pady=15)

        self._header_label = tk.Label(
            header,
            text="",
            font=styles.FONT_HEADING,
            fg=styles.HEADER_TEXT,
            bg=styles.HEADER_BG,
        )
        self._header_label.pack(side="left", padx=10)

        center = tk.Frame(self, bg=styles.BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        self._title_label = tk.Label(
            center,
            text="",
            font=styles.FONT_TITLE,
            fg=styles.PRIMARY_DARK,
            bg=styles.BG,
        )
        self._title_label.pack(pady=(0, 10))

        self._subtitle_label = tk.Label(
            center,
            text="",
            font=styles.FONT_BODY,
            fg=styles.TEXT_LIGHT,
            bg=styles.BG,
        )
        self._subtitle_label.pack(pady=(0, 40))

        btn_row = tk.Frame(center, bg=styles.BG)
        btn_row.pack()

        for order_type, info in ORDER_TYPES.items():
            self._create_type_card(btn_row, order_type, info)

        self._confirm_btn = create_button(
            center,
            text="",
            style="primary",
            state="disabled",
            command=self._go_payment,
            padx=60,
            pady=18,
        )
        self._confirm_btn.pack(pady=(40, 0))

    def on_show(self) -> None:
        self._selected = self.app.order_type
        self._refresh_texts()
        self._update_cards()

    def _refresh_texts(self) -> None:
        if self._back_btn:
            self._back_btn.configure(text=self.app.t("back_to_menu"))
        if self._header_label:
            self._header_label.configure(text=self.app.t("order_type_check"))
        if self._title_label:
            self._title_label.configure(text=self.app.t("order_type_title"))
        if self._subtitle_label:
            self._subtitle_label.configure(text=self.app.t("order_type_subtitle"))
        if self._confirm_btn:
            self._confirm_btn.configure(text=self.app.t("pay"))

        for order_type, (label, desc) in self._card_labels.items():
            info = ORDER_TYPES[order_type]
            label.configure(text=self.app.t(info["label_key"]))
            desc.configure(text=self.app.t(info["desc_key"]))

    def _create_type_card(self, parent: tk.Frame, order_type: str, info: dict) -> None:
        card = tk.Frame(
            parent,
            bg=styles.PANEL,
            highlightbackground=styles.BORDER,
            highlightthickness=2,
            width=280,
            height=260,
            cursor="hand2",
        )
        card.pack(side="left", padx=20)
        card.pack_propagate(False)
        self._card_frames[order_type] = card

        tk.Label(
            card,
            text=info["icon"],
            font=("Apple Color Emoji", 56),
            bg=styles.PANEL,
        ).pack(pady=(35, 15))

        label = tk.Label(
            card,
            text="",
            font=styles.FONT_HEADING,
            fg=styles.TEXT,
            bg=styles.PANEL,
        )
        label.pack()

        desc = tk.Label(
            card,
            text="",
            font=styles.FONT_SMALL,
            fg=styles.TEXT_LIGHT,
            bg=styles.PANEL,
        )
        desc.pack(pady=(8, 0))
        self._card_labels[order_type] = (label, desc)

        def select() -> None:
            self._selected = order_type
            self.app.update_order_type(order_type)
            self._update_cards()

        card.bind("<Button-1>", lambda _: select())
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda _: select())

    def _update_cards(self) -> None:
        for order_type, card in self._card_frames.items():
            if order_type == self._selected:
                card.configure(highlightbackground=styles.PRIMARY_DARK, highlightthickness=3)
            else:
                card.configure(highlightbackground=styles.BORDER, highlightthickness=2)

        if self._confirm_btn:
            state = "normal" if self._selected else "disabled"
            self._confirm_btn.configure(state=state)

    def _go_payment(self) -> None:
        if not self._selected:
            return

        choice = self.app.order_type_label(self._selected)
        if not messagebox.askyesno(
            self.app.t("order_confirm_dialog_title"),
            self.app.t("order_confirm_dialog_msg", choice=choice),
        ):
            return

        self.app.show_screen("payment")
