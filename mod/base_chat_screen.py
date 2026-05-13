# mod/base_chat_screen.py

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
# Кл. Початок. Імпорт NumericProperty для зв'язку input_y з KV-лейаутом
from kivy.properties import NumericProperty
# Кл. Кінець
# Кл. Початок. Імпорти для діалогу підтвердження очищення чату
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
# Кл. Кінець
# Кл. Початок. Імпорт менеджера API — централізований виклик для всіх чатів
from tools.manage_api import APIManager
# Кл. Кінець

# ─── ChatInputCard

CHAT_KV = '''
<ChatInputCard@MDCard>:
    orientation: "vertical"
    radius: [50]
    elevation: 4
    padding: dp(7)
    spacing: dp(8)
    size_hint_y: None
    height: self.minimum_height
    md_bg_color: app.theme_cls.bg_light
'''

Builder.load_string(CHAT_KV)


# ─── Кольори за темою

def _theme_colors(theme_style):
    dark = theme_style == "Dark"
    return {
        "bot_bg":        (1, 1, 1, 0.07) if dark else (0, 0, 0, 0.06),
        "bot_text":      (0.88, 0.88, 0.88, 1) if dark else (0.15, 0.15, 0.15, 1),
        "bubble_border": (1, 1, 1, 0.18) if dark else (0, 0, 0, 0.14),
        "input_text":    (1, 1, 1, 1)    if dark else (0, 0, 0, 1),
    }


class BaseChatScreen(MDScreen):

    # Кл. Початок. NumericProperty для підняття блоку вводу при відкритті клавіатури.
    # KV прив'язує y блоку вводу до цього значення (в пікселях).
    # При відкритті клавіатури = висота клавіатури, при закритті = 0.
    input_y = NumericProperty(0)
    # Кл. Кінець

    #  КЛАВІАТУРА

    # Кл. Початок. setup_keyboard_handler більше не робить Window.bind —
    # bind/unbind відбувається ТІЛЬКИ в on_enter/on_leave,
    # щоб уникнути подвійного виклику хендлера
    def setup_keyboard_handler(self):
        # Метод залишено для виклику з on_kv_post дочірніх класів.
        # Реальна підписка — в on_enter.
        pass
    # Кл. Кінець

    def on_leave(self):
        Window.unbind(on_keyboard_height=self._on_keyboard_height)

    def on_enter(self):
        Window.bind(on_keyboard_height=self._on_keyboard_height)

    def _on_keyboard_height(self, window, height):
        """
        height > 0 — клавіатура відкрита, height == 0 — закрита.
        Піднімаємо блок вводу (input_area) на висоту клавіатури через input_y.
        """
        # Кл. Початок. Замість padding на root_box — встановлюємо input_y.
        # KV у кожному чат-екрані прив'язує y блоку input_area до root.input_y,
        # завдяки чому весь блок (поле + кнопки) піднімається цілком.
        try:
            self.input_y = int(height)
            if height > 0:
                Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)
        except Exception as e:
            print(f"[BaseChatScreen] keyboard handler: {e}")
        # Кл. Кінець

    #  КОЛІР ТЕКСТУ ПОЛЯ ВВОДУ

    def setup_input_colors(self):
        app = MDApp.get_running_app()
        self._apply_input_color(app.theme_cls.theme_style)
        app.theme_cls.bind(theme_style=self._on_theme_change)
        # Кл. Початок. Підписка на зміну мови для оновлення hint_text поля вводу
        app.lang.bind(current=self._on_lang_change)
        # Кл. Кінець

    def _apply_input_color(self, theme_style):
        cl = _theme_colors(theme_style)
        try:
            self.ids.input_text.foreground_color = cl["input_text"]
            # Кл. Початок. Колір курсора — змінюй CURSOR_COLOR нижче під свій бренд.
            # Формат: (R, G, B, A) у діапазоні 0.0–1.0
            CURSOR_COLOR = (0.13, 0.77, 0.37, 1)   # ← зелений, змінюй тут
            self.ids.input_text.cursor_color = CURSOR_COLOR
            # Кл. Кінець
        except Exception as e:
            print(f"[BaseChatScreen] input color: {e}")

    # Кл. Початок. Оновлення hint_text при зміні мови —
    # показуємо hint тільки якщо поле порожнє і не у фокусі
    def _on_lang_change(self, instance, value):
        self._refresh_hint()

    def _refresh_hint(self):
        app = MDApp.get_running_app()
        try:
            field = self.ids.input_text
            if not field.focus and not field.text:
                field.hint_text = app.lang.get("hint_title")
        except Exception as e:
            print(f"[BaseChatScreen] hint refresh: {e}")
    # Кл. Кінець

    def _on_theme_change(self, instance, value):
        self._apply_input_color(value)
        if hasattr(self, "_top_menu"):
            self.build_top_menu()

    #  ВЕРХНЄ МЕНЮ

    def build_top_menu(self):
        app = MDApp.get_running_app()

        if hasattr(self, "_top_menu"):
            self._top_menu.dismiss()

        items = [
            {
                "text":       app.lang.get("chat_menu_export_pdf"),
                "on_release": lambda: self._top_menu_action("export_pdf"),
            },
            {
                "text":       app.lang.get("chat_menu_export_txt"),
                "on_release": lambda: self._top_menu_action("export_txt"),
            },
            {
                "text":       app.lang.get("chat_menu_clear"),
                "on_release": lambda: self._top_menu_action("clear"),
            },
        ]

        self._top_menu = MDDropdownMenu(
            caller=self.ids.btn_top_menu,
            items=items,
            width_mult=4,
        )

    def open_top_menu(self):
        self.build_top_menu()
        self._top_menu.open()

    def _top_menu_action(self, action):
        self._top_menu.dismiss()
        if action == "export_pdf":
            print(f"[{self.name}] Експорт в PDF")
        elif action == "export_txt":
            print(f"[{self.name}] Експорт в TXT")
        # Кл. Початок. "clear" більше не чистить напряму — відкриває діалог підтвердження
        elif action == "clear":
            self.confirm_clear_chat()
        # Кл. Кінець

    # Кл. Початок. Діалог підтвердження очищення чату.
    # Спочатку перевіряємо чи є повідомлення в chat_box:
    #   — порожній → показуємо інформаційний діалог "Чат порожній" з кнопкою OK
    #   — є повідомлення → показуємо діалог підтвердження з "Очистити" / "Скасувати"
    # _clear_dialog та _empty_dialog зберігаються як атрибути щоб уникнути
    # повторного створення при повторному виклику.
    def confirm_clear_chat(self):
        app = MDApp.get_running_app()

        # Перевірка: чи є хоча б одне повідомлення в чаті
        is_empty = len(self.ids.chat_box.children) == 0

        if is_empty:
            # Якщо діалог "порожній" вже відкритий — не дублюємо
            if hasattr(self, "_empty_dialog") and self._empty_dialog:
                self._empty_dialog.open()
                return

            self._empty_dialog = MDDialog(
                title=app.lang.get("chat_empty_title"),
                buttons=[
                    MDFlatButton(
                        text=app.lang.get("chat_empty_ok"),
                        text_color=app.theme_cls.primary_color,
                        on_release=lambda x: self._close_empty_dialog(),
                    ),
                ],
            )
            self._empty_dialog.open()

        else:
            # Якщо діалог підтвердження вже відкритий — не дублюємо
            if hasattr(self, "_clear_dialog") and self._clear_dialog:
                self._clear_dialog.open()
                return

            self._clear_dialog = MDDialog(
                title=app.lang.get("chat_clear_title"),
                text=app.lang.get("chat_clear_body"),
                buttons=[
                    MDFlatButton(
                        text=app.lang.get("chat_clear_cancel"),
                        text_color=app.theme_cls.primary_color,
                        on_release=lambda x: self._clear_dialog.dismiss(),
                    ),
                    MDFlatButton(
                        text=app.lang.get("chat_clear_confirm"),
                        text_color=app.theme_cls.error_color,
                        on_release=lambda x: self._do_clear_chat(),
                    ),
                ],
            )
            self._clear_dialog.open()

    def _close_empty_dialog(self):
        if hasattr(self, "_empty_dialog") and self._empty_dialog:
            self._empty_dialog.dismiss()
            self._empty_dialog = None

    def _do_clear_chat(self):
        self.ids.chat_box.clear_widgets()
        # Кл. Початок. Очищаємо history разом з UI — щоб AI не пам'ятав старий контекст
        if hasattr(self, "history"):
            self.history.clear()
        # Кл. Кінець
        if hasattr(self, "_clear_dialog") and self._clear_dialog:
            self._clear_dialog.dismiss()
            self._clear_dialog = None
    # Кл. Кінець

    #  ВІДПРАВКА

    # Кл. Початок. send_message — додає повідомлення до history і викликає APIManager.
    # api_provider_name і api_model визначаються в дочірньому класі (pop_ai/gem/test).
    # Поки APIManager обробляє запит — поле вводу заблоковане (is_waiting = True).
    def send_message(self):
        text = self.ids.input_text.text.strip()
        if not text:
            return

        if getattr(self, "is_waiting", False):
            return

        self.is_waiting  = True
        self.typing_widget = None

        self.add_user_message(text)
        self.ids.input_text.text = ""

        if hasattr(self, "history"):
            self.history.append({"role": "user", "content": text})

        # Показуємо "..." поки чекаємо відповіді
        self.typing_widget = self.add_bot_typing()

        # Кл. Початок. Страховий таймаут — скидає is_waiting якщо
        # on_done/on_error не викликались протягом TIMEOUT + 5 секунд
        from tools.manage_api import TIMEOUT as _T
        def _safety_unlock(dt):
            if getattr(self, "is_waiting", False):
                print("[BaseChatScreen] Safety timeout — скидаємо is_waiting")
                self._on_api_error("⚠️ Час очікування вийшов. Спробуй ще раз.")
        Clock.schedule_once(_safety_unlock, _T + 5)
        # Кл. Кінець

        APIManager.ask(
            chat_id  = getattr(self, "api_chat_id", "ai"),
            messages = list(getattr(self, "history", [])),
            on_done  = self._on_api_done,
            on_error = self._on_api_error,
        )

    def _on_api_done(self, text: str):
        """Відповідь отримана — показуємо одним блоком."""
        self.is_waiting = False

        if self.typing_widget:
            try:
                self.ids.chat_box.remove_widget(self.typing_widget)
            except Exception:
                pass
            self.typing_widget = None

        if hasattr(self, "history") and text:
            self.history.append({"role": "assistant", "content": text})

        self.add_bot_message(text)
        self.scroll_to_bottom()

    def _on_api_error(self, msg: str):
        """Помилка — показуємо текст у чаті, розблоковуємо відправку."""
        self.is_waiting = False

        if self.typing_widget:
            try:
                self.ids.chat_box.remove_widget(self.typing_widget)
            except Exception:
                pass
            self.typing_widget = None

        self.add_bot_message(msg)
        self.scroll_to_bottom()
    # Кл. Кінець

    #  БУЛЬБАШКА КОРИСТУВАЧА

    def add_user_message(self, text):
        app   = MDApp.get_running_app()
        cl    = _theme_colors(app.theme_cls.theme_style)
        c     = app.theme_cls.primary_color

        bg    = (c[0], c[1], c[2], 0.40)
        t_col = (0.12, 0.12, 0.12, 1) if app.theme_cls.theme_style == "Light" \
                else (0.92, 0.92, 0.92, 1)

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
            radius=[dp(12), dp(12), dp(1), dp(12)],
        )

        self._draw_border(bubble, cl["bubble_border"], width=dp(0.3))

        label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=t_col,
            size_hint=(None, None),
            adaptive_size=True,
        )

        def _upd_size(inst, val):
            inst.width     = min(val[0], dp(250))
            inst.text_size = (inst.width, None)

        def _upd_bubble(inst, val):
            bubble.width = label.width + dp(24)

        label.bind(texture_size=_upd_size)
        label.bind(width=_upd_bubble)

        bubble.add_widget(label)
        row.add_widget(MDBoxLayout())
        row.add_widget(bubble)

        self.ids.chat_box.add_widget(row)
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.05)

    #  БУЛЬБАШКА БОТА

    def add_bot_message(self, text):
        self._add_bot_bubble(text, typing=False)

    def add_bot_typing(self):
        return self._add_bot_bubble("...", typing=True)

    def _add_bot_bubble(self, text, typing=False):
        app = MDApp.get_running_app()
        cl  = _theme_colors(app.theme_cls.theme_style)

        bubble = MDBoxLayout(
            orientation="vertical",
            padding=[dp(14), dp(10)],
            size_hint_y=None,
            adaptive_height=True,
            size_hint_x=1,
            md_bg_color=cl["bot_bg"],
            radius=[dp(12), dp(12), dp(12), dp(1)],
        )

        self._draw_border(bubble, cl["bubble_border"], width=dp(0.3))

        label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=cl["bot_text"],
            size_hint_y=None,
            adaptive_height=True,
            text_size=(self.width - dp(40), None),
        )

        bubble.add_widget(label)
        self.ids.chat_box.add_widget(bubble)
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.05)

        return bubble if typing else None

    @staticmethod
    def _draw_border(widget, color, width=None):
        from kivy.graphics import Color, Line

        line_w = width if width is not None else dp(0.3)

        def _redraw(*args):
            widget.canvas.after.clear()
            r = widget.radius
            with widget.canvas.after:
                Color(*color)
                Line(
                    rounded_rectangle=(
                        widget.x, widget.y,
                        widget.width, widget.height,
                        r[0], r[1], r[2], r[3],
                        64,
                    ),
                    width=line_w,
                )

        widget.bind(pos=_redraw, size=_redraw)
        _redraw()

    #  SCROLL / NAVIGATION

    def scroll_to_bottom(self):
        self.ids.scroll.scroll_y = 0

    def go_back(self):
        MDApp.get_running_app().go_back()
