[app]

# Основна інформація
title = Demon System
package.name = demonsystem
package.domain = org.demonsystem
version = 1.0

# Точка входу
package.entrypoint = main.py:MainApp

# Директорія проєкту
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ini,ttf,mp3,wav

# Файли та папки для включення
source.include_patterns = main.py, app/, screens/, mod/, tools/, lang/, *.kv
source.exclude_patterns = buildozer.spec, *.pyc, *.pyo, .git*, __pycache__/, .buildozer/, *.kv.bak, *.log, *.spec.backup

# Екран
orientation = portrait
fullscreen = 0

# Дозволи
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE

# Android налаштування
android.api = 33
android.minapi = 24
android.ndk_api = 26
android.enable_androidx = True
android.archs = arm64-v8a                  # Залишили тільки 64-біт для стабільності
# Використовуємо зовнішню SDK

source.exclude_patterns = tools/, buildozer.spec, *.pyc, *.pyo, .git*, __pycache__/, .buildozer/, *.kv.bak, *.log, *.spec.backup

# Використовуємо зовнішню SDK з правильним шляхом до sdkmanager
android.sdkmanager_path = $HOME/android-sdk/cmdline-tools/cmdline-tools/bin

# Залежності
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,sqlite3

# python-for-android
p4a.branch = master

# Налаштування збірки
log_level = 2
warn_on_root = True

# ========================================
# Додаткові параметри
# ========================================

# Для кращої сумісності
#buildozer = 1.5.0
python.version = 3

# Якщо будуть проблеми з великими залежностями
# android.packages = 

# Якщо потрібен presplash екран
# presplash.filename = %(source.dir)s/presplash.png
# presplash.color = #000000
