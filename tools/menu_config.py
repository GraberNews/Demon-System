# tools/menu_config.py

# ===== AI CHAT MENU
def get_ai_menu():
    return [
        {"icon": "format-list-bulleted", "key": "bott_answers_menu", "action": "answers"},
        {"icon": "file", "key": "bott_aifiles_menu", "action": "files"},
        {"icon": "robot", "key": "bott_gem_menu", "action": "gem"},
        {"icon": "test-tube", "key": "bott_test_menu", "action": "test"},
        {"icon": "database", "key": "bott_ai_db_menu", "action": "db"},
    ]


# ===== GEM CHAT MENU
def get_gem_menu():
    return [
        {"icon": "format-list-bulleted", "key": "bott_answers_menu", "action": "answers"},
        {"icon": "file", "key": "bott_gemfiles_menu", "action": "files"},
        {"icon": "robot", "key": "bott_ai_menu", "action": "ai"},
        {"icon": "test-tube", "key": "bott_test_menu", "action": "test"},
        {"icon": "database", "key": "bott_gem_db_menu", "action": "db"},
    ]


# ===== TEST CHAT MENU
def get_test_menu():
    return [
        {"icon": "format-list-bulleted", "key": "bott_answers_menu", "action": "answers"},
        {"icon": "file", "key": "bott_testfiles_menu", "action": "files"},
        {"icon": "robot", "key": "bott_ai_menu", "action": "ai"},
        {"icon": "robot", "key": "bott_gem_menu", "action": "gem"},
        {"icon": "database", "key": "bott_test_db_menu", "action": "db"},
    ]


# ===== 🔥 ГОЛОВНА ФУНКЦІЯ (ОБОВ'ЯЗКОВО!)
def get_menu_items(menu_type):
    if menu_type == "ai":
        return get_ai_menu()

    if menu_type == "gem":
        return get_gem_menu()

    if menu_type == "test":
        return get_test_menu()

    # fallback
    return get_ai_menu()