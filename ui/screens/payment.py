from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from ui import styles
from ui.screens.base import BaseScreen
from ui.widgets import create_button


class PaymentScreen(BaseScreen):
    """결제 수단 선택 화면."""

    PAYMENT_METHODS = [
        ("card", "pay_card", "method_card"),
        ("cash", "pay_cash", "method_cash"),
        ("mobile", "pay_mobile", "method_mobile"),
    ]

    def __init__(self, app) -> None:
        super().__init__(app)
        self._selected_method = tk.StringVar(value="card")
        self._order_summary_frame: tk.Frame | None = None
        self._back_btn: tk.Button | None = None
        self._header_label: tk.Label | None = None
        self._summary_title: tk.Label | None = None
        self._method_title: tk.Label | None = None
        self._total_label: tk.Label | None = None
        self._pay_btn: tk.Button | None = None
        self._total_heading: tk.Label | None = None
        self._method_radios: list[tk.Radiobutton] = []
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
            command=lambda: self.app.show_screen("order_confirm"),
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

        body = tk.Frame(self, bg=styles.BG)
        body.pack(fill="both", expand=True, padx=40, pady=30)

        left = tk.Frame(body, bg=styles.PANEL, highlightbackground=styles.BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        self._summary_title = tk.Label(
            left,
            text="",
            font=styles.FONT_HEADING,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        )
        self._summary_title.pack(anchor="w", padx=25, pady=(25, 10))

        self._order_summary_frame = tk.Frame(left, bg=styles.PANEL)
        self._order_summary_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        right = tk.Frame(body, bg=styles.PANEL, width=380, highlightbackground=styles.BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._method_title = tk.Label(
            right,
            text="",
            font=styles.FONT_HEADING,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        )
        self._method_title.pack(anchor="w", padx=25, pady=(25, 20))

        for value, label_key, _method_key in self.PAYMENT_METHODS:
            radio = tk.Radiobutton(
                right,
                text="",
                variable=self._selected_method,
                value=value,
                font=styles.FONT_BODY,
                fg=styles.TEXT,
                bg=styles.PANEL,
                activebackground=styles.PANEL,
                selectcolor=styles.BG,
                cursor="hand2",
                padx=25,
                pady=8,
            )
            radio.pack(anchor="w", fill="x")
            self._method_radios.append(radio)

        self._total_label = tk.Label(
            right,
            text="",
            font=styles.FONT_PRICE,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        )
        self._total_label.pack(pady=(30, 20))

        self._pay_btn = create_button(
            right,
            text="",
            style="success",
            command=self._complete_payment,
            padx=30,
            pady=18,
        )
        self._pay_btn.pack(fill="x", padx=25, pady=(0, 25))

    def on_show(self) -> None:
        self._refresh_texts()
        self._render_summary()

    def _refresh_texts(self) -> None:
        if self._back_btn:
            self._back_btn.configure(text=self.app.t("back"))
        if self._header_label:
            self._header_label.configure(text=self.app.t("payment"))
        if self._summary_title:
            self._summary_title.configure(text=self.app.t("order_summary"))
        if self._method_title:
            self._method_title.configure(text=self.app.t("payment_method"))
        if self._pay_btn:
            self._pay_btn.configure(text=self.app.t("pay"))

        for radio, (value, label_key, _method_key) in zip(self._method_radios, self.PAYMENT_METHODS):
            radio.configure(text=self.app.t(label_key))

    def _render_summary(self) -> None:
        if self._order_summary_frame is None:
            return

        for widget in self._order_summary_frame.winfo_children():
            widget.destroy()

        for cart_item in self.app.cart.items.values():
            block = tk.Frame(self._order_summary_frame, bg=styles.PANEL)
            block.pack(fill="x", pady=6)

            top = tk.Frame(block, bg=styles.PANEL)
            top.pack(fill="x")

            tk.Label(
                top,
                text=f"{cart_item.menu_item.localized_name(self.app.language)} × {cart_item.quantity}",
                font=styles.FONT_BODY,
                fg=styles.TEXT,
                bg=styles.PANEL,
            ).pack(side="left")

            tk.Label(
                top,
                text=self.app.t("won", amount=f"{cart_item.subtotal:,}"),
                font=styles.FONT_BODY,
                fg=styles.TEXT_LIGHT,
                bg=styles.PANEL,
            ).pack(side="right")

            if cart_item.option_summary:
                tk.Label(
                    block,
                    text=cart_item.option_summary_for(self.app.language),
                    font=styles.FONT_SMALL,
                    fg=styles.TEXT_LIGHT,
                    bg=styles.PANEL,
                    anchor="w",
                ).pack(fill="x")

        order_type = self.app.order_type
        if order_type:
            tk.Frame(self._order_summary_frame, bg=styles.BORDER, height=1).pack(fill="x", pady=12)
            tk.Label(
                self._order_summary_frame,
                text=self.app.t("order_type_line", type=self.app.order_type_label(order_type)),
                font=styles.FONT_BODY,
                fg=styles.PRIMARY_DARK,
                bg=styles.PANEL,
                anchor="w",
            ).pack(fill="x")

        tk.Frame(self._order_summary_frame, bg=styles.BORDER, height=1).pack(fill="x", pady=15)

        total_row = tk.Frame(self._order_summary_frame, bg=styles.PANEL)
        total_row.pack(fill="x")

        tk.Label(
            total_row,
            text=self.app.t("total_payment"),
            font=styles.FONT_HEADING,
            fg=styles.TEXT,
            bg=styles.PANEL,
        ).pack(side="left")

        tk.Label(
            total_row,
            text=self.app.t("won", amount=f"{self.app.cart.total:,}"),
            font=styles.FONT_PRICE,
            fg=styles.PRIMARY_DARK,
            bg=styles.PANEL,
        ).pack(side="right")

        self._total_label.configure(
            text=self.app.t("payment_amount", amount=f"{self.app.cart.total:,}")
        )

    def _complete_payment(self) -> None:
        method_map = {value: method_key for value, _label, method_key in self.PAYMENT_METHODS}
        method = self.app.t(method_map[self._selected_method.get()])
        order_type_label = self.app.order_type_label(self.app.order_type) if self.app.order_type else ""

        if not messagebox.askyesno(
            self.app.t("payment_confirm_title"),
            self.app.t(
                "payment_confirm_msg",
                order_type=order_type_label,
                method=method,
                amount=f"{self.app.cart.total:,}",
            ),
        ):
            return

        self.app.place_order(payment_method=method)
        self.app.show_screen("receipt")
