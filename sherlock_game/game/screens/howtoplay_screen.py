"""How-to-play screen."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock


INSTRUCTIONS = """[b][color=e2b848]THE CASE[/color][/b]

Lord Blackwood's priceless ruby has been stolen from the British Museum. Scotland Yard is baffled. Only you — Sherlock Holmes — can unmask the thief.

[b][color=e2b848]HOW TO PLAY[/color][/b]

[b]1. Investigate Scenes[/b]
Tap the scene buttons at the bottom to travel between 221B Baker Street, the British Museum, and the East End Docks.

[b]2. Collect Clues[/b]
Inside each scene, tap highlighted objects to examine them. Clues are added to your Case File automatically.

[b]3. Review Your Case File[/b]
Tap [i]Case File[/i] to review all collected clues and see which suspects they implicate.

[b]4. Make Your Deduction[/b]
Once you have gathered [b]4 or more clues[/b], the [i]Deduce[/i] button unlocks. Choose your suspect wisely — you only get one accusation.

[b][color=e2b848]SUSPECTS[/color][/b]

• [b]Colonel Moran[/b] — Sharpshooter, gambler, dangerous.
• [b]Irene Adler[/b] — Brilliant, resourceful, with a personal claim.
• [b]Prof. Moriarty[/b] — Criminal mastermind. Never acts without purpose.

[b][color=e2b848]TIP[/color][/b]

Examine every object in every scene before making your accusation. The truth is in the details.
"""


class HowToPlayScreen(Screen):
    BG = (0.07, 0.05, 0.03, 1)
    GOLD = (0.88, 0.72, 0.28, 1)

    def on_enter(self):
        Clock.schedule_once(self._deferred_enter, 0)

    def _deferred_enter(self, dt):
        self.clear_widgets()
        with self.canvas.before:
            Color(*self.BG)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        header = Label(
            text="How to Play",
            font_size=26,
            bold=True,
            color=self.GOLD,
            size_hint=(1, None),
            height=50,
        )
        root.add_widget(header)

        scroll = ScrollView(size_hint=(1, 1))
        content = Label(
            text=INSTRUCTIONS,
            markup=True,
            font_size=15,
            color=(0.92, 0.88, 0.78, 1),
            size_hint=(1, None),
            halign="left",
            valign="top",
            padding=(10, 10),
        )
        content.bind(width=lambda inst, v: setattr(inst, "text_size", (v, None)))
        content.bind(texture_size=lambda inst, v: setattr(inst, "height", v[1]))
        scroll.add_widget(content)
        root.add_widget(scroll)

        back_btn = Button(
            text="Back to Menu",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(0.20, 0.14, 0.06, 1),
            color=self.GOLD,
            font_size=16,
            bold=True,
        )
        back_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "menu"))
        root.add_widget(back_btn)

        self.add_widget(root)

    def _update_bg(self, *_):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
