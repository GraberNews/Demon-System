from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

KV = '''
<PopAIScreen>:
    md_bg_color: app.theme_cls.bg_dark

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Gem Demon"
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
                padding: dp(20)
                spacing: dp(10)

       # Панель вводу
        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height
            padding: [dp(5), dp(5), dp(5), dp(20)]

            # контейнер поля
            MDBoxLayout:
                size_hint_y: None
                height: input_text.height
                radius: [8]
                padding: [dp(2), dp(20), dp(2), dp(15)]

                FloatLayout:

                    MDTextField:
                        id: input_text
                        hint_text: "Запитай..."
                        multiline: True
                        max_height: dp(200)
                        size_hint_y: None
                        height: max(self.minimum_height, dp(40))
                        size_hint_x: 0.85
                        pos_hint: {"x": 0, "center_y": 0.6}
                        text_size: self.width, None
                        mode: "rectangle"
                        line_color_normal: 0.5, 0.5, 0.5, 1
                        line_color_focus: app.theme_cls.primary_color
                        on_text:
                            self.height = min(self.minimum_height, self.max_height)

                    MDIconButton:
                        icon: "send"   # інша іконка
                        theme_icon_color: "Custom"
                        icon_color: 1, 1, 1, 1
                        md_bg_color: app.theme_cls.primary_color
                        size_hint: None, None
                        size: dp(36), dp(36)
                        pos_hint: {"right": 1, "center_y": 0.4}
                        on_release: root.send_message()
'''

Builder.load_string(KV)

class PopAIScreen(MDScreen):

    def send_message(self):
        text = self.ids.input_text.text.strip()
        if not text:
            return

        self.add_message(text, "user")
        self.ids.input_text.text = ""

        # тестова відповідь
        Clock.schedule_once(
            lambda dt: self.add_message("Я демон, але вже думаю", "bot"),
            0.3
        )

    def add_message(self, text, sender):
        align = "right" if sender == "user" else "left"

        msg = MDLabel(
            text=text,
            size_hint_y=None,
            halign=align,
            theme_text_color="Primary"
        )

        msg.bind(texture_size=msg.setter("size"))
        self.ids.chat_box.add_widget(msg)

        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.05)

    def scroll_to_bottom(self):
        self.ids.scroll.scroll_y = 0

    def go_back(self):
        self.manager.current = "home"