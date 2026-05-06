# screens/settings.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.widget import Widget

KV = '''
<SettingsScreen>:
    name: "settings"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: top_bar
            title: app.lang.get("settings_title")
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["dots-vertical", lambda x: root.menu_placeholder()]]

        MDScrollView:

            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "20dp"
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    radius: [16,]
                    elevation: 2
                    padding: "15dp"
                    size_hint_y: None
                    height: "100dp"
                    md_bg_color: app.theme_cls.bg_light

                    MDBoxLayout:
                        orientation: "horizontal"

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                id: lang_title
                                text: app.lang.get("language")
                                font_style: "H6"

                            MDLabel:
                                id: lang_desc
                                text: app.lang.get("language_desc")
                                theme_text_color: "Secondary"

                        Widget:

                        MDIconButton:
                            icon: "chevron-right"
                            on_release: root.open_language_dialog()

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
                                id: theme_title
                                text: app.lang.get("theme")
                                font_style: "H6"

                            MDLabel:
                                id: theme_desc
                                text: app.lang.get("theme_desc")
                                theme_text_color: "Secondary"

                        Widget:

                        MDSwitch:
                            id: theme_switch
                            on_active: root.toggle_theme(self.active)

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
                            id: other_title
                            text: app.lang.get("other")
                            font_style: "H6"

                        MDLabel:
                            id: other_desc
                            text: app.lang.get("other_desc")
                            theme_text_color: "Secondary"

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
                            id: about_title
                            text: app.lang.get("about_us")
                            font_style: "H6"

                        MDLabel:
                            id: about_desc
                            text: app.lang.get("about_us_desc")
                            theme_text_color: "Secondary"
'''

Builder.load_string(KV)


class SettingsScreen(MDScreen):

    def on_pre_enter(self):
        app = MDApp.get_running_app()

        # sync theme switch
        is_dark = app.config_manager.get_theme() == "Dark"
        self.ids.theme_switch.active = is_dark

    # АС нормальний back без костилів
    def go_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_back()

    def menu_placeholder(self):
        print("Menu placeholder")

    # Тема
    def toggle_theme(self, value):
        app = MDApp.get_running_app()

        if value:
            app.theme_manager.set_dark()
            app.config_manager.set_theme("Dark")
        else:
            app.theme_manager.set_light()
            app.config_manager.set_theme("Light")

    # Діалог мови
    # АС нормальний вибір з чеком
    def open_language_dialog(self):
        app = MDApp.get_running_app()
        self.selected_lang = app.lang.current

        self.lang_items = [
            self.create_lang_item("English", "en"),
            self.create_lang_item("Українська", "ua"),
            self.create_lang_item("Français", "fr"),
        ]

        self.dialog = MDDialog(
            title=app.lang.get("language"),
            type="simple",
            items=self.lang_items,
            buttons=[
                MDFlatButton(
                    text=app.lang.get("cancel"),
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text=app.lang.get("apply"),
                    on_release=lambda x: self.apply_language()
                ),
            ],
        )

        self.dialog.open()

    def create_lang_item(self, text, code):
        from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

        def on_item_release(instance):
            self.select_language(code)

            for item in self.lang_items:
                item.ids.icon.icon = "blank"

            instance.ids.icon.icon = "check"

        item = OneLineAvatarIconListItem(
            text=text,
            on_release=on_item_release
        )

        icon = IconLeftWidget(
            icon="check" if code == self.selected_lang else "blank"
        )

        item.add_widget(icon)
        item.ids.icon = icon

        return item

    def select_language(self, code):
        self.selected_lang = code
        print(f"Вибрано мову: {code}")

    def apply_language(self):
        app = MDApp.get_running_app()

        if hasattr(self, 'selected_lang'):
            app.lang.set(self.selected_lang)
            app.config_manager.set_lang(self.selected_lang)

        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()

        self.update_text()

    # АС повне оновлення текстів + діалог
    def update_text(self):
        app = MDApp.get_running_app()

        self.ids.top_bar.title = app.lang.get("settings_title")

        self.ids.lang_title.text = app.lang.get("language")
        self.ids.lang_desc.text = app.lang.get("language_desc")

        self.ids.theme_title.text = app.lang.get("theme")
        self.ids.theme_desc.text = app.lang.get("theme_desc")

        self.ids.other_title.text = app.lang.get("other")
        self.ids.other_desc.text = app.lang.get("other_desc")

        self.ids.about_title.text = app.lang.get("about_us")
        self.ids.about_desc.text = app.lang.get("about_us_desc")

        if hasattr(self, "dialog") and self.dialog:
            self.dialog.title = app.lang.get("language")
            self.dialog.buttons[0].text = app.lang.get("cancel")
            self.dialog.buttons[1].text = app.lang.get("apply")