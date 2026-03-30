"""Deduction screen — choose your suspect and make the accusation."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line
from kivy.clock import Clock
import math


class SuspectCard(BoxLayout):
    """Visual card for a suspect with clue count badge."""

    NORMAL_BG = (0.14, 0.10, 0.06, 1)
    SELECTED_BG = (0.30, 0.20, 0.08, 1)
    GOLD = (0.88, 0.72, 0.28, 1)

    def __init__(self, suspect, clue_count, on_select, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=6, **kwargs)
        self._suspect = suspect
        self._clue_count = clue_count
        self._on_select = on_select
        self._selected = False

        with self.canvas.before:
            self._bg_color = Color(*self.NORMAL_BG)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8])
            self._border_color = Color(0.40, 0.30, 0.12, 1)
            self._border_rect = Line(
                rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], 8),
                width=1.5,
            )
        self.bind(pos=self._redraw, size=self._redraw)

        name_lbl = Label(
            text=f"[b]{suspect['name']}[/b]",
            markup=True,
            font_size=15,
            color=self.GOLD,
            size_hint=(1, None),
            height=28,
            halign="center",
        )
        name_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        desc_lbl = Label(
            text=suspect["description"],
            font_size=11,
            color=(0.80, 0.76, 0.62, 1),
            size_hint=(1, None),
            height=36,
            halign="center",
            valign="top",
        )
        desc_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        motive_lbl = Label(
            text=f"[i]Motive: {suspect['motive']}[/i]",
            markup=True,
            font_size=10,
            color=(0.65, 0.60, 0.45, 1),
            size_hint=(1, None),
            height=28,
            halign="center",
            valign="top",
        )
        motive_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        badge_text = f"{clue_count} clue(s) against them" if clue_count else "No clues yet"
        badge_color = "(0.95, 0.65, 0.30, 1)" if clue_count else "(0.50, 0.46, 0.36, 1)"
        badge_lbl = Label(
            text=f"[color={'ffaa44' if clue_count else '7a7060'}]{badge_text}[/color]",
            markup=True,
            font_size=11,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=20,
            halign="center",
        )
        badge_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        accuse_btn = Button(
            text="Accuse",
            size_hint=(0.8, None),
            height=38,
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(0.35, 0.18, 0.06, 1),
            color=(0.95, 0.80, 0.45, 1),
            font_size=13,
            bold=True,
        )
        accuse_btn.bind(on_release=lambda *_: self._on_select(self._suspect["id"]))

        self.add_widget(name_lbl)
        self.add_widget(desc_lbl)
        self.add_widget(motive_lbl)
        self.add_widget(badge_lbl)
        self.add_widget(accuse_btn)

    def _redraw(self, *_):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._border_rect.rounded_rectangle = (
            self.pos[0], self.pos[1], self.size[0], self.size[1], 8
        )


class DeductionScreen(Screen):
    BG = (0.07, 0.05, 0.03, 1)
    GOLD = (0.88, 0.72, 0.28, 1)

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
        from game.models.game_state import game_state, SUSPECTS

        root = BoxLayout(orientation="vertical", padding=14, spacing=10)

        header = Label(
            text="[b]Make Your Deduction[/b]",
            markup=True,
            font_size=22,
            color=self.GOLD,
            size_hint=(1, None),
            height=40,
            halign="center",
        )
        header.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(header)

        warning = Label(
            text="[color=ff6666][b]Warning:[/b] You have one accusation. Choose wisely.[/color]",
            markup=True,
            font_size=13,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=26,
            halign="center",
        )
        warning.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(warning)

        # Clue summary per suspect
        suspects_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 1),
            spacing=8,
        )
        for suspect in SUSPECTS:
            clue_count = len(game_state.clues_pointing_to(suspect["id"]))
            card = SuspectCard(
                suspect=suspect,
                clue_count=clue_count,
                on_select=self._on_accusation,
                size_hint=(1, 1),
            )
            suspects_row.add_widget(card)
        root.add_widget(suspects_row)

        back_btn = Button(
            text="Back to Investigation",
            size_hint=(0.6, None),
            height=44,
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(0.16, 0.11, 0.04, 1),
            color=self.GOLD,
            font_size=14,
        )
        back_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "scene"))
        root.add_widget(back_btn)

        self.add_widget(root)

    def _on_accusation(self, suspect_id):
        from game.models.game_state import game_state, SUSPECTS, CULPRIT_ID
        suspect = next(s for s in SUSPECTS if s["id"] == suspect_id)

        content = BoxLayout(orientation="vertical", padding=16, spacing=10)

        confirm_lbl = Label(
            text=f"Accuse [b]{suspect['name']}[/b] of stealing the ruby?",
            markup=True,
            font_size=16,
            color=(0.92, 0.88, 0.78, 1),
            size_hint=(1, 1),
            halign="center",
            valign="middle",
        )
        confirm_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        btns = BoxLayout(orientation="horizontal", size_hint=(1, None), height=46, spacing=10)

        yes_btn = Button(
            text="Yes — Accuse",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.45, 0.12, 0.06, 1),
            color=(1, 0.80, 0.50, 1),
            font_size=15,
            bold=True,
        )

        no_btn = Button(
            text="Cancel",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.16, 0.11, 0.04, 1),
            color=(0.75, 0.70, 0.55, 1),
            font_size=15,
        )

        btns.add_widget(yes_btn)
        btns.add_widget(no_btn)
        content.add_widget(confirm_lbl)
        content.add_widget(btns)

        popup = Popup(
            title="Final Accusation",
            title_color=self.GOLD,
            content=content,
            size_hint=(0.82, 0.40),
            background="",
            background_color=(0.10, 0.07, 0.03, 0.97),
            separator_color=self.GOLD,
        )
        yes_btn.bind(on_release=lambda *_: self._confirm_accusation(popup, suspect_id))
        no_btn.bind(on_release=popup.dismiss)
        popup.open()

    def _confirm_accusation(self, popup, suspect_id):
        from game.models.game_state import game_state
        popup.dismiss()
        game_state.make_accusation(suspect_id)
        self.manager.current = "verdict"
