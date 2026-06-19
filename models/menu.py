from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from models.options import OptionGroup, get_item_option_groups, load_option_groups


@dataclass(frozen=True)
class MenuItem:
    id: str
    name: str
    name_en: str
    price: int
    description: str
    description_en: str
    category_id: str
    category_name: str
    option_ids: tuple[str, ...]

    @property
    def has_options(self) -> bool:
        return len(self.option_ids) > 0

    def localized_name(self, language: str) -> str:
        if language == "en":
            return self.name_en
        return self.name

    def localized_description(self, language: str) -> str:
        if language == "en":
            return self.description_en
        return self.description

    def get_option_groups(self, all_groups: dict[str, OptionGroup]) -> list[OptionGroup]:
        return get_item_option_groups(list(self.option_ids), all_groups)


def load_menu(path: Path | None = None) -> list[MenuItem]:
    if path is None:
        path = Path(__file__).resolve().parent.parent / "data" / "menu.json"

    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    items: list[MenuItem] = []
    for category in data["categories"]:
        for item in category["items"]:
            items.append(
                MenuItem(
                    id=item["id"],
                    name=item["name"],
                    name_en=item.get("name_en", item["name"]),
                    price=item["price"],
                    description=item["description"],
                    description_en=item.get("description_en", item["description"]),
                    category_id=category["id"],
                    category_name=category["name"],
                    option_ids=tuple(item.get("options", [])),
                )
            )
    return items


def get_categories(items: list[MenuItem]) -> list[tuple[str, str]]:
    seen: dict[str, str] = {}
    for item in items:
        seen[item.category_id] = item.category_name
    return list(seen.items())


def get_menu_loader() -> tuple[list[MenuItem], dict[str, OptionGroup]]:
    return load_menu(), load_option_groups()
