# app/config_manager.py
from configparser import ConfigParser
import os

class ConfigManager:
    def __init__(self, filename="config.ini"):
        self.filename = filename
        self.config = ConfigParser()

        if os.path.exists(self.filename):
            self.config.read(self.filename)
        else:
            self.create_default()

    def create_default(self):
        self.config["theme"] = {"mode": "Light"}
        self.config["language"] = {"code": "ua"} 
        self.save()

    def save(self):
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)

    def get_theme(self):
        return self.config.get("theme", "mode", fallback="Light")

    def set_theme(self, mode):
        if "theme" not in self.config:
            self.config["theme"] = {}
        self.config["theme"]["mode"] = mode
        self.save()

    # Нові методи для мови
    def get_lang(self):
        return self.config.get("language", "code", fallback="ua")

    def set_lang(self, code):
        if "language" not in self.config:
            self.config["language"] = {}
        self.config["language"]["code"] = code
        self.save()
