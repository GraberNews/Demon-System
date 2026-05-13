# tools/manage_api.py

import threading
import re as _re
import queue as _queue
from kivy.clock import Clock

_html_re = _re.compile(r"<[^>]+>")

def _strip_html(text: str) -> str:
    return _html_re.sub("", text).strip()


# ═══════════════════════════════════════════════════════════════════════
# НАЛАШТУВАННЯ ЧАСУ ОЧІКУВАННЯ
# ═══════════════════════════════════════════════════════════════════════
TIMEOUT = 20   # секунд; змінюй тут


# ═══════════════════════════════════════════════════════════════════════
# ЧАТ: AI  (pop_ai.py)
# ═══════════════════════════════════════════════════════════════════════
AI_PROVIDER = "Yqcloud"   # ← провайдер AI чату
AI_MODEL    = "gpt-4o-mini"      # ← модель AI чату
# ═══════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════
# ЧАТ: GEM  (pop_gem.py)
# ═══════════════════════════════════════════════════════════════════════
GEM_PROVIDER = "Yqcloud"         # ← провайдер Gem чату
GEM_MODEL    = "gpt-4o"          # ← модель Gem чату
# ═══════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════
# ЧАТ: TEST  (pop_test.py)
# ═══════════════════════════════════════════════════════════════════════
TEST_PROVIDER = "Yqcloud"  # ← провайдер Test чату
TEST_MODEL    = "gpt-3.5-turbo"  # ← модель Test чату
# ═══════════════════════════════════════════════════════════════════════


_CHAT_CONFIG = {
    "ai":   (AI_PROVIDER,   AI_MODEL),
    "gem":  (GEM_PROVIDER,  GEM_MODEL),
    "test": (TEST_PROVIDER, TEST_MODEL),
}


class APIManager:

    @classmethod
    def ask(cls, chat_id: str, messages: list, on_done, on_error):
        provider_name, model = _CHAT_CONFIG.get(chat_id, (AI_PROVIDER, AI_MODEL))
        thread = threading.Thread(
            target=cls._run,
            args=(provider_name, model, messages, on_done, on_error),
            daemon=True,
        )
        thread.start()

    @classmethod
    def get_provider_name(cls, chat_id: str) -> str:
        return _CHAT_CONFIG.get(chat_id, (AI_PROVIDER,))[0]

    @classmethod
    def _run(cls, provider_name, model, messages, on_done, on_error):
        try:
            import g4f
            import g4f.Provider as _pm
        except Exception as e:
            Clock.schedule_once(lambda dt: on_error(f"Помилка імпорту g4f: {e}"), 0)
            return

        provider = getattr(_pm, provider_name, None)
        if provider is None:
            Clock.schedule_once(
                lambda dt: on_error(
                    f"Провайдер '{provider_name}' не знайдений.\n"
                    f"Перевір назву в списку g4f.Provider."
                ), 0
            )
            return

        result_q = _queue.Queue()

        def _worker():
            tokens = []
            try:
                response = g4f.ChatCompletion.create(
                    model    = model,
                    provider = provider,
                    messages = messages,
                    stream   = True,
                )
                if response is None:
                    result_q.put(("empty", None))
                    return
                for chunk in response:
                    if chunk is None:
                        continue
                    chunk_str = _strip_html(str(chunk))
                    if not chunk_str:
                        continue
                    if chunk_str.startswith("{'error'") or \
                       chunk_str.startswith('{"error"'):
                        result_q.put(("error", chunk_str))
                        return
                    tokens.append(chunk_str)
                if tokens:
                    result_q.put(("ok", "".join(tokens)))
                else:
                    result_q.put(("empty", None))
            except Exception as e:
                result_q.put(("error", str(e)))

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        t.join(timeout=TIMEOUT)

        if t.is_alive():
            msg = (
                f"⏱ '{provider_name}' не відповів за {TIMEOUT}с.\n"
                f"Перевір з'єднання або зміни провайдера."
            )
            Clock.schedule_once(lambda dt: on_error(msg), 0)
            return

        try:
            status, data = result_q.get_nowait()
        except _queue.Empty:
            Clock.schedule_once(
                lambda dt: on_error(f"'{provider_name}': немає відповіді."), 0
            )
            return

        if status == "ok":
            print(f"[APIManager] Успіх: {provider_name} / {model}")
            Clock.schedule_once(lambda dt: on_done(data), 0)

        elif status == "empty":
            msg = (
                f"📭 '{provider_name}' повернув порожню відповідь.\n"
                f"Спробуй ще раз або зміни провайдера."
            )
            Clock.schedule_once(lambda dt: on_error(msg), 0)

        else:
            print(f"[APIManager] Error: {provider_name}/{model}: {data}")
            Clock.schedule_once(
                lambda dt: on_error(f"⚠️ '{provider_name}':\n{data}"), 0
            )
