# screens/settings.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

KV = '''
# ===== Елемент мови з чекбоксом (тип confirmation)
<LangItem>:
    on_release: root.set_icon(check)

    CheckboxLeftWidget:
        id: check
        group: "lang_group"

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

                # ===== МОВА — весь блок клікабельний
                MDCard:
                    radius: [16,]
                    elevation: 2
                    padding: "15dp"
                    size_hint_y: None
                    height: "100dp"
                    md_bg_color: app.theme_cls.bg_light
                    on_release: root.open_language_dialog()
                    ripple_behavior: True

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
                                text: app.lang.get("language_current")
                                theme_text_color: "Secondary"

                        Widget:

                        MDIcon:
                            icon: "chevron-right"
                            size_hint: None, None
                            size: "24dp", "24dp"
                            pos_hint: {"center_y": 0.5}
                            theme_text_color: "Secondary"

                # ===== ТЕМА
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

                # ===== ІНШЕ
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

                # ===== ПРО НАС
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


# ===== Елемент списку мов з radio-чекбоксом
class LangItem(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        for check in instance_check.get_widgets(instance_check.group):
            if check != instance_check:
                check.active = False


class SettingsScreen(MDScreen):

    def on_pre_enter(self):
        app = MDApp.get_running_app()

        self._syncing_switch = True
        is_dark = app.config_manager.get_theme() == "Dark"
        self.ids.theme_switch.active = is_dark
        self._syncing_switch = False

    def go_back(self):
        MDApp.get_running_app().go_back()

    def menu_placeholder(self):
        print("Menu placeholder")

    # ===== ТЕМА
    def toggle_theme(self, value):
        if getattr(self, '_syncing_switch', False):
            return

        app = MDApp.get_running_app()

        if value:
            app.theme_manager.set_dark()
            app.config_manager.set_theme("Dark")
        else:
            app.theme_manager.set_light()
            app.config_manager.set_theme("Light")

    # ===== ДІАЛОГ МОВИ
    def open_language_dialog(self):
        app = MDApp.get_running_app()
        current = app.lang.current

        # Кл. Початок. Додано німецьку (de) та іспанську (es) у список мов
        langs = [
            ("English",     "en"),
            ("Українська",  "ua"),
            ("Français",    "fr"),
            ("Deutsch",     "de"),
            ("Español",     "es"),
        ]
        # Кл. Кінець

        self._lang_items = []

        for label, code in langs:
            item = LangItem(text=label)
            item._lang_code = code
            self._lang_items.append(item)

        self.dialog = None

        self.dialog = MDDialog(
            title=app.lang.get("dialog_language"),
            type="confirmation",
            items=self._lang_items,
            buttons=[
                MDFlatButton(
                    text=app.lang.get("cancel"),
                    text_color=app.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text=app.lang.get("apply"),
                    text_color=app.theme_cls.primary_color,
                    on_release=lambda x: self.apply_language()
                ),
            ],
        )

        self.dialog.open()

        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._set_active_check(current), 0.05)

    def _set_active_check(self, current_lang):
        for item in self._lang_items:
            if item._lang_code == current_lang:
                try:
                    item.ids.check.active = True
                except Exception as e:
                    print(f"[SettingsScreen] check error: {e}")
                break

    def apply_language(self):
        app = MDApp.get_running_app()

        selected = None
        for item in self._lang_items:
            try:
                if item.ids.check.active:
                    selected = item._lang_code
                    break
            except Exception:
                pass

        if selected and selected != app.lang.current:
            app.lang.set(selected)
            app.config_manager.set_lang(selected)
            self.update_text()

        if self.dialog:
            self.dialog.dismiss()

    # ===== ОНОВЛЕННЯ ТЕКСТІВ
    def update_text(self):
        app = MDApp.get_running_app()

        self.ids.top_bar.title   = app.lang.get("settings_title")
        self.ids.lang_title.text = app.lang.get("language")
        self.ids.lang_desc.text  = app.lang.get("language_current")
        self.ids.theme_title.text = app.lang.get("theme")
        self.ids.theme_desc.text  = app.lang.get("theme_desc")
        self.ids.other_title.text = app.lang.get("other")
        self.ids.other_desc.text  = app.lang.get("other_desc")
        self.ids.about_title.text = app.lang.get("about_us")
        self.ids.about_desc.text  = app.lang.get("about_us_desc")

        if hasattr(self, "dialog") and self.dialog:
            self.dialog.title = app.lang.get("language")
            self.dialog.buttons[0].text = app.lang.get("cancel")
            self.dialog.buttons[1].text = app.lang.get("apply")
