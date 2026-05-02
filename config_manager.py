# app/config_manager.py

from configparser import ConfigParser
import os


class ConfigManager:
    def __init__(self, filename="config.ini"):
        self.filename = filename
        self.config = ConfigParser()

        # якщо файл існує → читаємо
        if os.path.exists(self.filename):
            self.config.read(self.filename)
        else:
            self.create_default()

    # створення дефолтного конфігу
    def create_default(self):
        self.config["theme"] = {
            "mode": "Light"  # Light або Dark
        }

        self.save()

    # зберегти файл
    def save(self):
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)

    # отримати тему
    def get_theme(self):
        return self.config.get("theme", "mode", fallback="Light")

    # зберегти тему
    def set_theme(self, mode):
        if "theme" not in self.config:
            self.config["theme"] = {}

        self.config["theme"]["mode"] = mode
        self.save()