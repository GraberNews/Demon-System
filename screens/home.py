# screens/home.py
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<HomeScreen>:
    name: "home"
    md_bg_color: get_color_from_hex("#0D4037")

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: top_bar
            title: app.lang.get("home_title")
            elevation: 4
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["menu", lambda x: app.open_drawer()]]
            right_action_items: [["dots-vertical", lambda x: root.menu_placeholder()]]

        MDLabel:
            id: main_label
            halign: "center"
            valign: "middle"
            font_style: "H4"
            theme_text_color: "Primary"
            size_hint_y: 0.7

    MDFloatLayout:

        MDFloatingActionButton:
            icon: "robot"
            icon_size: "90"
            md_bg_color: get_color_from_hex("#ff9900")
            pos_hint: {"center_x": 0.12, "center_y": 0.06}
            elevation: 10
            on_release: root.open_ai()

        MDFloatingActionButton:
            icon: "star-four-points"
            #icon_color: "#abbfff"
            icon_size: "150"
            md_bg_color: get_color_from_hex("#6699ff")
            pos_hint: {"center_x": 0.32, "center_y": 0.06}
            elevation: 10
            on_release: root.open_gem()
            
        MDFloatingActionButton:
            icon: "ab-testing"
            icon_color: "#6699ff"
            icon_size: "120"
            md_bg_color: get_color_from_hex("#424954")
            pos_hint: {"center_x": 0.88, "center_y": 0.06}
            elevation: 10
            on_release: root.open_test()
'''

Builder.load_string(KV)

class HomeScreen(MDScreen):

    def open_ai(self):
        if self.manager:
            self.manager.current = "ai"

    def open_gem(self):
        if self.manager:
            self.manager.current = "gem"

    def open_test(self):
        if self.manager:
            self.manager.current = "test"

    def menu_placeholder(self):
        print("Menu placeholder - Home")

    # АС оновлення текстів при зміні мови
    def update_text(self):
        app = MDApp.get_running_app()

        try:
            self.ids.top_bar.title = app.lang.get("home_title")
        except Exception as e:
            print(f"[HomeScreen] {e}")