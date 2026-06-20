from __future__ import annotations

import tkinter as tk

from ui import styles
from ui.screens.base import BaseScreen
from ui.widgets import create_button


class ReceiptScreen(BaseScreen):
    """영수증 출력 여부 선택 화면."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self._title_label: tk.Label | None = None
        self._no_btn: tk.Button | None = None
        self._yes_btn: tk.Button | None = None
        self._build()

    def _build(self) -> None:
        center = tk.Frame(self, bg=styles.BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text="🧾",
            font=("Apple Color Emoji", 72),
            bg=styles.BG,
        ).pack(pady=(0, 20))

        self._title_label = tk.Label(
            center,
            text="",
            font=styles.FONT_TITLE,
            fg=styles.PRIMARY_DARK,
            bg=styles.BG,
        )
        self._title_label.pack(pady=(0, 40))

        btn_row = tk.Frame(center, bg=styles.BG)
        btn_row.pack()

        self._no_btn = create_button(
            btn_row,
            text="",
            style="ghost",
            command=lambda: self._choose(False),
            padx=40,
            pady=18,
        )
        self._no_btn.pack(side="left", padx=12)

        self._yes_btn = create_button(
            btn_row,
            text="",
            style="primary",
            command=lambda: self._choose(True),
            padx=40,
            pady=18,
        )
        self._yes_btn.pack(side="left", padx=12)

    def on_show(self) -> None:
        self._refresh_texts()

    def _refresh_texts(self) -> None:
        if self._title_label:
            self._title_label.configure(text=self.app.t("receipt_ask"))
        if self._no_btn:
            self._no_btn.configure(text=self.app.t("receipt_no"))
        if self._yes_btn:
            self._yes_btn.configure(text=self.app.t("receipt_yes"))

    def _choose(self, wants_receipt: bool) -> None:
        self.app.set_receipt_wanted(wants_receipt)
        self.app.reset_to_welcome()
