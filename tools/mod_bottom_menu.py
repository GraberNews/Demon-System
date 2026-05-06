# tools/mod_bottom_menu.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

KV = '''
<BottomMenu>:
    size_hint: 1, 1
    auto_dismiss: False
    background: ""
    background_color: 0, 0, 0, 0

    FloatLayout:

        # ===== OVERLAY
        MDBoxLayout:
            size_hint: 1, 1
            md_bg_color: 0, 0, 0, 0.1
            on_touch_down: root.close_on_touch(*args)

        # ===== PANEL
        MDBoxLayout:
            id: panel
            orientation: "vertical"
            size_hint: 1, None
            height: self.minimum_height
            pos_hint: {"x": 0, "y": -1}
            padding: dp(10)
            spacing: dp(10)
            md_bg_color: app.theme_cls.bg_light
            radius: [90, 90, 0, 0]

            # ===== TITLE
            MDLabel:
                id: title_label
                text: app.lang.get("bott_menu_title")
                halign: "center"
                font_style: "H6"
                size_hint_y: None
                height: self.texture_size[1] + dp(10)

            # ===== CONTENT
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

    def __init__(self, items=None, on_select=None, **kwargs):
        super().__init__(**kwargs)

        self.on_select = on_select
        self.items = items or []

        self.build_menu()

        # ===== LANGUAGE BIND
        app = MDApp.get_running_app()
        app.lang.bind(current=self.on_language_change)

    # ===== BUILD MENU
    def build_menu(self):
        app = MDApp.get_running_app()

        self.ids.content.clear_widgets()

        for item_data in self.items:
            icon = item_data.get("icon")
            key = item_data.get("key")
            action = item_data.get("action")

            text = app.lang.get(key)

            # 🔥 FIX lambda (щоб не було багів із замиканням)
            def callback(act):
                return lambda x: self.on_item(act)

            item = OneLineIconListItem(
                text=text,
                on_release=callback(action)
            )

            item.add_widget(IconLeftWidget(icon=icon))
            self.ids.content.add_widget(item)

    # ===== LANGUAGE CHANGE
    def on_language_change(self, instance, value):
        self.update_text()

    def update_text(self):
        app = MDApp.get_running_app()

        # TITLE
        self.ids.title_label.text = app.lang.get("bott_menu_title")

        # REBUILD MENU
        self.build_menu()

    # ===== OPEN
    def open(self, *args):
        super().open(*args)

        self.ids.panel.pos_hint = {"x": 0, "y": -1}

        Animation(
            pos_hint={"x": 0, "y": 0},
            d=0.25,
            t="out_quad"
        ).start(self.ids.panel)

    # ===== CLOSE
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

    # ===== TAP OUTSIDE
    def close_on_touch(self, instance, touch):
        if not self.ids.panel.collide_point(*touch.pos):
            self.dismiss()
            return True
        return False

    # ===== CLICK
    def on_item(self, action):
        if self.on_select:
            self.on_select(action)

        self.dismiss()