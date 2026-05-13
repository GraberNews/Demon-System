# main.py
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp
from app.config_manager import ConfigManager
from kivymd.app import MDApp
from configparser import ConfigParser
from screens.answers import AnswersScreen
from screens.home import HomeScreen
from screens.settings import SettingsScreen
from mod.pop_ai import PopAIScreen
from mod.pop_gem import PopGemScreen
from mod.pop_test import PopTestScreen
from tools.theme import ThemeManager
from tools.left_menu import LeftMenu
from kivy.event import EventDispatcher
from kivy.properties import StringProperty

# ====== LANG
# Стабільна локалізація без лагів

class Lang(EventDispatcher):
    current = StringProperty("ua")

    def __init__(self):
        super().__init__()
        self._cache = {}
        self.data = ConfigParser()
        self.load()

    def load(self, lang=None):
        # Скидаємо ConfigParser щоб старі ключі не залишались
        self.data = ConfigParser()
        self._cache.clear()
        target = lang or self.current
        self.data.read(f"lang/{target}.ini", encoding="utf-8")

    def set(self, lang):
        if self.current != lang:
            # Завантажуємо ПЕРЕД зміною current
            # щоб до моменту dispatch дані вже були актуальні
            self.load(lang)
            # StringProperty сам викличе dispatch — ручний виклик не потрібен
            self.current = lang

    def get(self, key, section="main"):
        cache_key = f"{self.current}:{section}:{key}"
        if cache_key not in self._cache:
            self._cache[cache_key] = self.data.get(section, key, fallback=key)
        return self._cache[cache_key]

# Кл. Початок. Змінено режим softinput з "below_target" на "pan"
# "pan" дозволяє отримувати точну висоту клавіатури через on_keyboard_height
# і піднімати блок вводу вручну, не зачіпаючи ScrollView/root_box
Window.softinput_mode = "pan"
# Кл. Кінець

KV = '''

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
                        text: app.lang.get("app_main_title")
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
        self.config_manager = ConfigManager()

        # Стек навігації
        self.screen_stack = []

        # Мова
        saved_lang = self.config_manager.get_lang()
        self.lang.set(saved_lang)
        self.lang.bind(current=self.on_language_change)

        # Тема
        self.theme_manager = ThemeManager(self)
        saved_theme = self.config_manager.get_theme()

        if saved_theme == "Dark":
            self.theme_manager.set_dark()
        else:
            self.theme_manager.set_light()

        self.root_widget = Builder.load_string(KV)
        self.sm = self.root_widget.ids.sm

        # Screens
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(AnswersScreen(name="answers"))
        self.sm.add_widget(PopAIScreen(name="ai"))
        self.sm.add_widget(PopGemScreen(name="gem"))
        self.sm.add_widget(PopTestScreen(name="test"))
        # Drawer
        self.left_menu = LeftMenu(self)
        self.nav_drawer = self.left_menu.create_drawer()
        self.root_widget.ids.nav_layout.add_widget(self.nav_drawer)

        self.sm.bind(
            current=lambda instance, screen: self.left_menu.update(self.nav_drawer, screen)
        )

        # Перехід на Home
        Clock.schedule_once(self.lock_orientation, 0)
        Clock.schedule_once(self.go_to_home, 3)

        return self.root_widget

    # =====Мова

    def on_language_change(self, instance, value):
        print(f"Language changed to: {value}")

        if hasattr(self, 'left_menu'):
            self.left_menu.refresh(self.nav_drawer, self.sm.current)

        for screen in self.sm.screens:
            if hasattr(screen, "update_text"):
                try:
                    screen.update_text()
                except Exception as e:
                    print(f"Помилка {screen.name}: {e}")

    # ===== NAVIGATION

    # Правильна навігація зі стеком
    def switch_screen(self, screen_name):
        if screen_name and self.sm.current != screen_name:
            self.screen_stack.append(self.sm.current)

        self.sm.current = screen_name
        self.nav_drawer.set_state("close")

    def go_back(self):
        if self.screen_stack:
            self.sm.current = self.screen_stack.pop()
        else:
            self.sm.current = "home"

    # ===== Sys

    def go_to_home(self, dt):
        self.sm.current = "home"

    def open_drawer(self):
        self.nav_drawer.set_state("open")

    def lock_orientation(self, *args):
        if platform != "android":
            return

        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            ActivityInfo = autoclass('android.content.pm.ActivityInfo')
            activity = PythonActivity.mActivity
            activity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
            )
        except Exception as e:
            print(f"[lock_orientation] {e}")

if __name__ == '__main__':
    MainApp().run()