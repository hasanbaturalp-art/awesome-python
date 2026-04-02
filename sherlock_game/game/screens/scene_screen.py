"""Investigation scene screen — tap objects to find clues."""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import (
    Color, Rectangle, Ellipse, Line, RoundedRectangle, Triangle
)
from kivy.animation import Animation
from kivy.clock import Clock
import math


# ---------- per-scene drawing helpers ----------

def _draw_baker_street(canvas, w, h):
    """Draw 221B Baker Street interior."""
    with canvas:
        # Floor
        Color(0.22, 0.14, 0.08, 1)
        Rectangle(pos=(0, 0), size=(w, h * 0.36))

        # Wallpaper – dark green Victorian
        Color(0.10, 0.16, 0.10, 1)
        Rectangle(pos=(0, h * 0.36), size=(w, h * 0.64))

        # Wallpaper pattern (simple grid)
        Color(0.13, 0.20, 0.13, 1)
        for xi in range(0, int(w), 30):
            Line(points=[xi, h * 0.36, xi, h], width=0.8)
        for yi in range(int(h * 0.36), int(h), 30):
            Line(points=[0, yi, w, yi], width=0.8)

        # Fireplace
        Color(0.15, 0.10, 0.06, 1)
        Rectangle(pos=(w * 0.35, h * 0.34), size=(w * 0.30, h * 0.32))
        Color(0.05, 0.03, 0.02, 1)
        Rectangle(pos=(w * 0.40, h * 0.36), size=(w * 0.20, h * 0.24))
        # Fire glow
        Color(0.9, 0.45, 0.05, 0.7)
        Ellipse(pos=(w * 0.42, h * 0.36), size=(w * 0.16, h * 0.10))
        Color(0.95, 0.70, 0.10, 0.5)
        Ellipse(pos=(w * 0.44, h * 0.38), size=(w * 0.12, h * 0.08))

        # Mantelpiece
        Color(0.28, 0.18, 0.10, 1)
        Rectangle(pos=(w * 0.32, h * 0.66), size=(w * 0.36, h * 0.04))

        # Letter on mantelpiece (interactive object marker drawn by object buttons)

        # Armchair (left)
        Color(0.35, 0.20, 0.10, 1)
        Rectangle(pos=(w * 0.04, h * 0.30), size=(w * 0.20, h * 0.22))
        Color(0.30, 0.16, 0.08, 1)
        Rectangle(pos=(w * 0.02, h * 0.38), size=(w * 0.05, h * 0.18))
        Rectangle(pos=(w * 0.23, h * 0.38), size=(w * 0.05, h * 0.18))

        # Bookshelf (right)
        Color(0.20, 0.12, 0.06, 1)
        Rectangle(pos=(w * 0.76, h * 0.34), size=(w * 0.22, h * 0.50))
        for bi in range(6):
            book_colors = [
                (0.55, 0.15, 0.10),
                (0.15, 0.25, 0.55),
                (0.15, 0.45, 0.20),
                (0.55, 0.40, 0.10),
                (0.40, 0.15, 0.45),
                (0.50, 0.50, 0.15),
            ]
            Color(*book_colors[bi], 1)
            bx = w * 0.78 + bi * (w * 0.03)
            Rectangle(pos=(bx, h * 0.36), size=(w * 0.025, h * 0.18))

        # Tobacco pouch on small table (right area)
        Color(0.28, 0.18, 0.08, 1)
        Rectangle(pos=(w * 0.62, h * 0.34), size=(w * 0.12, h * 0.06))

        # Window (top left)
        Color(0.35, 0.42, 0.55, 0.6)
        Rectangle(pos=(w * 0.04, h * 0.65), size=(w * 0.22, h * 0.28))
        Color(0.22, 0.28, 0.40, 1)
        Line(points=[w * 0.15, h * 0.65, w * 0.15, h * 0.93], width=1.5)
        Line(points=[w * 0.04, h * 0.79, w * 0.26, h * 0.79], width=1.5)

        # Map on wall (center-top)
        Color(0.75, 0.68, 0.48, 1)
        Rectangle(pos=(w * 0.38, h * 0.72), size=(w * 0.22, h * 0.18))
        Color(0.20, 0.30, 0.55, 0.8)
        Ellipse(pos=(w * 0.44, h * 0.76), size=(w * 0.06, h * 0.06))
        Color(0.55, 0.10, 0.10, 0.9)
        Ellipse(pos=(w * 0.50, h * 0.80), size=(w * 0.04, h * 0.04))


def _draw_museum(canvas, w, h):
    """Draw the British Museum crime scene."""
    with canvas:
        # Marble floor
        Color(0.82, 0.80, 0.78, 1)
        Rectangle(pos=(0, 0), size=(w, h * 0.36))
        Color(0.75, 0.73, 0.71, 1)
        for xi in range(0, int(w), 60):
            Line(points=[xi, 0, xi, h * 0.36], width=0.6)
        for yi in range(0, int(h * 0.36), 60):
            Line(points=[0, yi, w, yi], width=0.6)

        # Stone walls
        Color(0.55, 0.52, 0.48, 1)
        Rectangle(pos=(0, h * 0.36), size=(w, h * 0.64))

        # Pillars
        for px in [0.05, 0.80]:
            Color(0.68, 0.64, 0.60, 1)
            Rectangle(pos=(w * px, h * 0.32), size=(w * 0.12, h * 0.52))
            Color(0.72, 0.68, 0.64, 1)
            Rectangle(pos=(w * px - w * 0.02, h * 0.82), size=(w * 0.16, h * 0.04))

        # Display pedestal (smashed)
        Color(0.72, 0.68, 0.64, 1)
        Rectangle(pos=(w * 0.30, h * 0.36), size=(w * 0.40, h * 0.20))
        # Broken glass case (just outline + shards)
        Color(0.55, 0.70, 0.82, 0.5)
        Line(
            rectangle=(w * 0.30, h * 0.54, w * 0.40, h * 0.20),
            width=1.5,
            dash_offset=5,
            dash_length=8,
        )
        # Broken glass shards on floor
        Color(0.72, 0.82, 0.90, 0.6)
        for gx, gy in [
            (0.28, 0.34), (0.32, 0.32), (0.38, 0.33),
            (0.44, 0.35), (0.50, 0.32), (0.55, 0.34),
        ]:
            Ellipse(pos=(w * gx, h * gy), size=(8, 4))

        # Visitor ledger on a stand (right side)
        Color(0.40, 0.28, 0.14, 1)
        Rectangle(pos=(w * 0.74, h * 0.36), size=(w * 0.06, h * 0.24))
        Color(0.55, 0.35, 0.15, 1)
        Rectangle(pos=(w * 0.68, h * 0.56), size=(w * 0.18, h * 0.16))

        # Torn glove on floor (left of display)
        Color(0.88, 0.84, 0.78, 0.85)
        Ellipse(pos=(w * 0.60, h * 0.34), size=(w * 0.06, h * 0.04))

        # Skylight (top-center)
        Color(0.55, 0.62, 0.75, 0.4)
        Rectangle(pos=(w * 0.35, h * 0.82), size=(w * 0.30, h * 0.16))
        Color(0.48, 0.55, 0.68, 0.8)
        Line(points=[w * 0.50, h * 0.82, w * 0.50, h * 0.98], width=1.5)
        Line(points=[w * 0.35, h * 0.90, w * 0.65, h * 0.90], width=1.5)

        # Banner
        Color(0.20, 0.18, 0.12, 0.9)
        Rectangle(pos=(w * 0.18, h * 0.74), size=(w * 0.64, h * 0.08))
        # "BRITISH MUSEUM" text handled by Label


def _draw_docks(canvas, w, h):
    """Draw East End Docks night scene."""
    with canvas:
        # Night sky / fog
        Color(0.06, 0.08, 0.10, 1)
        Rectangle(pos=(0, h * 0.36), size=(w, h * 0.64))

        # Water
        Color(0.05, 0.10, 0.14, 1)
        Rectangle(pos=(0, 0), size=(w, h * 0.20))
        # Ripples
        Color(0.10, 0.16, 0.22, 0.7)
        for yi in range(int(h * 0.04), int(h * 0.20), 12):
            Line(points=[0, yi, w, yi], width=0.8)

        # Dock planks
        Color(0.20, 0.14, 0.08, 1)
        Rectangle(pos=(0, h * 0.20), size=(w, h * 0.16))
        Color(0.16, 0.11, 0.06, 1)
        for xi in range(0, int(w), 30):
            Line(points=[xi, h * 0.20, xi, h * 0.36], width=1.2)

        # Fog layer
        Color(0.55, 0.60, 0.58, 0.12)
        Rectangle(pos=(0, h * 0.28), size=(w, h * 0.20))

        # Moored ship hull (left background)
        Color(0.12, 0.10, 0.08, 1)
        Rectangle(pos=(-w * 0.05, h * 0.20), size=(w * 0.30, h * 0.22))
        # Mast
        Color(0.18, 0.14, 0.10, 1)
        Line(points=[w * 0.10, h * 0.42, w * 0.10, h * 0.88], width=2)
        Line(points=[w * 0.04, h * 0.70, w * 0.18, h * 0.70], width=1.2)

        # Shipping crate (left foreground)
        Color(0.35, 0.24, 0.12, 1)
        Rectangle(pos=(w * 0.12, h * 0.28), size=(w * 0.18, h * 0.14))
        Color(0.28, 0.18, 0.08, 1)
        Line(rectangle=(w * 0.12, h * 0.28, w * 0.18, h * 0.14), width=1.5)
        # Stencil "S.M." marker
        Color(0.80, 0.72, 0.40, 0.7)
        Line(points=[w * 0.16, h * 0.34, w * 0.16, h * 0.38], width=1.2)
        Line(points=[w * 0.16, h * 0.38, w * 0.19, h * 0.36], width=1.2)
        Line(points=[w * 0.19, h * 0.36, w * 0.19, h * 0.34], width=1.2)

        # Cigarette on dock (right-center)
        Color(0.82, 0.72, 0.55, 0.9)
        Rectangle(pos=(w * 0.56, h * 0.30), size=(w * 0.08, h * 0.012))
        Color(1.0, 0.40, 0.10, 0.8)
        Ellipse(pos=(w * 0.56, h * 0.298), size=(w * 0.012, h * 0.016))

        # Crumpled note (far right)
        Color(0.85, 0.80, 0.65, 0.85)
        Ellipse(pos=(w * 0.77, h * 0.34), size=(w * 0.06, h * 0.04))

        # Gas lamp (right)
        Color(0.30, 0.24, 0.16, 1)
        Line(points=[w * 0.88, h * 0.36, w * 0.88, h * 0.72], width=3)
        Color(0.88, 0.80, 0.45, 0.8)
        Ellipse(pos=(w * 0.83, h * 0.70), size=(w * 0.10, h * 0.08))
        Color(0.88, 0.80, 0.45, 0.25)
        Ellipse(pos=(w * 0.75, h * 0.64), size=(w * 0.26, h * 0.22))

        # Stars
        Color(0.90, 0.88, 0.80, 0.7)
        for sx, sy in [
            (0.25, 0.90), (0.40, 0.85), (0.55, 0.93),
            (0.62, 0.88), (0.70, 0.95), (0.80, 0.86),
        ]:
            Ellipse(pos=(w * sx, h * sy), size=(3, 3))


SCENE_DRAW_FNS = {
    "baker_street": _draw_baker_street,
    "museum": _draw_museum,
    "docks": _draw_docks,
}


# ---------- Object Tap Button ----------

class ObjectButton(Widget):
    """Circular tap target for an interactive object in a scene."""

    PULSE_COLOR = (0.95, 0.85, 0.30, 0.7)
    FOUND_COLOR = (0.30, 0.85, 0.40, 0.6)

    def __init__(self, obj_data, collected, on_tap, **kwargs):
        super().__init__(**kwargs)
        self._obj = obj_data
        self._collected = collected
        self._on_tap = on_tap
        self._pulse = 0.0
        self._growing = True
        self._draw()
        Clock.schedule_interval(self._animate, 1 / 30)

    def _draw(self):
        self.canvas.clear()
        r = min(self.width, self.height) * 0.4
        cx = self.center_x
        cy = self.center_y
        pr = r + 6 * math.sin(self._pulse)
        with self.canvas:
            if self._collected:
                Color(*self.FOUND_COLOR)
            else:
                alpha = 0.5 + 0.3 * math.sin(self._pulse)
                Color(self.PULSE_COLOR[0], self.PULSE_COLOR[1], self.PULSE_COLOR[2], alpha)
            Ellipse(
                pos=(cx - pr, cy - pr),
                size=(pr * 2, pr * 2),
            )
            if self._collected:
                Color(0.10, 0.60, 0.20, 1)
            else:
                Color(0.88, 0.72, 0.28, 1)
            Line(circle=(cx, cy, r), width=1.8)

    def _animate(self, dt):
        step = dt * 4
        if self._growing:
            self._pulse += step
            if self._pulse >= math.pi:
                self._growing = False
        else:
            self._pulse -= step
            if self._pulse <= 0:
                self._growing = True
                self._pulse = 0
        self._draw()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._on_tap(self._obj)
            return True
        return super().on_touch_down(touch)


# ---------- Scene Screen ----------

class SceneScreen(Screen):
    BG_DARK = (0.06, 0.04, 0.02, 1)
    GOLD = (0.88, 0.72, 0.28, 1)
    NAV_BG = (0.10, 0.07, 0.03, 1)

    def on_enter(self):
        Clock.schedule_once(lambda dt: self._build(), 0)

    def _build(self):
        from game.models.game_state import game_state, SCENES, CLUES
        self.clear_widgets()
        self.canvas.before.clear()

        w, h = self.width, self.height
        scene_data = SCENES[game_state.current_scene_id]
        game_state.visited_scenes.add(game_state.current_scene_id)

        with self.canvas.before:
            Color(*self.BG_DARK)
            Rectangle(pos=self.pos, size=self.size)

        root = BoxLayout(orientation="vertical")

        # --- Top bar ---
        top_bar = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=max(44, h * 0.07),
            padding=[8, 4],
            spacing=6,
        )
        with top_bar.canvas.before:
            Color(*self.NAV_BG)
            self._top_bg = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(
            pos=lambda i, v: setattr(self._top_bg, "pos", v),
            size=lambda i, v: setattr(self._top_bg, "size", v),
        )

        menu_btn = Button(
            text="Menu",
            size_hint=(None, 1),
            width=70,
            background_normal="",
            background_color=(0.22, 0.16, 0.06, 1),
            color=self.GOLD,
            font_size=13,
        )
        menu_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "menu"))

        scene_label = Label(
            text=scene_data["name"],
            font_size=max(14, h * 0.024),
            bold=True,
            color=self.GOLD,
            size_hint=(1, 1),
            halign="center",
        )
        scene_label.bind(size=lambda i, v: setattr(i, "text_size", v))

        clue_count = Label(
            text=f"Clues: {len(game_state.collected_clues)}",
            font_size=13,
            color=(0.75, 0.70, 0.55, 1),
            size_hint=(None, 1),
            width=80,
            halign="right",
        )
        clue_count.bind(size=lambda i, v: setattr(i, "text_size", v))

        top_bar.add_widget(menu_btn)
        top_bar.add_widget(scene_label)
        top_bar.add_widget(clue_count)
        root.add_widget(top_bar)

        # --- Scene description ---
        desc_label = Label(
            text=f"[i]{scene_data['description']}[/i]",
            markup=True,
            font_size=max(12, h * 0.020),
            color=(0.80, 0.76, 0.62, 1),
            size_hint=(1, None),
            height=max(32, h * 0.055),
            halign="center",
            valign="middle",
            padding=(10, 2),
        )
        desc_label.bind(size=lambda i, v: setattr(i, "text_size", v))
        with desc_label.canvas.before:
            Color(0.12, 0.09, 0.04, 1)
            Rectangle(pos=desc_label.pos, size=desc_label.size)
        desc_label.bind(
            pos=lambda i, v: i.canvas.before.clear() or _rebind_rect(i),
            size=lambda i, v: i.canvas.before.clear() or _rebind_rect(i),
        )
        root.add_widget(desc_label)

        # --- Scene art + interactive objects ---
        scene_area = FloatLayout(size_hint=(1, 1))
        draw_fn = SCENE_DRAW_FNS[scene_data["id"]]
        # Actual drawing happens after layout
        self._scene_area = scene_area
        self._scene_data = scene_data

        # Add object tap buttons
        for obj in scene_data["objects"]:
            px, py = obj["pos_hint"]
            collected = game_state.has_clue(obj["clue_id"])
            btn = ObjectButton(
                obj_data=obj,
                collected=collected,
                on_tap=self._on_object_tapped,
                size_hint=(None, None),
                size=(56, 56),
                pos_hint={"x": px - 0.07, "y": py - 0.07},
            )
            scene_area.add_widget(btn)

            lbl = Label(
                text=obj["label"],
                font_size=11,
                color=(0.88, 0.84, 0.70, 1),
                size_hint=(None, None),
                size=(80, 20),
                pos_hint={"x": px - 0.10, "y": py - 0.13},
                halign="center",
            )
            lbl.bind(size=lambda i, v: setattr(i, "text_size", v))
            scene_area.add_widget(lbl)

        root.add_widget(scene_area)

        # --- Bottom navigation ---
        nav_height = max(52, h * 0.10)
        nav_bar = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=nav_height,
            padding=[6, 4],
            spacing=4,
        )
        with nav_bar.canvas.before:
            Color(*self.NAV_BG)
            self._nav_bg = Rectangle(pos=nav_bar.pos, size=nav_bar.size)
        nav_bar.bind(
            pos=lambda i, v: setattr(self._nav_bg, "pos", v),
            size=lambda i, v: setattr(self._nav_bg, "size", v),
        )

        scene_buttons = [
            ("221B", "baker_street"),
            ("Museum", "museum"),
            ("Docks", "docks"),
        ]
        for label_text, scene_id in scene_buttons:
            is_current = scene_id == game_state.current_scene_id
            sb = Button(
                text=label_text,
                size_hint=(1, 1),
                background_normal="",
                background_color=(0.30, 0.22, 0.08, 1) if is_current else (0.16, 0.11, 0.04, 1),
                color=self.GOLD if is_current else (0.65, 0.58, 0.40, 1),
                font_size=max(12, h * 0.020),
                bold=is_current,
            )
            sid = scene_id  # capture
            sb.bind(on_release=lambda b, s=sid: self._go_to_scene(s))
            nav_bar.add_widget(sb)

        # Case file and Deduce buttons
        case_btn = Button(
            text="Case File",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.14, 0.20, 0.12, 1),
            color=(0.60, 0.88, 0.55, 1),
            font_size=max(12, h * 0.020),
        )
        case_btn.bind(on_release=lambda *_: setattr(self.manager, "current", "casefile"))

        can_deduce = game_state.can_deduce()
        deduce_btn = Button(
            text="Deduce",
            size_hint=(1, 1),
            background_normal="",
            background_color=(0.28, 0.12, 0.06, 1) if can_deduce else (0.10, 0.08, 0.06, 1),
            color=(0.95, 0.65, 0.30, 1) if can_deduce else (0.40, 0.36, 0.28, 1),
            font_size=max(12, h * 0.020),
            bold=can_deduce,
        )
        if can_deduce:
            deduce_btn.bind(
                on_release=lambda *_: setattr(self.manager, "current", "deduction")
            )

        nav_bar.add_widget(case_btn)
        nav_bar.add_widget(deduce_btn)

        root.add_widget(nav_bar)

        self.add_widget(root)

        # Schedule scene drawing after layout pass
        Clock.schedule_once(self._draw_scene, 0.05)

    def _draw_scene(self, *_):
        sa = self._scene_area
        w, h = sa.width, sa.height
        if w <= 0 or h <= 0:
            Clock.schedule_once(self._draw_scene, 0.05)
            return
        sa.canvas.before.clear()
        with sa.canvas.before:
            SCENE_DRAW_FNS[self._scene_data["id"]](sa.canvas.before, w, h)

    def _go_to_scene(self, scene_id):
        from game.models.game_state import game_state
        game_state.current_scene_id = scene_id
        self._build()

    def _on_object_tapped(self, obj_data):
        from game.models.game_state import game_state, CLUES
        clue = CLUES[obj_data["clue_id"]]
        is_new = game_state.collect_clue(clue["id"])
        self._show_clue_popup(clue, is_new)

    def _show_clue_popup(self, clue, is_new):
        header = "New Clue Found!" if is_new else "Clue (already collected)"
        suspect_text = ""
        if clue["points_to"]:
            from game.models.game_state import SUSPECTS
            name = next(s["name"] for s in SUSPECTS if s["id"] == clue["points_to"])
            suspect_text = f"\n\n[color=ffcc44][i]This implicates: {name}[/i][/color]"

        content = BoxLayout(orientation="vertical", padding=16, spacing=10)
        title_lbl = Label(
            text=f"[b]{clue['title']}[/b]",
            markup=True,
            font_size=18,
            color=(0.88, 0.72, 0.28, 1),
            size_hint=(1, None),
            height=36,
            halign="center",
        )
        title_lbl.bind(size=lambda i, v: setattr(i, "text_size", v))

        body_lbl = Label(
            text=clue["description"] + suspect_text,
            markup=True,
            font_size=14,
            color=(0.92, 0.88, 0.78, 1),
            size_hint=(1, 1),
            halign="left",
            valign="top",
            text_size=(300, None),
        )

        close_btn = Button(
            text="Continue Investigation",
            size_hint=(1, None),
            height=44,
            background_normal="",
            background_color=(0.20, 0.14, 0.06, 1),
            color=(0.88, 0.72, 0.28, 1),
            font_size=14,
        )

        content.add_widget(title_lbl)
        content.add_widget(body_lbl)
        content.add_widget(close_btn)

        popup = Popup(
            title=header,
            title_color=(0.88, 0.72, 0.28, 1),
            content=content,
            size_hint=(0.85, 0.55),
            background="",
            background_color=(0.10, 0.07, 0.03, 0.97),
            separator_color=(0.88, 0.72, 0.28, 1),
        )
        close_btn.bind(on_release=lambda *_: self._close_clue_popup(popup))
        popup.open()

    def _close_clue_popup(self, popup):
        popup.dismiss()
        self._build()


def _rebind_rect(widget):
    with widget.canvas.before:
        Color(0.12, 0.09, 0.04, 1)
        Rectangle(pos=widget.pos, size=widget.size)
