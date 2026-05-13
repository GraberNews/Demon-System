# mod/pop_test.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp

from tools.mod_bottom_menu import BottomMenu
from tools.menu_config import get_menu_items
from tools.manage_api import APIManager
from mod.base_chat_screen import BaseChatScreen


KV = '''
<PopTestScreen>:
    md_bg_color: app.theme_cls.bg_dark

    FloatLayout:

        MDBoxLayout:
            id: root_box
            orientation: "vertical"
            size_hint: 1, 1

            MDTopAppBar:
                id: top_bar
                title: app.lang.get("test_title")
                elevation: 4
                left_action_items: [["arrow-left", lambda x: root.go_back()]]
                right_action_items: [["cog", lambda x: app.switch_screen("settings")]]

            ScrollView:
                id: scroll

                MDBoxLayout:
                    id: chat_box
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(10)
                    spacing: dp(10)

            # Кл. Початок. Порожній спейсер висотою блоку вводу —
            # щоб ScrollView не перекривав контент знизу
            Widget:
                id: input_spacer
                size_hint_y: None
                height: input_area.height
            # Кл. Кінець

        # Кл. Початок. Блок вводу винесено з root_box у FloatLayout.
        # y: root.input_y піднімає ВЕСЬ блок (поле + кнопки) разом з клавіатурою.
        MDBoxLayout:
            id: input_area
            orientation: "vertical"
            size_hint: 1, None
            height: self.minimum_height
            y: root.input_y
            padding: [dp(10), 0, dp(10), dp(15)]

            ChatInputCard:
                id: input_card

                MDTextField:
                    id: input_text
                    hint_text: app.lang.get("hint_title")
                    multiline: True
                    max_height: dp(200)
                    radius: [40]
                    size_hint_y: None
                    height: max(self.minimum_height, dp(36))
                    size_hint_x: 1
                    mode: "fill"
                    line_color_normal: app.theme_cls.primary_color
                    line_color_focus:  app.theme_cls.primary_color
                    on_text:
                        self.height = min(self.minimum_height, self.max_height)
                    # Кл. Початок. Виправлено on_focus — див. коментар у pop_ai.py
                    on_focus:
                        if self.focus: self.hint_text = ""
                        else: root._refresh_hint()
                    # Кл. Кінець

                MDBoxLayout:
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(6)

                    MDIconButton:
                        icon: "plus"
                        icon_size: "26sp"
                        size_hint: None, None
                        size: dp(38), dp(38)
                        icon_color: 1, 1, 1, 1
                        radius: [10,]
                        on_release: root.open_bottom_menu()

                    # Кл. Початок. Логотип чату між кнопками — у майбутньому буде іконка
                    MDLabel:
                        id: chat_logo
                        text: "TsT"
                        halign: "center"
                        valign: "middle"
                        font_style: "H6"
                        theme_text_color: "Primary"
                    # Кл. Кінець

                    MDIconButton:
                        icon: "send"
                        icon_size: "26sp"
                        size_hint: None, None
                        size: dp(38), dp(38)
                        icon_color: 1, 1, 1, 1
                        radius: [10,]
                        on_release: root.send_message()
        # Кл. Кінець

        MDIconButton:
            id: btn_top_menu
            icon: "dots-vertical"
            icon_size: "16sp"
            elevation: 4
            size_hint: None, None
            size: dp(40), dp(40)
            pos_hint: {"right": 0.98, "top": 0.9}
            theme_icon_color: "Custom"
            icon_color:
                (1, 1, 1, 0.9) if app.theme_cls.theme_style == "Dark" \
                else (0.1, 0.1, 0.1, 0.9)
            md_bg_color:
                (0.25, 0.25, 0.25, 0.7) if app.theme_cls.theme_style == "Dark" \
                else (0.91, 0.91, 0.91, 0.7)
            on_release: root.open_top_menu()
'''

Builder.load_string(KV)


class PopTestScreen(BaseChatScreen):

    def on_kv_post(self, base_widget):
        self.setup_keyboard_handler()
        self.setup_input_colors()
        self.bottom_menu = BottomMenu(
            items=get_menu_items("test"),
            on_select=self.handle_menu
        )
        self.history = []
        self.api_chat_id = "test"
        # Назва провайдера береться з manage_api.py (блок ЧАТ: TEST)
        self.ids.chat_logo.text = APIManager.get_provider_name("test")

    def open_bottom_menu(self):
        self.bottom_menu.open()

    def handle_menu(self, action):
        app = MDApp.get_running_app()
        actions = {
            # Кл. Початок. "clear" викликає діалог підтвердження з BaseChatScreen
            "clear":   lambda: self.confirm_clear_chat(),
            # Кл. Кінець
            "answers": lambda: app.switch_screen("answers"),
            "ai":      lambda: app.switch_screen("ai"),
            "gem":     lambda: app.switch_screen("gem"),
            "files":   lambda: print("TEST files"),
            "db":      lambda: print("TEST DB"),
        }
        if action in actions:
            actions[action]()

    def update_text(self):
        app = MDApp.get_running_app()
        try:
            self.ids.top_bar.title = app.lang.get("test_title")
            # Кл. Початок. Завжди оновлюємо bottom_menu — він тепер завжди існує
            self.bottom_menu.update_text()
            # Кл. Кінець
            # Кл. Початок. Оновлюємо hint_text поля вводу при зміні мови
            self._refresh_hint()
            # Кл. Кінець
            if hasattr(self, "_top_menu"):
                self.build_top_menu()
        except Exception as e:
            print(f"[PopTestScreen] {e}")
