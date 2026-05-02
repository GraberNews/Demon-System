# tools/theme.py

class ThemeManager:
    def __init__(self, app):
        self.app = app

    # Темна тема
    def set_dark(self):
        self.app.theme_cls.theme_style = "Dark"

        # палітра (твоя)
        self.app.theme_cls.primary_palette = "Teal"
        self.app.theme_cls.primary_hue = "800"
        self.app.theme_cls.accent_palette = "Orange"
        self.app.theme_cls.accent_hue = "500"

    # Світла тема
    def set_light(self):
        self.app.theme_cls.theme_style = "Light"

        # та сама палітра
        self.app.theme_cls.primary_palette = "Teal"
        self.app.theme_cls.primary_hue = "800"
        self.app.theme_cls.accent_palette = "Orange"
        self.app.theme_cls.accent_hue = "500"
