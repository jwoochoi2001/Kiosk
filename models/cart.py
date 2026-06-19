from __future__ import annotations

from dataclasses import dataclass, field

from models.menu import MenuItem
from models.options import (
    OptionGroup,
    calc_extra_price,
    format_option_summary,
    normalize_selection,
)


def make_cart_key(menu_item_id: str, selected_options: dict[str, str]) -> str:
    parts = [menu_item_id] + [f"{key}:{value}" for key, value in sorted(selected_options.items())]
    return "|".join(parts)


@dataclass
class CartItem:
    menu_item: MenuItem
    option_groups: list[OptionGroup]
    selected_options: dict[str, str]
    quantity: int = 1
    cart_key: str = ""

    def __post_init__(self) -> None:
        if not self.cart_key:
            self.cart_key = make_cart_key(self.menu_item.id, self.selected_options)

    @property
    def unit_price(self) -> int:
        return self.menu_item.price + calc_extra_price(self.option_groups, self.selected_options)

    @property
    def subtotal(self) -> int:
        return self.unit_price * self.quantity

    def option_summary_for(self, language: str) -> str:
        return format_option_summary(self.option_groups, self.selected_options, language)

    @property
    def option_summary(self) -> str:
        return self.option_summary_for("ko")


@dataclass
class Cart:
    items: dict[str, CartItem] = field(default_factory=dict)

    def add(
        self,
        menu_item: MenuItem,
        option_groups: list[OptionGroup],
        selected_options: dict[str, str] | None = None,
    ) -> None:
        normalized = normalize_selection(option_groups, selected_options or {})
        key = make_cart_key(menu_item.id, normalized)

        if key in self.items:
            self.items[key].quantity += 1
        else:
            self.items[key] = CartItem(
                menu_item=menu_item,
                option_groups=option_groups,
                selected_options=normalized,
                cart_key=key,
            )

    def remove(self, cart_key: str) -> None:
        if cart_key not in self.items:
            return
        self.items[cart_key].quantity -= 1
        if self.items[cart_key].quantity <= 0:
            del self.items[cart_key]

    def clear(self) -> None:
        self.items.clear()

    @property
    def total(self) -> int:
        return sum(item.subtotal for item in self.items.values())

    @property
    def count(self) -> int:
        return sum(item.quantity for item in self.items.values())

    @property
    def is_empty(self) -> bool:
        return len(self.items) == 0
