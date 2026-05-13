# app/config_manager.py
from configparser import ConfigParser
import os

class ConfigManager:
    def __init__(self):
        # Безпечний шлях для Android та Desktop
        # user_data_dir — правильна директорія для даних додатку на всіх платформах
        try:
            from kivy.app import App
            app = App.get_running_app()
            data_dir = app.user_data_dir if app else "."
        except Exception:
            data_dir = "."

        self.filename = os.path.join(data_dir, "config.ini")
        self.config = ConfigParser()

        if os.path.exists(self.filename):
            self.config.read(self.filename, encoding="utf-8")
        else:
            self.create_default()

    def create_default(self):
        self.config["theme"] = {"mode": "Light"}
        self.config["language"] = {"code": "ua"}
        self.save()

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f"[ConfigManager] Не вдалося зберегти config: {e}")

    def get_theme(self):
        return self.config.get("theme", "mode", fallback="Light")

    def set_theme(self, mode):
        if "theme" not in self.config:
            self.config["theme"] = {}
        self.config["theme"]["mode"] = mode
        self.save()

    def get_lang(self):
        return self.config.get("language", "code", fallback="ua")

    def set_lang(self, code):
        if "language" not in self.config:
            self.config["language"] = {}
        self.config["language"]["code"] = code
        self.save()
