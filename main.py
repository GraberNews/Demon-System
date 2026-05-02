# main.py 1

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from home import HomeScreen
from settings import SettingsScreen
from mod.pop_ai import PopAIScreen
from mod.pop_gem import PopGemScreen

Window.softinput_mode = "below_target"


# 🔹 Інфо блок (ПРАВИЛЬНО для KivyMD 1.2.0)
class DrawerInfoBlock(MDBoxLayout):
    title = StringProperty("")
    text = StringProperty("")


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
                        text: "Demon System"
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
        # 🎨 Тема
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "500"

        self.root_widget = Builder.load_string(KV)
        self.sm = self.root_widget.ids.sm

        # 📱 Екрани
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(PopAIScreen(name="ai"))
        self.sm.add_widget(PopGemScreen(name="gem"))

        # ☰ Drawer
        self.nav_drawer = self.create_navigation_drawer()
        self.root_widget.ids.nav_layout.add_widget(self.nav_drawer)

        # 🔄 оновлення меню
        self.sm.bind(current=self.update_drawer)

        # 📱 орієнтація
        Clock.schedule_once(self.lock_orientation, 0)

        # 🚀 старт
        Clock.schedule_once(self.go_to_home, 2)

        return self.root_widget

    # 📱 Орієнтація
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

    # 📂 Drawer
    def create_navigation_drawer(self):
        from kivymd.uix.navigationdrawer import MDNavigationDrawer

        drawer = MDNavigationDrawer(
            anchor="left",
            width=dp(280)
        )

        self.drawer_menu = self.build_menu("home")
        drawer.add_widget(self.drawer_menu)

        return drawer

    # 🔄 Оновлення Drawer
    def update_drawer(self, instance, screen_name):
        self.nav_drawer.clear_widgets()
        self.drawer_menu = self.build_menu(screen_name)
        self.nav_drawer.add_widget(self.drawer_menu)

    # 🧠 Меню + інфо
    def build_menu(self, screen_name):
        from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
        from kivymd.uix.label import MDLabel
        from kivy.uix.scrollview import ScrollView

        scroll = ScrollView()
        menu = MDList()

        # 🔝 Header
        menu.add_widget(
            MDLabel(
                text="Demon System",
                font_style="H6",
                size_hint_y=None,
                height=dp(60),
                padding=[dp(16), dp(30), dp(16), dp(10)]
            )
        )

        # 🔘 Кнопка
        def item(text, icon, screen):
            btn = OneLineIconListItem(
                text=text,
                on_release=lambda x: self.switch_screen(screen)
            )
            btn.add_widget(IconLeftWidget(icon=icon))
            return btn

        # 🎯 Меню
        if screen_name == "settings":
            menu.add_widget(item("Home", "home", "home"))
            menu.add_widget(item("AI", "robot", "ai"))
            menu.add_widget(item("Gem", "star-four-points", "gem"))
            menu.add_widget(DrawerInfoBlock(
            title="AUTHOR",
            text="Nova Dev"
        ))
        else:
            menu.add_widget(item("Gem", "star-four-points", "gem"))
            menu.add_widget(item("AI", "robot", "ai"))
            menu.add_widget(item("Налаштування", "cog", "settings"))

        # ───────────────
        # 📌 ІНФО БЛОКИ
        # ───────────────
        menu.add_widget(DrawerInfoBlock(
            title="Інформація 1",
            text="""Це довгий текст який у майбутньому буде додаватись з локальної бази даних або текстового файлу. в даний час цей блок не є інформаційним"""
        ))

        menu.add_widget(DrawerInfoBlock(
            title="Інформація 2",
            text="Це довгий текст який у майбутньому буде додаватись з локальної бази даних або текстового файлу. в даний час цей блок не є інформаційним"
        ))

        scroll.add_widget(menu)
        return scroll

    # 🔄 Перехід
    def switch_screen(self, screen_name):
        if screen_name:
            self.sm.current = screen_name

        self.nav_drawer.set_state("close")

    def go_to_home(self, dt):
        self.sm.current = "home"

    # ☰ Відкрити меню
    def open_drawer(self):
        self.nav_drawer.set_state("open")


if __name__ == '__main__':
    MainApp().run()
