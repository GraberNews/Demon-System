# tools/bottom_menu.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.uix.modalview import ModalView

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

KV = '''
<BottomMenu>:
    size_hint: 1, 1
    auto_dismiss: False
    background: ""

    FloatLayout:

        # затемнення
        MDBoxLayout:
            size_hint: 1, 1
            md_bg_color: 0, 0, 0, 0.4
            on_touch_down: root.close_on_touch(*args)

        # панель
        MDBoxLayout:
            id: panel
            orientation: "vertical"
            size_hint: 1, None
            height: self.minimum_height
            pos_hint: {"x": 0, "y": -1}
            padding: dp(10)
            spacing: dp(10)
            md_bg_color: app.theme_cls.bg_light
            radius: [20, 20, 0, 0]

            MDLabel:
                text: "Menu"
                halign: "center"
                md_bg_color: 0, 0, 0, 0.4
                font_style: "H6"
                size_hint_y: None
                height: self.texture_size[1] + dp(10)

            ScrollView:
                size_hint_y: None
                height: min(self.parent.height * 1.8, self.children[0].minimum_height)

                MDBoxLayout:
                    id: content
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
'''

Builder.load_string(KV)


class BottomMenu(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_menu()

    # ---------- меню ----------
    def build_menu(self):
        items = [
            ("file", "File"),
            ("image", "Image"),
            ("delete", "Clear chat"),
            ("database", "Database"),
            ("cog", "Settings"),
        ]

        for icon, text in items:
            item = OneLineIconListItem(
                text=text,
                on_release=lambda x, t=text: self.on_item(t)
            )
            item.add_widget(IconLeftWidget(icon=icon))
            self.ids.content.add_widget(item)

    # ---------- open ----------
    def open(self, *args):
        super().open(*args)

        self.ids.panel.pos_hint = {"x": 0, "y": -1}

        Animation(
            pos_hint={"x": 0, "y": 0},
            d=0.1,
            t="out_quad"
        ).start(self.ids.panel)

    # ---------- dismiss ----------
    def dismiss(self, *args):
        anim = Animation(
            pos_hint={"x": 0, "y": -1},
            d=0.2,
            t="in_quad"
        )

        anim.bind(on_complete=self._finish_dismiss)
        anim.start(self.ids.panel)

    def _finish_dismiss(self, *args):
        super().dismiss()

    # ---------- тап поза ----------
    def close_on_touch(self, instance, touch):
        if not self.ids.panel.collide_point(*touch.pos):
            self.dismiss()
            return True
        return False

    # ---------- click ----------
    def on_item(self, text):
        print(f"Clicked: {text}")
        self.dismiss()


# ================= TEST APP =================

KV_APP = '''
MDScreen:

    MDFloatingActionButton:
        icon: "plus"
        pos_hint: {"center_x": 0.1, "center_y": 0.1}
        on_release: app.open_menu()
'''


class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV_APP)

    def open_menu(self):
        BottomMenu().open()


if __name__ == "__main__":
    TestApp().run()