import os
import datetime

def log_session(msg):
    log_file = os.path.join(os.path.expanduser("~"), "english_mastery_debug.log")
    try:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [SESSION_UTILS] {msg}\n")
    except: pass

def set_session(page, key, value):
    """Sets a session value using the best available method for the environment."""
    log_session(f"Setting {key}={value}")
    try:
        # Standard Flet (Antigravity)
        page.session.set(key, value)
        log_session(f"Set {key} via .set()")
    except Exception as e:
        log_session(f".set() failed: {e}")
        try:
            # Built app environment
            page.session[key] = value
            log_session(f"Set {key} via []")
        except Exception as e2:
            log_session(f"[] failed: {e2}")

def get_session(page, key):
    """Gets a session value using the best available method for the environment."""
    log_session(f"Getting {key}")
    try:
        # Standard Flet (Antigravity)
        val = page.session.get(key)
        log_session(f"Got {key}={val} via .get()")
        return val
    except Exception as e:
        log_session(f".get() failed: {e}")
        try:
            # Built app environment
            val = page.session[key]
            log_session(f"Got {key}={val} via []")
            return val
        except Exception as e2:
            log_session(f"[] failed: {e2}")
            return None
