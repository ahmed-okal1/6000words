import flet as ft
import os
import sys
import traceback

def main(page: ft.Page):
    # --- STEP 1: RESILIENT UI SETUP ---
    page.title = "English Mastery - Startup"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    page.scroll = ft.ScrollMode.ALWAYS

    # Use a simple list to show progress
    status_list = ft.Column(spacing=10)
    page.add(
        ft.Text("Diagnostic Startup", size=24, weight="bold"),
        status_list
    )
    
    def report(msg, color="white"):
        status_list.controls.append(ft.Text(msg, color=color, size=12))
        page.update()

    report(f"Python Version: {sys.version}")
    report(f"Executable: {sys.executable}")
    report(f"CWD: {os.getcwd()}")

    # --- STEP 2: LOGGING SETUP ---
    log_file = os.path.join(os.path.expanduser("~"), "english_mastery_debug.log")
    def log_to_file(msg):
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{msg}\n")
        except: pass

    log_to_file("\n--- NEW STARTUP ---")

    # --- STEP 3: DATABASE & VIEWS ---
    try:
        report("Loading database logic...")
        import database
        db_path = database.get_db_path()
        report(f"Target DB Path: {db_path}", "blue")
        
        report("Initializing database...")
        database.init_db()
        
        report("Seeding data...")
        from seed_data import seed_data
        seed_data()
        
        report("Loading views...")
        from views.landing_view import LandingView
        from views.dashboard_view import DashboardView
        from views.learning_view import LearningView
        from views.words_view import WordsView
        from views.difficult_words_view import DifficultWordsView
        report("Logic loaded successfully.", "green")

        # Clear diagnostic UI and start main app
        ft.time.sleep(1) # Let user see the green "Success" for a bit
        page.controls.clear()
        page.padding = 0
        page.scroll = None
        page.title = "English Mastery"
        
    except Exception as e:
        err = f"CRITICAL ERROR: {str(e)}\n\n{traceback.format_exc()}"
        report(err, "red")
        log_to_file(err)
        return

    # --- STEP 4: ROUTING ---
    def route_change(route):
        try:
            page.views.clear()
            if page.route == "/":
                page.views.append(LandingView(page))
            elif page.route == "/dashboard":
                page.views.append(DashboardView(page))
            elif page.route == "/learn":
                page.views.append(LearningView(page))
            elif page.route == "/words":
                page.views.append(WordsView(page))
            elif page.route == "/difficult":
                page.views.append(DifficultWordsView(page))
            page.update()
        except Exception as e:
            report(f"Routing Error: {e}", "red")

    page.on_route_change = route_change
    page.on_view_pop = lambda _: [page.views.pop(), page.go(page.views[-1].route)]
    
    # Start Navigation
    try:
        last_username = page.client_storage.get("last_username")
        if last_username:
            page.session.set("username", last_username)
            page.go("/dashboard")
        else:
            page.go("/")
    except:
        page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
