import os
import datetime

# Global dictionary to act as a reliable session store across all environments
SESSION_FALLBACK = {}

def log_session(msg):
    log_file = os.path.join(os.path.expanduser("~"), "english_mastery_debug.log")
    try:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [SESSION_UTILS] {msg}\n")
    except: pass

def set_session(page, key, value):
    """Sets a session value using memory fallback and native methods."""
    log_session(f"SET {key}={value}")
    
    # Always store in memory fallback (most reliable)
    SESSION_FALLBACK[key] = value
    
    try:
        # Standard Flet (Antigravity)
        page.session.set(key, value)
        log_session(f"Saved {key} via .set()")
    except:
        try:
            # Native dict-style
            page.session[key] = value
            log_session(f"Saved {key} via []")
        except:
            log_session(f"Native session storage failed for {key}, relying on MEMORY ONLY")

def get_session(page, key):
    """Gets a session value from memory fallback or native methods."""
    log_session(f"GET {key}")
    
    # 1. Check memory fallback first
    if key in SESSION_FALLBACK:
        val = SESSION_FALLBACK[key]
        log_session(f"Retrieved {key}={val} from MEMORY")
        return val
        
    # 2. Try native methods if not in memory
    try:
        val = page.session.get(key)
        log_session(f"Retrieved {key}={val} via .get()")
        return val
    except:
        try:
            val = page.session[key]
            log_session(f"Retrieved {key}={val} via []")
            return val
        except:
            log_session(f"All retrieval methods failed for {key}")
            return None

def clear_session():
    """Clear the memory fallback."""
    SESSION_FALLBACK.clear()
    log_session("Memory session cleared.")
