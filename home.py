# home.py
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen

from mod.pop_ai import PopAIScreen
from mod.pop_gem import PopGemScreen


KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<HomeScreen>:
    name: "home"
    md_bg_color: get_color_from_hex("#0D4037")

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Demon System"
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["menu", lambda x: app.open_drawer()]]

        MDLabel:
            text: "Головний екран"
            halign: "center"
            valign: "middle"
            font_style: "H4"
            theme_text_color: "Primary"
            size_hint_y: 0.7

    MDFloatLayout:

        MDFloatingActionButton:
            icon: "robot"
            md_bg_color: app.theme_cls.accent_color
            pos_hint: {"center_x": 0.88, "center_y": 0.08}
            elevation: 10
            on_release: root.open_ai()

        MDFloatingActionButton:
            icon: "star-four-points"
            md_bg_color: get_color_from_hex("#03A9F4")
            pos_hint: {"center_x": 0.88, "center_y": 0.19}
            elevation: 10
            on_release: root.open_gem()
'''
# -----------------------------------

Builder.load_string(KV)


class HomeScreen(MDScreen):

    def on_enter(self):
        manager = self.manager
        if manager:
            if not manager.has_screen("ai"):
                manager.add_widget(PopAIScreen(name="ai"))

            if not manager.has_screen("gem"):
                manager.add_widget(PopGemScreen(name="gem"))

    def open_ai(self):
        if self.manager:
            self.manager.current = "ai"

    def open_gem(self):
        if self.manager:
            self.manager.current = "gem"