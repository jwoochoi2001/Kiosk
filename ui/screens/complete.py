from __future__ import annotations

import tkinter as tk

from ui import styles
from ui.screens.base import BaseScreen


class CompleteScreen(BaseScreen):
    """결제 완료 화면 (영수증 선택 전)."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self._done_label: tk.Label | None = None
        self._order_number_label: tk.Label | None = None
        self._summary_label: tk.Label | None = None
        self._timer_id: str | None = None
        self._build()

    def _build(self) -> None:
        center = tk.Frame(self, bg=styles.BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text="✓",
            font=("Apple SD Gothic Neo", 72, "bold"),
            fg=styles.SUCCESS,
            bg=styles.BG,
        ).pack(pady=(0, 10))

        self._done_label = tk.Label(
            center,
            text="",
            font=styles.FONT_TITLE,
            fg=styles.PRIMARY_DARK,
            bg=styles.BG,
        )
        self._done_label.pack()

        self._order_number_label = tk.Label(
            center,
            text="",
            font=styles.FONT_HEADING,
            fg=styles.TEXT,
            bg=styles.BG,
        )
        self._order_number_label.pack(pady=(20, 10))

        self._summary_label = tk.Label(
            center,
            text="",
            font=styles.FONT_BODY,
            fg=styles.TEXT_LIGHT,
            bg=styles.BG,
        )
        self._summary_label.pack(pady=(0, 20))

    def on_show(self) -> None:
        if self._done_label:
            self._done_label.configure(text=self.app.t("payment_done"))

        order = self.app.last_order
        if order and self._order_number_label and self._summary_label:
            self._order_number_label.configure(text=self.app.t("order_number", number=order["number"]))
            parts = [
                self.app.t("paid_with", method=order["payment_method"]),
                self.app.t("won", amount=f"{order['total']:,}"),
            ]
            if order.get("order_type"):
                parts.insert(0, order["order_type"])
            self._summary_label.configure(text="  ·  ".join(parts))

        self._start_timer()

    def on_hide(self) -> None:
        self._cancel_timer()

    def _start_timer(self) -> None:
        self._cancel_timer()
        self._timer_id = self.after(styles.COMPLETE_TO_RECEIPT_SECONDS * 1000, self._go_receipt)

    def _cancel_timer(self) -> None:
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

    def _go_receipt(self) -> None:
        self._timer_id = None
        self.app.show_screen("receipt")
