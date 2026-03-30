"""Case File screen — review all collected clues."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle


class CaseFileScreen(Screen):
    BG = (0.06, 0.08, 0.05, 1)
    GOLD = (0.88, 0.72, 0.28, 1)
    GREEN = (0.40, 0.82, 0.45, 1)

    def on_enter(self):
        self.clear_widgets()
        with self.canvas.before:
            Color(*self.BG)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd, size=self._upd)
        self._build()

    def _upd(self, *_):
        self._bg.pos = self.pos
        self._bg.size = self.size

    def _build(self):
        from game.models.game_state import game_state, CLUES, SUSPECTS, MIN_CLUES_TO_DEDUCE

        root = BoxLayout(orientation="vertical", padding=14, spacing=10)

        # Header
        header = Label(
            text="[b]Case File[/b]",
            markup=True,
            font_size=24,
            color=self.GOLD,
            size_hint=(1, None),
            height=40,
            halign="center",
        )
        header.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(header)

        collected = game_state.collected_clues
        if not collected:
            empty = Label(
                text="[i]No clues collected yet.\nVisit the scenes and examine objects.[/i]",
                markup=True,
                font_size=15,
                color=(0.70, 0.66, 0.52, 1),
                size_hint=(1, 1),
                halign="center",
                valign="middle",
            )
            empty.bind(size=lambda i, v: setattr(i, "text_size", v))
            root.add_widget(empty)
        else:
            # Summary by suspect
            summary_label = Label(
                text=f"[b]{len(collected)} clue(s) collected[/b]  —  "
                     f"{'Ready to deduce!' if game_state.can_deduce() else f'Need {MIN_CLUES_TO_DEDUCE - len(collected)} more to unlock Deduce'}",
                markup=True,
                font_size=13,
                color=(0.70, 0.85, 0.65, 1),
                size_hint=(1, None),
                height=28,
                halign="center",
            )
            summary_label.bind(size=lambda i, v: setattr(i, "text_size", v))
            root.add_widget(summary_label)

            scroll = ScrollView(size_hint=(1, 1))
            inner = BoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                spacing=8,
                padding=[0, 4],
            )
            inner.bind(minimum_height=inner.setter("height"))

            for cid in collected:
                clue = CLUES[cid]
                card = self._make_clue_card(clue, SUSPECTS)
                inner.add_widget(card)

            scroll.add_widget(inner)
            root.add_widget(scroll)

        # Bottom buttons
        btns = BoxLayout(orientation="horizontal", size_hint=(1, None), height=48, spacing=8)

        back_btn = Button(
            text="Back",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.16, 0.11, 0.04, 1),
            color=self.GOLD,
            font_size=15,
        )
        back_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "scene"))

        can_deduce = game_state.can_deduce()
        deduce_btn = Button(
            text="Deduce Now",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.28, 0.12, 0.06, 1) if can_deduce else (0.10, 0.08, 0.05, 1),
            color=(0.95, 0.65, 0.30, 1) if can_deduce else (0.38, 0.34, 0.26, 1),
            font_size=15,
            bold=can_deduce,
        )
        if can_deduce:
            deduce_btn.bind(
                on_release=lambda *_: setattr(self.manager, "current", "deduction")
            )

        btns.add_widget(back_btn)
        btns.add_widget(deduce_btn)
        root.add_widget(btns)

        self.add_widget(root)

    def _make_clue_card(self, clue, suspects):
        card = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=90,
            padding=[10, 6],
            spacing=4,
        )
        with card.canvas.before:
            Color(0.10, 0.14, 0.08, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[6])
        card.bind(
            pos=lambda i, v: i.canvas.before.clear() or self._rebind_card(i),
            size=lambda i, v: i.canvas.before.clear() or self._rebind_card(i),
        )

        title_lbl = Label(
            text=f"[b]{clue['title']}[/b]",
            markup=True,
            font_size=14,
            color=self.GOLD,
            size_hint=(1, None),
            height=22,
            halign="left",
        )
        title_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        desc_lbl = Label(
            text=clue["description"],
            font_size=12,
            color=(0.82, 0.78, 0.65, 1),
            size_hint=(1, None),
            height=36,
            halign="left",
            valign="top",
        )
        desc_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        card.add_widget(title_lbl)
        card.add_widget(desc_lbl)

        if clue["points_to"]:
            suspect_name = next(
                (s["name"] for s in suspects if s["id"] == clue["points_to"]), "Unknown"
            )
            impl_lbl = Label(
                text=f"[color=ffcc44][i]Implicates: {suspect_name}[/i][/color]",
                markup=True,
                font_size=11,
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=18,
                halign="left",
            )
            impl_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))
            card.add_widget(impl_lbl)

        return card

    @staticmethod
    def _rebind_card(card):
        with card.canvas.before:
            Color(0.10, 0.14, 0.08, 1)
            RoundedRectangle(pos=card.pos, size=card.size, radius=[6])
