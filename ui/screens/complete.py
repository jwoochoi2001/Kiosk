from __future__ import annotations

import tkinter as tk

from ui import styles
from ui.screens.base import BaseScreen
from ui.widgets import create_button


class CompleteScreen(BaseScreen):
    """결제 완료 화면."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self._done_label: tk.Label | None = None
        self._order_number_label: tk.Label | None = None
        self._summary_label: tk.Label | None = None
        self._countdown_label: tk.Label | None = None
        self._home_btn: tk.Button | None = None
        self._remaining_seconds = styles.COMPLETE_AUTO_HOME_SECONDS
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

        self._countdown_label = tk.Label(
            center,
            text="",
            font=styles.FONT_BODY,
            fg=styles.TEXT,
            bg=styles.BG,
        )
        self._countdown_label.pack(pady=(0, 30))

        self._home_btn = create_button(
            center,
            text="",
            style="primary",
            command=self._go_home,
            padx=50,
            pady=18,
        )
        self._home_btn.pack()

    def on_show(self) -> None:
        self._refresh_texts()
        order = self.app.last_order
        if order and self._order_number_label and self._summary_label:
            self._order_number_label.configure(text=self.app.t("order_number", number=order["number"]))
            parts = [
                self.app.t("paid_with", method=order["payment_method"]),
                self.app.t("won", amount=f"{order['total']:,}"),
            ]
            if order.get("order_type"):
                parts.insert(0, order["order_type"])
            if order.get("receipt"):
                parts.append(self.app.t("receipt_printed"))
            self._summary_label.configure(text="  ·  ".join(parts))

        self._remaining_seconds = styles.COMPLETE_AUTO_HOME_SECONDS
        self._update_countdown()
        self._start_timer()

    def _refresh_texts(self) -> None:
        if self._done_label:
            self._done_label.configure(text=self.app.t("payment_done"))
        if self._home_btn:
            self._home_btn.configure(text=self.app.t("go_home"))

    def on_hide(self) -> None:
        self._cancel_timer()

    def _start_timer(self) -> None:
        self._cancel_timer()
        self._timer_id = self.after(1000, self._tick)

    def _tick(self) -> None:
        self._remaining_seconds -= 1
        if self._remaining_seconds <= 0:
            self._go_home()
            return
        self._update_countdown()
        self._timer_id = self.after(1000, self._tick)

    def _update_countdown(self) -> None:
        if self._countdown_label:
            self._countdown_label.configure(
                text=self.app.t("auto_home", seconds=self._remaining_seconds)
            )

    def _cancel_timer(self) -> None:
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

    def _go_home(self) -> None:
        self.app.reset_to_welcome()
