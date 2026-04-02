"""Main menu screen."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.animation import Animation
from kivy.clock import Clock
import math


class FogParticle(Widget):
    """Animated fog/smoke particle for atmospheric background."""

    def __init__(self, x, y, radius, speed, **kwargs):
        super().__init__(**kwargs)
        self._x = x
        self._y = y
        self._radius = radius
        self._speed = speed
        self._alpha = 0.0
        self._phase = 0.0
        with self.canvas:
            self._color = Color(0.7, 0.75, 0.8, 0)
            self._ellipse = Ellipse(
                pos=(x - radius, y - radius),
                size=(radius * 2, radius * 2),
            )
        Clock.schedule_interval(self._tick, 1 / 30)

    def _tick(self, dt):
        self._phase += dt * self._speed
        self._alpha = max(0.0, 0.18 * math.sin(self._phase) + 0.12)
        self._color.a = self._alpha
        ox = 40 * math.sin(self._phase * 0.7)
        self._ellipse.pos = (self._x + ox - self._radius, self._y - self._radius)


class MenuScreen(Screen):
    BG_COLOR = (0.06, 0.04, 0.02, 1)
    GOLD = (0.88, 0.72, 0.28, 1)
    CREAM = (0.95, 0.92, 0.82, 1)
    BTN_COLOR = (0.20, 0.14, 0.06, 1)
    BTN_PRESS = (0.35, 0.24, 0.10, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._fog_particles = []
        self.bind(size=self._on_resize, pos=self._on_resize)

    def _on_resize(self, *_):
        if self.width > 0 and self.height > 0:
            Clock.schedule_once(lambda dt: self._build(), 0)

    def on_enter(self):
        self._build()

    def _build(self, *_):
        self.canvas.before.clear()
        self.clear_widgets()
        self._fog_particles.clear()

        w, h = self.width, self.height

        with self.canvas.before:
            # Dark Victorian background
            Color(*self.BG_COLOR)
            Rectangle(pos=self.pos, size=self.size)

            # Foggy street light glow at top-center
            Color(0.9, 0.85, 0.5, 0.08)
            Ellipse(pos=(w * 0.35, h * 0.55), size=(w * 0.3, h * 0.3))

            # Silhouette of London rooftops (simple polygon via Lines)
            Color(0.03, 0.02, 0.01, 1)
            # Left block
            Rectangle(pos=(0, 0), size=(w * 0.18, h * 0.28))
            # Middle-left
            Rectangle(pos=(w * 0.22, 0), size=(w * 0.12, h * 0.22))
            # Middle chimney
            Rectangle(pos=(w * 0.40, 0), size=(w * 0.08, h * 0.32))
            Rectangle(pos=(w * 0.38, h * 0.30), size=(w * 0.04, h * 0.06))
            # Right block
            Rectangle(pos=(w * 0.70, 0), size=(w * 0.20, h * 0.25))
            Rectangle(pos=(w * 0.85, 0), size=(w * 0.15, h * 0.20))
            # Far-right tower
            Rectangle(pos=(w * 0.93, 0), size=(w * 0.07, h * 0.30))

            # Moon
            Color(0.95, 0.93, 0.80, 0.85)
            Ellipse(pos=(w * 0.80, h * 0.78), size=(w * 0.10, w * 0.10))
            Color(0.06, 0.04, 0.02, 0.6)
            Ellipse(pos=(w * 0.83, h * 0.79), size=(w * 0.10, w * 0.10))

            # Gold decorative lines
            Color(*self.GOLD)
            Line(points=[w * 0.1, h * 0.86, w * 0.9, h * 0.86], width=1.2)
            Line(points=[w * 0.1, h * 0.38, w * 0.9, h * 0.38], width=1.2)

        # Fog particles
        import random
        random.seed(42)
        for _ in range(6):
            p = FogParticle(
                x=random.uniform(0.1, 0.9) * w,
                y=random.uniform(0.3, 0.55) * h,
                radius=random.uniform(40, 90),
                speed=random.uniform(0.3, 0.8),
            )
            self.add_widget(p)
            self._fog_particles.append(p)

        # Main layout
        layout = BoxLayout(
            orientation="vertical",
            padding=[w * 0.08, h * 0.06],
            spacing=h * 0.018,
            size_hint=(1, 1),
            pos=(0, 0),
        )

        # Title
        title = Label(
            text="SHERLOCK HOLMES",
            font_size=min(w, h) * 0.075,
            bold=True,
            color=self.GOLD,
            size_hint=(1, 0.14),
            halign="center",
        )
        title.bind(size=lambda inst, v: setattr(inst, "text_size", v))

        subtitle = Label(
            text="The Case of the Stolen Ruby",
            font_size=min(w, h) * 0.038,
            color=self.CREAM,
            size_hint=(1, 0.08),
            halign="center",
            italic=True,
        )
        subtitle.bind(size=lambda inst, v: setattr(inst, "text_size", v))

        tagline = Label(
            text="[i]\"Elementary, my dear Watson.\"[/i]",
            markup=True,
            font_size=min(w, h) * 0.028,
            color=(0.70, 0.65, 0.50, 1),
            size_hint=(1, 0.07),
            halign="center",
        )
        tagline.bind(size=lambda inst, v: setattr(inst, "text_size", v))

        spacer1 = Widget(size_hint=(1, 0.12))

        btn_new = self._make_button(
            "New Investigation", min(w, h) * 0.048, self._on_new_game
        )
        btn_how = self._make_button(
            "How to Play", min(w, h) * 0.040, self._on_how_to_play
        )

        spacer2 = Widget(size_hint=(1, 0.08))

        version = Label(
            text="v1.0  •  221B Productions",
            font_size=min(w, h) * 0.022,
            color=(0.45, 0.40, 0.30, 1),
            size_hint=(1, 0.06),
            halign="center",
        )
        version.bind(size=lambda inst, v: setattr(inst, "text_size", v))

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(tagline)
        layout.add_widget(spacer1)
        layout.add_widget(btn_new)
        layout.add_widget(btn_how)
        layout.add_widget(spacer2)
        layout.add_widget(version)
        self.add_widget(layout)

    def _make_button(self, text, font_size, callback):
        btn = Button(
            text=text,
            font_size=font_size,
            size_hint=(0.7, None),
            height=max(52, self.height * 0.08),
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=self.BTN_COLOR,
            color=self.GOLD,
            bold=True,
        )
        btn.bind(on_release=callback)
        btn.bind(
            on_press=lambda b: setattr(b, "background_color", self.BTN_PRESS),
            on_release=lambda b: setattr(b, "background_color", self.BTN_COLOR),
        )
        # Wrap in a container to allow pos_hint
        container = BoxLayout(size_hint=(1, None), height=btn.height + 8)
        container.bind(height=lambda c, v: setattr(btn, "height", v - 8))
        container.add_widget(btn)
        return container

    def _on_new_game(self, *_):
        from game.models.game_state import game_state
        game_state.reset()
        self.manager.current = "scene"

    def _on_how_to_play(self, *_):
        self.manager.current = "howtoplay"
