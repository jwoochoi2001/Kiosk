from __future__ import annotations

import random
import tkinter as tk
from typing import Any

from models.cart import Cart
from ui import styles
from ui.i18n import translate
from ui.order_types import ORDER_TYPES
from ui.screens.receipt import ReceiptScreen
from ui.screens.complete import CompleteScreen
from ui.screens.processing import ProcessingScreen
from ui.screens.menu import MenuScreen
from ui.screens.order_confirm import OrderConfirmScreen
from ui.screens.payment import PaymentScreen
from ui.screens.welcome import WelcomeScreen


class KioskApp(tk.Tk):
    """커피 키오스크 메인 애플리케이션."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Coffee Kiosk")
        self.geometry(f"{styles.WINDOW_WIDTH}x{styles.WINDOW_HEIGHT}")
        self.configure(bg=styles.BG)
        self.resizable(False, False)

        self.cart = Cart()
        self.language = "ko"
        self.order_type: str | None = None
        self.last_order: dict[str, Any] | None = None
        self._screens: dict[str, tk.Frame] = {}
        self._current_screen_name: str | None = None

        self.container = tk.Frame(self, bg=styles.BG)
        self.container.pack(fill="both", expand=True)

        self._register_screens()
        self.show_screen("welcome")

    def _register_screens(self) -> None:
        screen_classes = {
            "welcome": WelcomeScreen,
            "menu": MenuScreen,
            "order_confirm": OrderConfirmScreen,
            "payment": PaymentScreen,
            "processing": ProcessingScreen,
            "complete": CompleteScreen,
            "receipt": ReceiptScreen,
        }
        for name, screen_class in screen_classes.items():
            screen = screen_class(self)
            self._screens[name] = screen
            screen.place(x=0, y=0, relwidth=1, relheight=1)

    def show_screen(self, name: str) -> None:
        if name not in self._screens:
            raise ValueError(f"Unknown screen: {name}")

        if self._current_screen_name:
            current = self._screens[self._current_screen_name]
            current.on_hide()
            current.lower()

        next_screen = self._screens[name]
        next_screen.on_show()
        next_screen.lift()
        self._current_screen_name = name

    def t(self, key: str, **kwargs) -> str:
        return translate(self.language, key, **kwargs)

    def set_language(self, language: str) -> None:
        if language not in ("ko", "en"):
            raise ValueError(f"Unsupported language: {language}")
        self.language = language

    def order_type_label(self, order_type: str) -> str:
        return self.t(ORDER_TYPES[order_type]["label_key"])

    def update_order_type(self, order_type: str) -> None:
        if order_type not in ORDER_TYPES:
            raise ValueError(f"Unknown order type: {order_type}")
        self.order_type = order_type

    def reset_to_welcome(self) -> None:
        self.cart.clear()
        self.order_type = None
        menu_screen = self._screens.get("menu")
        if menu_screen is not None:
            menu_screen.reset_to_default_category()
        self.show_screen("welcome")

    def place_order(self, payment_method: str) -> None:
        order_type_label = self.order_type_label(self.order_type) if self.order_type else ""
        self.last_order = {
            "number": random.randint(100, 999),
            "total": self.cart.total,
            "payment_method": payment_method,
            "order_type": order_type_label,
            "items": [
                {
                    "name": item.menu_item.localized_name(self.language),
                    "options": item.option_summary_for(self.language),
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "subtotal": item.subtotal,
                }
                for item in self.cart.items.values()
            ],
        }

    def set_receipt_wanted(self, wanted: bool) -> None:
        if self.last_order is not None:
            self.last_order["receipt"] = wanted


def run() -> None:
    app = KioskApp()
    app.mainloop()
