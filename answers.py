# screens/answers.py

from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<AnswersScreen>:
    name: "answers"
    #md_bg_color: get_color_from_hex("#0D4037")

    MDBoxLayout:
        orientation: "vertical"

        # Верхня панель
        MDTopAppBar:
            title: "Відповіді"
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["menu", lambda x: app.open_drawer()]]
            right_action_items: [["cog", lambda x: app.switch_screen("settings")]]

        # Контент
        MDBoxLayout:
            # Суди будем транслювати контент
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"

'''

Builder.load_string(KV)


class AnswersScreen(MDScreen):
    pass