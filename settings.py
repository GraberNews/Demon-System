# settings.py

from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen


KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<SettingsScreen>:
    name: "settings"
    #md_bg_color: get_color_from_hex("#0D4037")

    MDBoxLayout:
        orientation: "vertical"

        # Верхня панель
        MDTopAppBar:
            title: "Налаштування"
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["menu", lambda x: app.open_drawer()]]

        # Контент
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"

            MDLabel:
                text: "Налаштування"
                halign: "center"
                font_style: "H4"

            MDLabel:
                text: "Тут будуть параметри додатку"
                halign: "center"
                theme_text_color: "Secondary"
'''

Builder.load_string(KV)


class SettingsScreen(MDScreen):
    pass