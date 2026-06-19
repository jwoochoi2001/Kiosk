from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from ui import styles

if TYPE_CHECKING:
    from ui.app import KioskApp


class BaseScreen(tk.Frame):
    """모든 화면의 기본 클래스."""

    def __init__(self, app: KioskApp, **kwargs) -> None:
        super().__init__(app.container, bg=styles.BG, **kwargs)
        self.app = app

    def on_show(self) -> None:
        """화면이 표시될 때 호출됩니다."""

    def on_hide(self) -> None:
        """화면이 숨겨질 때 호출됩니다."""
