# mod/pop_test.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from tools.mod_bottom_menu import BottomMenu

# ====== 🔥 START IMPORT (NEW MENU SYSTEM)
from tools.menu_config import get_menu_items
# ====== 🔥 END IMPORT


KV = '''
<PopTestScreen>:
    md_bg_color: app.theme_cls.bg_dark

    MDBoxLayout:
        orientation: "vertical"

        # ===== TOP BAR
        MDTopAppBar:
            id: top_bar
            title: app.lang.get("test_title")
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["cog", lambda x: app.switch_screen("settings")]]

        # ===== Chat Area
        ScrollView:
            id: scroll

            MDBoxLayout:
                id: chat_box
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(10)
                spacing: dp(8)

        # ===== Блок вводу
        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height
            padding: [dp(0), dp(0), dp(0), dp(20)]

            MDBoxLayout:
                size_hint_y: None
                height: input_text.height

                FloatLayout:
                    
                    BoxLayout:
                        size_hint_y: None
                        height: dp(70)
                        orientation: "horizontal"
                        spacing: dp(10)
                        padding: [dp(10), dp(5), dp(10), dp(20)]
                
                        # "+"
                        MDIconButton:
                            icon: "plus"
                            md_bg_color: app.theme_cls.primary_color
                            theme_icon_color: "Custom"
                            icon_color: 1,1,1,1
                            icon_size: "16sp"
                            size_hint: None, None
                            on_release: root.open_bottom_menu()
                
                        # INPUT
                        MDTextField:
                            id: input_text
                            multiline: True
                            max_height: dp(200)
                            size_hint_y: None
                            height: max(self.minimum_height, dp(30))
                            size_hint_x: 0.85
                            text_size: self.width, None
                            mode: "rectangle"
                            on_text:
                                self.height = min(self.minimum_height, self.max_height)
                
                        # SEND
                        MDIconButton:
                            icon: "send-variant-outline"
                            md_bg_color: app.theme_cls.primary_color
                            theme_icon_color: "Custom"
                            icon_color: 1,1,1,1
                            icon_size: "16sp"
                            size_hint: None, None
                            on_release: root.send_message()
'''

Builder.load_string(KV)


class PopTestScreen(MDScreen):

    # ====== 🔥 START open_bottom_menu (FIXED)
    def open_bottom_menu(self):
        if not hasattr(self, "bottom_menu"):

            items = get_menu_items("test")

            self.bottom_menu = BottomMenu(
                items=items,
                on_select=self.handle_menu
            )

        self.bottom_menu.open()
    # ====== 🔥 END open_bottom_menu


    # ====== 🔥 START handle_menu
    def handle_menu(self, action):
        print("Menu action:", action)

        if action == "clear":
            self.ids.chat_box.clear_widgets()

        elif action == "settings":
            MDApp.get_running_app().switch_screen("settings")

        elif action == "answers":
            MDApp.get_running_app().switch_screen("answers")

        elif action == "files":
            print("TEST files")

        elif action == "gem":
            MDApp.get_running_app().switch_screen("gem")

        elif action == "ai":
            MDApp.get_running_app().switch_screen("ai")

        elif action == "db":
            print("TEST DB")
    # ====== 🔥 END handle_menu


    # ===== SEND
    def send_message(self):
        text = self.ids.input_text.text.strip()
        if not text:
            return

        self.add_user_message(text)
        self.ids.input_text.text = ""

        self.typing_widget = self.add_bot_typing()
        Clock.schedule_once(self.fake_response, 2)


    def fake_response(self, dt):
        text = "Це тестова відповідь бота. Тут буде API, згодом. Я зараз працюю над цим"

        if self.typing_widget:
            self.ids.chat_box.remove_widget(self.typing_widget)

        self.add_bot_message(text)


    # ===== USER MESSAGE
    def add_user_message(self, text):
        app = MDApp.get_running_app()

        c = app.theme_cls.primary_color
        bg = (c[0], c[1], c[2], 0.3)

        text_color = (0, 0, 0, 1) if app.theme_cls.theme_style == "Light" else (1, 1, 1, 1)

        row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            adaptive_height=True,
            padding=[dp(5), dp(4)],
        )

        bubble = MDBoxLayout(
            orientation="vertical",
            padding=[dp(12), dp(8)],
            size_hint=(None, None),
            adaptive_height=True,
            md_bg_color=bg,
            radius=[22, 22, 6, 22],
        )

        label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=text_color,
            size_hint=(None, None),
            adaptive_size=True,
        )

        def update_size(instance, value):
            instance.width = min(value[0], dp(250))
            instance.text_size = (instance.width, None)

        label.bind(texture_size=update_size)

        bubble.add_widget(label)

        def update_bubble(instance, value):
            bubble.width = label.width + dp(24)

        label.bind(width=update_bubble)

        row.add_widget(MDBoxLayout())
        row.add_widget(bubble)

        self.ids.chat_box.add_widget(row)
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.05)


    # ===== BOT MESSAGE
    def add_bot_message(self, text):
        app = MDApp.get_running_app()

        if app.theme_cls.theme_style == "Dark":
            bg = (1, 1, 1, 0.05)
            text_color = (1, 1, 1, 1)
        else:
            bg = (0, 0, 0, 0.05)
            text_color = (0, 0, 0, 1)

        bubble = MDBoxLayout(
            orientation="vertical",
            padding=[dp(14), dp(10)],
            size_hint_y=None,
            adaptive_height=True,
            size_hint_x=1,
            md_bg_color=bg,
            radius=[22, 22, 22, 6],
        )

        label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=text_color,
            size_hint_y=None,
            adaptive_height=True,
            text_size=(self.width - dp(40), None),
        )

        bubble.add_widget(label)
        self.ids.chat_box.add_widget(bubble)

        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.05)


    # ===== TYPING
    def add_bot_typing(self):
        app = MDApp.get_running_app()

        if app.theme_cls.theme_style == "Dark":
            bg = (1, 1, 1, 0.05)
            text_color = (1, 1, 1, 1)
        else:
            bg = (0, 0, 0, 0.05)
            text_color = (0, 0, 0, 1)

        bubble = MDBoxLayout(
            orientation="vertical",
            padding=[dp(14), dp(10)],
            size_hint_y=None,
            adaptive_height=True,
            size_hint_x=1,
            md_bg_color=bg,
            radius=[22, 22, 22, 6],
        )

        label = MDLabel(
            text="...",
            theme_text_color="Custom",
            text_color=text_color,
            size_hint_y=None,
            adaptive_height=True,
        )

        bubble.add_widget(label)
        self.ids.chat_box.add_widget(bubble)

        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.05)

        return bubble


    def scroll_to_bottom(self):
        self.ids.scroll.scroll_y = 0


    def go_back(self):
        MDApp.get_running_app().go_back()


    # ====== 🔥 START update_text
    def update_text(self):
        app = MDApp.get_running_app()

        try:
            self.ids.top_bar.title = app.lang.get("test_title")

            if hasattr(self, "bottom_menu"):
                self.bottom_menu.update_text()

        except Exception as e:
            print(f"[PopTestScreen] {e}")
    # ====== 🔥 END update_text