from __future__ import annotations

import tkinter as tk

from ui import styles
from ui.screens.base import BaseScreen


class ProcessingScreen(BaseScreen):
    """결제 진행 중 화면."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self._title_label: tk.Label | None = None
        self._subtitle_label: tk.Label | None = None
        self._timer_id: str | None = None
        self._build()

    def _build(self) -> None:
        center = tk.Frame(self, bg=styles.BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text="💳",
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
        self._title_label.pack()

        self._subtitle_label = tk.Label(
            center,
            text="",
            font=styles.FONT_BODY,
            fg=styles.TEXT_LIGHT,
            bg=styles.BG,
        )
        self._subtitle_label.pack(pady=(16, 0))

    def on_show(self) -> None:
        if self._title_label:
            self._title_label.configure(text=self.app.t("payment_processing"))
        if self._subtitle_label:
            self._subtitle_label.configure(text=self.app.t("payment_processing_sub"))
        self._start_timer()

    def on_hide(self) -> None:
        self._cancel_timer()

    def _start_timer(self) -> None:
        self._cancel_timer()
        self._timer_id = self.after(styles.PROCESSING_SECONDS * 1000, self._go_complete)

    def _cancel_timer(self) -> None:
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

    def _go_complete(self) -> None:
        self._timer_id = None
        self.app.show_screen("complete")
