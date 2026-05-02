# tools/left_menu.py

from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


# 🔹 Інфо блок
class DrawerInfoBlock(MDBoxLayout):
    title = StringProperty("")
    text = StringProperty("")


# 🔹 Конфіг меню
MENU_ITEMS = {
    "home": [
        ("Gem", "star-four-points", "gem"),
        ("AI", "robot", "ai"),
        ("Answers", "comment-question", "answers"),
        ("Налаштування", "cog", "settings"),
    ],
    "answers": [
        ("Home", "home", "home"),
        ("Gem", "star-four-points", "gem"),
        ("AI", "robot", "ai"),
        ("Налаштування", "cog", "settings"),
    ],
    "settings": []  # ❌ меню відсутнє
}


# 🔹 Кількість інфоблоків
INFO_BLOCKS = {
    "home": 2,
    "answers": 1,
    "settings": 0
}


class LeftMenu:

    def __init__(self, app):
        self.app = app
        self.drawer_menu = None

    # 📂 Drawer
    def create_drawer(self):
        drawer = MDNavigationDrawer(
            anchor="left",
            width=dp(280)
        )

        self.drawer_menu = self.build_menu("home")
        drawer.add_widget(self.drawer_menu)

        return drawer

    # 🔄 Оновлення
    def update(self, drawer, screen_name):
        drawer.clear_widgets()
        self.drawer_menu = self.build_menu(screen_name)
        drawer.add_widget(self.drawer_menu)

    # 🧠 Побудова меню
    def build_menu(self, screen_name):
        scroll = ScrollView()
        menu = MDList()

        # 🔝 Header
        menu.add_widget(
            MDLabel(
                text="Demon System",
                font_style="H6",
                size_hint_y=None,
                height=dp(60),
                padding=[dp(16), dp(30), dp(16), dp(10)]
            )
        )

        # 🔘 Кнопка
        def item(text, icon, screen):
            btn = OneLineIconListItem(
                text=text,
                on_release=lambda x: self.app.switch_screen(screen)
            )
            btn.add_widget(IconLeftWidget(icon=icon))
            return btn

        # 📌 Беремо конфіг
        items = MENU_ITEMS.get(screen_name, MENU_ITEMS["home"])

        for text, icon, screen in items:
            menu.add_widget(item(text, icon, screen))

        # 📌 Інфоблоки
        count = INFO_BLOCKS.get(screen_name, 2)

        for i in range(count):
            menu.add_widget(DrawerInfoBlock(
                title=f"Інформація {i+1}",
                text="Це інформаційний блок. Тут буде динамічний контент."
            ))

        scroll.add_widget(menu)
        return scroll
