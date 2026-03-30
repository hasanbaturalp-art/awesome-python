"""Verdict screen — reveal whether the player solved the case."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
import math


class VerdictScreen(Screen):
    BG_WIN = (0.04, 0.10, 0.04, 1)
    BG_LOSE = (0.10, 0.04, 0.03, 1)
    GOLD = (0.88, 0.72, 0.28, 1)

    def on_enter(self):
        self.clear_widgets()
        self.canvas.before.clear()
        self._build()

    def _build(self):
        from game.models.game_state import game_state, SUSPECTS, CLUES, CULPRIT_ID

        correct = game_state.correct
        accused = next(
            (s for s in SUSPECTS if s["id"] == game_state.accusation), None
        )
        culprit = next(s for s in SUSPECTS if s["id"] == CULPRIT_ID)

        bg_color = self.BG_WIN if correct else self.BG_LOSE
        with self.canvas.before:
            Color(*bg_color)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd, size=self._upd)

        root = BoxLayout(orientation="vertical", padding=20, spacing=14)

        # Result banner
        if correct:
            banner_text = "Case Solved!"
            banner_color = (0.45, 0.90, 0.45, 1)
            detail = (
                f"[b]{culprit['name']}[/b] has been apprehended by Scotland Yard.\n\n"
                "Your brilliant deduction has saved Lord Blackwood's ruby "
                "and upheld the honour of Baker Street."
            )
        else:
            banner_text = "The Wrong Man!"
            banner_color = (0.92, 0.35, 0.25, 1)
            who = accused["name"] if accused else "Unknown"
            detail = (
                f"You accused [b]{who}[/b], but they are innocent.\n\n"
                f"The true culprit — [b]{culprit['name']}[/b] — slipped away "
                "into the London fog. The ruby is lost."
            )

        banner = Label(
            text=f"[b]{banner_text}[/b]",
            markup=True,
            font_size=32,
            color=banner_color,
            size_hint=(1, None),
            height=56,
            halign="center",
        )
        banner.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(banner)

        # Separator
        sep = Widget(size_hint=(1, None), height=2)
        with sep.canvas:
            Color(*self.GOLD)
            Rectangle(pos=sep.pos, size=sep.size)
        sep.bind(pos=lambda i, v: i.canvas.clear() or self._draw_sep(i))
        sep.bind(size=lambda i, v: i.canvas.clear() or self._draw_sep(i))
        root.add_widget(sep)

        # Detail
        detail_lbl = Label(
            text=detail,
            markup=True,
            font_size=15,
            color=(0.92, 0.88, 0.78, 1),
            size_hint=(1, 1),
            halign="center",
            valign="middle",
        )
        detail_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(detail_lbl)

        # Culprit profile
        profile_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.85, None),
            height=100,
            pos_hint={"center_x": 0.5},
            padding=10,
            spacing=4,
        )
        with profile_box.canvas.before:
            Color(0.14, 0.10, 0.05, 1)
            self._pb_rect = Rectangle(pos=profile_box.pos, size=profile_box.size)
        profile_box.bind(
            pos=lambda i, v: setattr(self._pb_rect, "pos", v),
            size=lambda i, v: setattr(self._pb_rect, "size", v),
        )

        profile_box.add_widget(Label(
            text=f"[b]{culprit['name']}[/b]  —  The True Culprit",
            markup=True,
            font_size=14,
            color=self.GOLD,
            size_hint=(1, None),
            height=24,
            halign="center",
        ))
        profile_box.add_widget(Label(
            text=culprit["description"],
            font_size=12,
            color=(0.80, 0.76, 0.62, 1),
            size_hint=(1, None),
            height=22,
            halign="center",
        ))
        profile_box.add_widget(Label(
            text=f"Motive: {culprit['motive']}",
            font_size=11,
            color=(0.65, 0.60, 0.45, 1),
            size_hint=(1, None),
            height=20,
            halign="center",
        ))
        root.add_widget(profile_box)

        # Clues collected summary
        clues_lbl = Label(
            text=f"Clues collected: {len(game_state.collected_clues)} / 9",
            font_size=13,
            color=(0.65, 0.80, 0.65, 1),
            size_hint=(1, None),
            height=24,
            halign="center",
        )
        clues_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))
        root.add_widget(clues_lbl)

        # Buttons
        btns = BoxLayout(orientation="horizontal", size_hint=(1, None), height=50, spacing=10)

        play_again = Button(
            text="New Game",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.22, 0.16, 0.06, 1),
            color=self.GOLD,
            font_size=15,
            bold=True,
        )
        play_again.bind(on_release=self._new_game)

        menu_btn = Button(
            text="Main Menu",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.12, 0.09, 0.04, 1),
            color=(0.70, 0.65, 0.50, 1),
            font_size=15,
        )
        menu_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "menu"))

        btns.add_widget(play_again)
        btns.add_widget(menu_btn)
        root.add_widget(btns)

        self.add_widget(root)

    def _new_game(self, *_):
        from game.models.game_state import game_state
        game_state.reset()
        self.manager.current = "scene"

    def _upd(self, *_):
        self._bg.pos = self.pos
        self._bg.size = self.size

    @staticmethod
    def _draw_sep(widget):
        with widget.canvas:
            Color(0.88, 0.72, 0.28, 1)
            Rectangle(pos=widget.pos, size=widget.size)
