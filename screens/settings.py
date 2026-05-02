# screens/settings.py

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp


KV = '''
<SettingsScreen>:
    name: "settings"

    MDBoxLayout:
        orientation: "vertical"

        # 🔝 Top Bar
        MDTopAppBar:
            title: app.lang.get("settings_title")
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["dots-vertical", lambda x: root.menu_placeholder()]]

        # 📦 Контент
        MDScrollView:

            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "20dp"
                size_hint_y: None
                height: self.minimum_height

                # 🌍 Блок 1 — Мова
                MDCard:
                    radius: [16,]
                    elevation: 2
                    padding: "15dp"
                    size_hint_y: None
                    height: "100dp"
                    md_bg_color: app.theme_cls.bg_light

                    MDBoxLayout:
                        orientation: "vertical"

                        MDLabel:
                            text: app.lang.get("language")
                            font_style: "H6"

                        MDLabel:
                            text: app.lang.get("language_desc")
                            theme_text_color: "Secondary"

                # 🎨 Блок 2 — Тема
                MDCard:
                    radius: [16,]
                    elevation: 2
                    padding: "15dp"
                    size_hint_y: None
                    height: "100dp"
                    md_bg_color: app.theme_cls.bg_light

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "10dp"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: app.lang.get("theme")
                                font_style: "H6"

                            MDLabel:
                                text: app.lang.get("theme_desc")
                                theme_text_color: "Secondary"

                        Widget:

                        MDSwitch:
                            id: theme_switch
                            on_active: root.toggle_theme(self.active)

                # ⚙️ Блок 3 — Інше
                MDCard:
                    radius: [16,]
                    elevation: 2
                    padding: "15dp"
                    size_hint_y: None
                    height: "100dp"
                    md_bg_color: app.theme_cls.bg_light

                    MDBoxLayout:
                        orientation: "vertical"

                        MDLabel:
                            text: app.lang.get("other")
                            font_style: "H6"

                        MDLabel:
                            text: app.lang.get("other_desc")
                            theme_text_color: "Secondary"

                # ℹ️ Блок 4 — Про нас
                MDCard:
                    radius: [16,]
                    elevation: 2
                    padding: "15dp"
                    size_hint_y: None
                    height: "100dp"
                    md_bg_color: app.theme_cls.bg_light

                    MDBoxLayout:
                        orientation: "vertical"

                        MDLabel:
                            text: app.lang.get("about_us")
                            font_style: "H6"

                        MDLabel:
                            text: app.lang.get("about_us_desc")
                            theme_text_color: "Secondary"
'''

Builder.load_string(KV)


class SettingsScreen(MDScreen):

    def on_pre_enter(self):
        # 🔙 звідки зайшли
        self.prev_screen = self.manager.previous()

        # ✅ правильний доступ до app
        app = MDApp.get_running_app()

        # 🎨 встановити стан switch
        is_dark = app.config_manager.get_theme() == "Dark"
        self.ids.theme_switch.active = is_dark

    def go_back(self):
        if self.prev_screen:
            self.manager.current = self.prev_screen
        else:
            self.manager.current = "home"

    def menu_placeholder(self):
        print("Menu placeholder (ще не реалізовано)")

    # 🔹 Перемикач теми
    def toggle_theme(self, value):
        app = MDApp.get_running_app()

        if value:
            app.theme_manager.set_dark()
            app.config_manager.set_theme("Dark")
        else:
            app.theme_manager.set_light()
            app.config_manager.set_theme("Light")