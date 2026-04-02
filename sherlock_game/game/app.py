"""Main Kivy application — wires up the ScreenManager."""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.config import Config

# Mobile-friendly window size (portrait)
Config.set("graphics", "width", "390")
Config.set("graphics", "height", "844")
Config.set("graphics", "resizable", True)
Config.set("graphics", "multisamples", "0")


class SherlockApp(App):
    title = "Sherlock Holmes: The Stolen Ruby"

    def build(self):
        Window.clearcolor = (0.06, 0.04, 0.02, 1)

        sm = ScreenManager(transition=FadeTransition(duration=0.25))

        # Import screens lazily to avoid circular issues
        from game.screens.menu_screen import MenuScreen
        from game.screens.howtoplay_screen import HowToPlayScreen
        from game.screens.scene_screen import SceneScreen
        from game.screens.casefile_screen import CaseFileScreen
        from game.screens.deduction_screen import DeductionScreen
        from game.screens.verdict_screen import VerdictScreen

        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(HowToPlayScreen(name="howtoplay"))
        sm.add_widget(SceneScreen(name="scene"))
        sm.add_widget(CaseFileScreen(name="casefile"))
        sm.add_widget(DeductionScreen(name="deduction"))
        sm.add_widget(VerdictScreen(name="verdict"))

        sm.current = "menu"
        return sm
