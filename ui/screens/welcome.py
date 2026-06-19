from __future__ import annotations

import tkinter as tk

from ui import styles
from ui.screens.base import BaseScreen
from ui.widgets import create_button


class WelcomeScreen(BaseScreen):
    """시작 화면 — 주문 시작 버튼으로만 다음 화면으로 이동합니다."""

    def __init__(self, app) -> None:
        super().__init__(app)
        self._subtitle_label: tk.Label | None = None
        self._start_btn: tk.Button | None = None
        self._lang_btn: tk.Button | None = None
        self._build()

    def _build(self) -> None:
        top = tk.Frame(self, bg=styles.BG)
        top.pack(fill="x", padx=20, pady=20)

        self._lang_btn = create_button(
            top,
            text="",
            style="ghost",
            font=styles.FONT_BODY,
            command=self._toggle_language,
            padx=16,
            pady=8,
        )
        self._lang_btn.pack(side="right")

        center = tk.Frame(self, bg=styles.BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text="☕",
            font=("Apple Color Emoji", 80),
            bg=styles.BG,
        ).pack(pady=(0, 20))

        tk.Label(
            center,
            text="Coffee Kiosk",
            font=styles.FONT_TITLE,
            fg=styles.PRIMARY_DARK,
            bg=styles.BG,
        ).pack()

        self._subtitle_label = tk.Label(
            center,
            text="",
            font=styles.FONT_BODY,
            fg=styles.TEXT_LIGHT,
            bg=styles.BG,
        )
        self._subtitle_label.pack(pady=(10, 40))

        self._start_btn = create_button(
            center,
            text="",
            style="primary",
            command=lambda: self.app.show_screen("menu"),
            padx=60,
            pady=20,
        )
        self._start_btn.pack()

    def on_show(self) -> None:
        self._refresh_texts()

    def _toggle_language(self) -> None:
        next_lang = "en" if self.app.language == "ko" else "ko"
        self.app.set_language(next_lang)
        self._refresh_texts()

    def _refresh_texts(self) -> None:
        if self._subtitle_label:
            self._subtitle_label.configure(text=self.app.t("welcome_subtitle"))
        if self._start_btn:
            self._start_btn.configure(text=self.app.t("start_order"))
        if self._lang_btn:
            key = "lang_switch_to_en" if self.app.language == "ko" else "lang_switch_to_ko"
            self._lang_btn.configure(text=self.app.t(key))
