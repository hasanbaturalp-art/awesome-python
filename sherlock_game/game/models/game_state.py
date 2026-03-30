"""Central game state shared across all screens."""

import random


SUSPECTS = [
    {
        "id": "moran",
        "name": "Colonel Moran",
        "description": "A former army sharpshooter with a volatile temper.",
        "motive": "Owed gambling debts to Lord Blackwood.",
    },
    {
        "id": "adler",
        "name": "Irene Adler",
        "description": "A cunning opera singer known for her sharp wit.",
        "motive": "The ruby once belonged to her family.",
    },
    {
        "id": "moriarty",
        "name": "Prof. Moriarty",
        "description": "The Napoleon of Crime. Calculating and ruthless.",
        "motive": "Commissioned to steal it for a continental collector.",
    },
]

SCENES = {
    "baker_street": {
        "id": "baker_street",
        "name": "221B Baker Street",
        "description": "Holmes's famous lodgings. A letter lies on the mantelpiece.",
        "color": (0.18, 0.12, 0.08, 1),
        "objects": [
            {
                "id": "letter",
                "label": "Letter",
                "pos_hint": (0.15, 0.55),
                "clue_id": "ransom_note",
            },
            {
                "id": "tobacco",
                "label": "Tobacco Pouch",
                "pos_hint": (0.72, 0.45),
                "clue_id": "tobacco_shag",
            },
            {
                "id": "map",
                "label": "City Map",
                "pos_hint": (0.45, 0.65),
                "clue_id": "docks_marked",
            },
        ],
    },
    "museum": {
        "id": "museum",
        "name": "The British Museum",
        "description": "The scene of the crime. A smashed display case remains.",
        "color": (0.08, 0.12, 0.18, 1),
        "objects": [
            {
                "id": "glass",
                "label": "Broken Glass",
                "pos_hint": (0.30, 0.38),
                "clue_id": "military_boot",
            },
            {
                "id": "glove",
                "label": "Torn Glove",
                "pos_hint": (0.65, 0.50),
                "clue_id": "opera_glove",
            },
            {
                "id": "ledger",
                "label": "Visitor Ledger",
                "pos_hint": (0.50, 0.70),
                "clue_id": "moriarty_visit",
            },
        ],
    },
    "docks": {
        "id": "docks",
        "name": "The East End Docks",
        "description": "Fog rolls over the Thames. A suspicious crate stands nearby.",
        "color": (0.06, 0.10, 0.08, 1),
        "objects": [
            {
                "id": "crate",
                "label": "Shipping Crate",
                "pos_hint": (0.20, 0.42),
                "clue_id": "monogram_crate",
            },
            {
                "id": "cigarette",
                "label": "Cigarette Stub",
                "pos_hint": (0.60, 0.38),
                "clue_id": "army_cigarette",
            },
            {
                "id": "note",
                "label": "Crumpled Note",
                "pos_hint": (0.80, 0.55),
                "clue_id": "payment_note",
            },
        ],
    },
}

CLUES = {
    "ransom_note": {
        "id": "ransom_note",
        "title": "Ransom Note",
        "description": (
            "A typewritten note demanding silence about the ruby. "
            "The paper bears a faint scent of gunpowder."
        ),
        "points_to": "moran",
        "icon": "note",
    },
    "tobacco_shag": {
        "id": "tobacco_shag",
        "title": "Tobacco Pouch",
        "description": (
            "An empty pouch of Arcadia mixture — a brand favoured "
            "by military men and sold near the barracks."
        ),
        "points_to": "moran",
        "icon": "bag",
    },
    "docks_marked": {
        "id": "docks_marked",
        "title": "Marked City Map",
        "description": (
            "A map of London with the East End Docks circled in red ink "
            "and the date of the theft written beside it."
        ),
        "points_to": None,
        "icon": "map",
    },
    "military_boot": {
        "id": "military_boot",
        "title": "Boot Print Cast",
        "description": (
            "A plaster cast of a hobnailed military boot print found "
            "in the dust beside the broken display case."
        ),
        "points_to": "moran",
        "icon": "boot",
    },
    "opera_glove": {
        "id": "opera_glove",
        "title": "Torn Opera Glove",
        "description": (
            "A fine white glove, torn at the thumb. The embroidery "
            "matches the style of Parisian fashion houses."
        ),
        "points_to": "adler",
        "icon": "glove",
    },
    "moriarty_visit": {
        "id": "moriarty_visit",
        "title": "Visitor Ledger Entry",
        "description": (
            "An entry in the museum ledger — 'J. Moriarty, Professor of "
            "Mathematics' — signed the day before the theft."
        ),
        "points_to": "moriarty",
        "icon": "book",
    },
    "monogram_crate": {
        "id": "monogram_crate",
        "title": "Monogrammed Crate",
        "description": (
            "A shipping crate stencilled with the initials 'S.M.' — "
            "Sebastian Moran — addressed to a Viennese collector."
        ),
        "points_to": "moran",
        "icon": "box",
    },
    "army_cigarette": {
        "id": "army_cigarette",
        "title": "Army Cigarette Stub",
        "description": (
            "A half-smoked Army & Navy club cigarette. Only officers "
            "of the 1st Bangalore Pioneers carry this brand."
        ),
        "points_to": "moran",
        "icon": "cigarette",
    },
    "payment_note": {
        "id": "payment_note",
        "title": "Payment Demand",
        "description": (
            "A crumpled note reading: 'Deliver the stone or your debts "
            "go public — M.' Written in a disguised hand."
        ),
        "points_to": "moriarty",
        "icon": "note",
    },
}

# The true culprit for this playthrough
CULPRIT_ID = "moran"
# Minimum clues needed before the deduction screen unlocks
MIN_CLUES_TO_DEDUCE = 4


class GameState:
    """Singleton-style game state accessible from all screens."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.collected_clues: list[str] = []
        self.visited_scenes: set[str] = set()
        self.current_scene_id: str = "baker_street"
        self.case_solved: bool = False
        self.accusation: str | None = None
        self.correct: bool = False

    def collect_clue(self, clue_id: str) -> bool:
        """Return True if this is a new clue."""
        if clue_id not in self.collected_clues:
            self.collected_clues.append(clue_id)
            return True
        return False

    def has_clue(self, clue_id: str) -> bool:
        return clue_id in self.collected_clues

    def can_deduce(self) -> bool:
        return len(self.collected_clues) >= MIN_CLUES_TO_DEDUCE

    def make_accusation(self, suspect_id: str):
        self.accusation = suspect_id
        self.correct = suspect_id == CULPRIT_ID
        self.case_solved = True

    def clues_pointing_to(self, suspect_id: str) -> list[dict]:
        return [
            CLUES[cid]
            for cid in self.collected_clues
            if CLUES[cid]["points_to"] == suspect_id
        ]


# Global singleton
game_state = GameState()
