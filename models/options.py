from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OptionChoice:
    id: str
    name: str
    name_en: str
    extra_price: int

    def localized_name(self, language: str) -> str:
        if language == "en":
            return self.name_en
        return self.name


@dataclass(frozen=True)
class OptionGroup:
    id: str
    name: str
    name_en: str
    required: bool
    choices: tuple[OptionChoice, ...]
    visible_when: dict[str, str] | None = None

    def localized_name(self, language: str) -> str:
        if language == "en":
            return self.name_en
        return self.name

    def default_choice_id(self) -> str:
        return self.choices[0].id

    def get_choice(self, choice_id: str) -> OptionChoice | None:
        for choice in self.choices:
            if choice.id == choice_id:
                return choice
        return None

    def is_visible(self, selected: dict[str, str]) -> bool:
        if not self.visible_when:
            return True
        group = self.visible_when.get("group")
        choice = self.visible_when.get("choice")
        return selected.get(group) == choice


def load_option_groups(path: Path | None = None) -> dict[str, OptionGroup]:
    if path is None:
        path = Path(__file__).resolve().parent.parent / "data" / "options.json"

    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    groups: dict[str, OptionGroup] = {}
    for group_id, group in data["groups"].items():
        choices = tuple(
            OptionChoice(
                id=choice["id"],
                name=choice["name"],
                name_en=choice.get("name_en", choice["name"]),
                extra_price=choice.get("extra_price", 0),
            )
            for choice in group["choices"]
        )
        groups[group_id] = OptionGroup(
            id=group_id,
            name=group["name"],
            name_en=group.get("name_en", group["name"]),
            required=group.get("required", True),
            choices=choices,
            visible_when=group.get("visible_when"),
        )
    return groups


def get_item_option_groups(
    option_ids: list[str],
    all_groups: dict[str, OptionGroup],
) -> list[OptionGroup]:
    return [all_groups[option_id] for option_id in option_ids if option_id in all_groups]


def default_selection(groups: list[OptionGroup]) -> dict[str, str]:
    selected: dict[str, str] = {}
    for group in groups:
        if group.is_visible(selected):
            selected[group.id] = group.default_choice_id()
    return selected


def normalize_selection(
    groups: list[OptionGroup],
    selected: dict[str, str],
) -> dict[str, str]:
    normalized = default_selection(groups)
    for group in groups:
        if not group.is_visible(normalized):
            continue
        if group.id in selected and group.get_choice(selected[group.id]):
            normalized[group.id] = selected[group.id]
    return normalized


def format_option_summary(
    groups: list[OptionGroup],
    selected: dict[str, str],
    language: str = "ko",
) -> str:
    parts: list[str] = []
    for group in groups:
        if not group.is_visible(selected):
            continue
        choice = group.get_choice(selected.get(group.id, ""))
        if choice:
            parts.append(choice.localized_name(language))
    return " · ".join(parts)


def calc_extra_price(
    groups: list[OptionGroup],
    selected: dict[str, str],
) -> int:
    total = 0
    for group in groups:
        if not group.is_visible(selected):
            continue
        choice = group.get_choice(selected.get(group.id, ""))
        if choice:
            total += choice.extra_price
    return total
