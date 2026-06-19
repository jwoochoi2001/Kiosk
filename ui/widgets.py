from __future__ import annotations

import tkinter as tk
from typing import Literal

from ui import styles

ButtonStyle = Literal["primary", "accent", "success", "ghost", "header"]


def _button_colors(style: ButtonStyle) -> dict[str, str]:
    if style == "primary":
        return {
            "fg": styles.BTN_PRIMARY_FG,
            "bg": styles.BTN_PRIMARY_BG,
            "activebackground": styles.BTN_PRIMARY_ACTIVE,
            "activeforeground": styles.BTN_PRIMARY_FG,
        }
    if style == "accent":
        return {
            "fg": styles.BTN_ACCENT_FG,
            "bg": styles.BTN_ACCENT_BG,
            "activebackground": styles.BTN_ACCENT_ACTIVE,
            "activeforeground": styles.BTN_ACCENT_FG,
        }
    if style == "success":
        return {
            "fg": styles.BTN_SUCCESS_FG,
            "bg": styles.BTN_SUCCESS_BG,
            "activebackground": styles.BTN_SUCCESS_ACTIVE,
            "activeforeground": styles.BTN_SUCCESS_FG,
        }
    if style == "header":
        return {
            "fg": styles.HEADER_TEXT,
            "bg": styles.HEADER_BG,
            "activebackground": styles.BG,
            "activeforeground": styles.HEADER_TEXT,
        }
    return {
        "fg": styles.BTN_GHOST_FG,
        "bg": styles.BTN_GHOST_BG,
        "activebackground": styles.BORDER,
        "activeforeground": styles.BTN_GHOST_FG,
    }


def create_button(
    parent: tk.Misc,
    text: str,
    command,
    style: ButtonStyle = "primary",
    font=styles.FONT_BUTTON,
    **kwargs,
) -> tk.Button:
    colors = _button_colors(style)
    return tk.Button(
        parent,
        text=text,
        font=font,
        relief="flat",
        cursor="hand2",
        command=command,
        **colors,
        **kwargs,
    )
