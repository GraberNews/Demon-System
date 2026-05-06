# screens/answers.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

KV = '''
<AnswersScreen>:
    name: "answers"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: top_bar
            title: app.lang.get("answers_title")
            left_action_items: [["menu", lambda x: app.open_drawer()]]
            right_action_items: [["cog", lambda x: app.switch_screen("settings")]]

        MDScrollView:

            MDBoxLayout:
                id: content_box
                orientation: "vertical"
                padding: "20dp"
                spacing: "20dp"
                size_hint_y: None
                height: self.minimum_height
'''

Builder.load_string(KV)

class AnswersScreen(MDScreen):

    def on_pre_enter(self):
        if "content_box" not in self.ids:
            print("[AnswersScreen] content_box не знайдено!")
            return

        self.load_content()

    def load_content(self):
        box = self.ids.content_box
        box.clear_widgets()

        from kivymd.uix.label import MDLabel

        box.add_widget(MDLabel(text="Answers screen"))

    def go_back(self):
        if self.manager:
            self.manager.current = "home"

    def update_text(self):
        app = MDApp.get_running_app()

        try:
            self.ids.top_bar.title = app.lang.get("answers_title")
        except Exception as e:
            print(f"[AnswersScreen] {e}")