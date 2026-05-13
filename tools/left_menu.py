# tools/left_menu.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

# Інфо блок
class DrawerInfoBlock(MDBoxLayout):
    title = StringProperty("")
    text = StringProperty("")

# Конфіг
MENU_ITEMS = {
    "home": [
        ("menu_gem", "star-four-points", "gem"),
        ("menu_ai", "robot", "ai"),
        ("menu_answers", "comment-question", "answers"),
        ("menu_settings", "cog", "settings"),
    ],
    "answers": [
        ("menu_home", "home", "home"),
        ("menu_gem", "star-four-points", "gem"),
        ("menu_ai", "robot", "ai"),
        ("menu_settings", "cog", "settings"),
    ],
    "ai": [
        ("menu_home", "home", "home"),
        ("menu_gem", "star-four-points", "gem"),
        ("menu_test", "test-tube", "test"),
        ("menu_answers", "comment-question", "answers"),
        ("menu_settings", "cog", "settings"),
    ],
    "gem": [
        ("menu_home", "home", "home"),
        ("menu_ai", "robot", "ai"),
        ("menu_test", "test-tube", "test"),
        ("menu_answers", "comment-question", "answers"),
        ("menu_settings", "cog", "settings"),
    ],
    "test": [
        ("menu_home", "home", "home"),
        ("menu_ai", "robot", "ai"),
        ("menu_gem", "star-four-points", "gem"),
        ("menu_answers", "comment-question", "answers"),
        ("menu_settings", "cog", "settings"),
    ],
    "settings": []
}

INFO_BLOCKS = {
    "home": 2,
    "answers": 1,
    "settings": 0
}

class LeftMenu:

    def __init__(self, app):
        self.app = app
        self.drawer = None
        self.menu = None
        self.current_screen = "home"

        # Зберігаємо посилання для оновлення
        self.header_label = None
        self.menu_items = []
        self.info_blocks = []

    # Drawer
    def create_drawer(self):
        self.drawer = MDNavigationDrawer(
            anchor="left",
            width=dp(280)
        )

        scroll = ScrollView()
        self.menu = MDList()
        scroll.add_widget(self.menu)

        self.drawer.add_widget(scroll)

        # перша побудова
        self.build_menu("home")

        return self.drawer

    # Оновлення екрану (БЕЗ rebuild drawer)
    def update(self, drawer, screen_name):
        self.current_screen = screen_name
        self.build_menu(screen_name)

    # Побудова меню
    def build_menu(self, screen_name):
        self.menu.clear_widgets()
        self.menu_items.clear()
        self.info_blocks.clear()

        # Header
        self.header_label = MDLabel(
            text=self.app.lang.get("app_menu_title"),
            font_style="H6",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(16), dp(30), dp(16), dp(10)]
        )
        self.menu.add_widget(self.header_label)

        # Кнопка
        def item(text_key, icon, screen):
            btn = OneLineIconListItem(
                text=self.app.lang.get(text_key),
                on_release=lambda x: self.app.switch_screen(screen)
            )
            btn.add_widget(IconLeftWidget(icon=icon))

            # зберігаємо для оновлення
            btn._text_key = text_key
            self.menu_items.append(btn)

            return btn

        # Меню
        items = MENU_ITEMS.get(screen_name, MENU_ITEMS["home"])

        for text_key, icon, screen in items:
            self.menu.add_widget(item(text_key, icon, screen))

        # Інфоблоки
        count = INFO_BLOCKS.get(screen_name, 2)

        for i in range(count):
            block = DrawerInfoBlock(
                title=self.app.lang.get(f"info_title_{i+1}"),
                text=self.app.lang.get(f"info_text_{i+1}")
            )

            block._index = i + 1
            self.info_blocks.append(block)
            self.menu.add_widget(block)

    # Оновлення мови (без rebuild)
    def refresh(self, drawer, screen_name):
        # Header
        if self.header_label:
            self.header_label.text = self.app.lang.get("app_menu_title")

        # Кнопки
        for btn in self.menu_items:
            btn.text = self.app.lang.get(btn._text_key)

        # Інфоблоки
        for block in self.info_blocks:
            i = block._index
            block.title = self.app.lang.get(f"info_title_{i}")
            block.text = self.app.lang.get(f"info_text_{i}")