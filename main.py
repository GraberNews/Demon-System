# main.py --> PRELOADER

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp
from app.config_manager import ConfigManager
from kivymd.app import MDApp
from screens.answers import AnswersScreen
from screens.home import HomeScreen
from screens.settings import SettingsScreen
from mod.pop_ai import PopAIScreen
from mod.pop_gem import PopGemScreen
from tools.theme import ThemeManager
from tools.left_menu import LeftMenu
from configparser import ConfigParser

from kivy.event import EventDispatcher
from kivy.properties import StringProperty


#  Перемикання мови
class Lang(EventDispatcher):
    current = StringProperty("ua")  # 🔥 тригер

    def __init__(self):
        super().__init__()
        self.data = ConfigParser()
        self.load()

    def load(self):
        self.data.read(f"lang/{self.current}.ini", encoding="utf-8")

    def set(self, lang):
        self.current = lang   # 🔥 ТРИГЕР
        self.load()

    def get(self, key, section="main"):
        return self.data.get(section, key, fallback=key)
# Кінець перемикання мови

Window.softinput_mode = "below_target"


KV = '''
#:import dp kivy.metrics.dp

<DrawerInfoBlock>:
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height
    padding: dp(16), dp(10)
    spacing: dp(4)

    MDLabel:
        text: root.title
        font_style: "Caption"
        theme_text_color: "Hint"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: root.text
        font_style: "Body2"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: self.texture_size[1]


MDScreen:

    MDNavigationLayout:
        id: nav_layout

        MDScreenManager:
            id: sm

            MDScreen:
                name: "preloader"
                md_bg_color: "#00695C"

                MDBoxLayout:
                    orientation: "vertical"
                    padding: "40dp"
                    spacing: "20dp"

                    Widget:

                    MDIcon:
                        icon: "shield-key-outline"
                        halign: "center"
                        font_size: "120sp"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.9

                    MDLabel:
                        text: app.lang.get("app_title")
                        halign: "center"
                        font_style: "H3"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1

                    MDLabel:
                        text: "Loading..."
                        halign: "center"
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: 0.95, 0.95, 0.95, 0.8

                    Widget:
'''

class MainApp(MDApp):

    def build(self):
        self.lang = Lang()

                # Конфіг
        self.config_manager = ConfigManager()
        
        # Тема
        self.theme_manager = ThemeManager(self)
        
        # отримати збережену тему
        saved_theme = self.config_manager.get_theme()
        
        if saved_theme == "Dark":
            self.theme_manager.set_dark()
        else:
            self.theme_manager.set_light()

        self.root_widget = Builder.load_string(KV)
        self.sm = self.root_widget.ids.sm

        # Екрани
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(PopAIScreen(name="ai"))
        self.sm.add_widget(PopGemScreen(name="gem"))
        self.sm.add_widget(AnswersScreen(name="answers"))
        # Drawer (тепер через LeftMenu)
        self.left_menu = LeftMenu(self)
        self.nav_drawer = self.left_menu.create_drawer()
        self.root_widget.ids.nav_layout.add_widget(self.nav_drawer)

        # оновлення меню
        self.sm.bind(
            current=lambda instance, screen: self.left_menu.update(self.nav_drawer, screen)
        )

        # орієнтація (НЕ ЧІПАЄМО)
        Clock.schedule_once(self.lock_orientation, 0)

        # старт
        Clock.schedule_once(self.go_to_home, 5)

        return self.root_widget

    # Орієнтація
    def lock_orientation(self, *args):
        if platform != "android":
            return

        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        ActivityInfo = autoclass('android.content.pm.ActivityInfo')

        activity = PythonActivity.mActivity
        activity.setRequestedOrientation(
            ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        )

    # Перехід
    def switch_screen(self, screen_name):
        if screen_name:
            self.sm.current = screen_name

        self.nav_drawer.set_state("close")

    def go_to_home(self, dt):
        self.sm.current = "home"

    # Відкрити меню
    def open_drawer(self):
        self.nav_drawer.set_state("open")


if __name__ == '__main__':
    MainApp().run()