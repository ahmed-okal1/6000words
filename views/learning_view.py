import flet as ft
from database import get_user, get_words_by_level, update_user_progress, get_level_progress, set_level_progress, increment_word_error
import os
from gtts import gTTS
import tempfile

def LearningView(page: ft.Page):
    username = page.session.get("username")
    user = get_user(username)
    
    current_level = page.session.get("current_level") or user['current_level']
    
    # Load words
    all_words = get_words_by_level(current_level)
    
    if not all_words:
        return ft.View("/learn", controls=[ft.Text("No words found for this level.")])

    # Get per-level progress
    saved_index = get_level_progress(username, current_level)
    
    # Mutable state
    state = {
        "index": saved_index,
        "answered": False
    }
    
    if state["index"] >= len(all_words):
        state["index"] = 0

    # --- UI Controls ---
    arabic_text = ft.Text(
        all_words[state["index"]]['arabic_word'],
        size=40,
        weight=ft.FontWeight.BOLD,
        color="white",
    )
    
    word_counter = ft.Text(
        f"Level {current_level} - Word {state['index'] + 1}/{len(all_words)}", 
        color="white"
    )
    
    answer_field = ft.TextField(
        label="Type in English",
        border_color="white",
        color="white",
        text_align=ft.TextAlign.CENTER,
        width=300,
        autofocus=True,
    )
    
    feedback_text = ft.Text("", size=20)
    reveal_text = ft.Text("", size=22, color="amber", weight=ft.FontWeight.BOLD, visible=False)
    
    progress_bar = ft.ProgressBar(
        width=300,
        value=(state["index"] + 1) / len(all_words),
        color="green",
        bgcolor="white24"
    )

    # --- Functions ---
    def load_word():
        """Update all UI controls to show the current word."""
        word = all_words[state["index"]]
        arabic_text.value = word['arabic_word']
        arabic_text.update()
        word_counter.value = f"Level {current_level} - Word {state['index'] + 1}/{len(all_words)}"
        word_counter.update()
        progress_bar.value = (state["index"] + 1) / len(all_words)
        progress_bar.update()
        answer_field.value = ""
        answer_field.color = "white"
        answer_field.update()
        answer_field.focus()
        feedback_text.value = ""
        feedback_text.update()
        reveal_text.value = ""
        reveal_text.visible = False
        reveal_text.update()

    def show_word():
        word = all_words[state["index"]]
        reveal_text.value = word['english_word']
        reveal_text.visible = True
        reveal_text.update()

    def play_audio(e):
        word = all_words[state["index"]]
        text = word['english_word']
        try:
            import time
            fname = f"tts_{current_level}_{word['id']}_{int(time.time())}.mp3"
            fpath = os.path.join(tempfile.gettempdir(), fname)
            
            tts = gTTS(text, lang='en')
            tts.save(fpath)
            
            new_player = ft.Audio(src=fpath, autoplay=True)
            page.overlay.append(new_player)
            page.update()
        except Exception as ex:
            print(f"Audio error: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Audio error: {ex}"))
            page.snack_bar.open = True
            page.update()

    def check_answer(e):
        if state["answered"]:
            # Second Enter: advance to next word
            new_index = state["index"] + 1
            update_user_progress(username, current_level, new_index, score_increment=10)
            set_level_progress(username, current_level, new_index)
            
            if new_index >= len(all_words):
                # Level complete!
                feedback_text.value = "🎉 Level Complete!"
                feedback_text.color = "yellow"
                feedback_text.update()
                return
            
            state["index"] = new_index
            state["answered"] = False
            load_word()
            return

        word = all_words[state["index"]]
        user_input = answer_field.value.strip().lower()
        correct_answer = word['english_word'].lower()
        
        if user_input == correct_answer:
            state["answered"] = True
            feedback_text.value = "Correct! ✅  Press Enter to continue"
            feedback_text.color = "green"
            feedback_text.update()
            answer_field.color = "green"
            answer_field.update()
            answer_field.focus()
        else:
            feedback_text.value = "❌ Try Again"
            feedback_text.color = "red"
            feedback_text.update()
            answer_field.focus()
            # Track error
            increment_word_error(username, word['id'])

    answer_field.on_submit = check_answer

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "\\":
            play_audio(None)

    page.on_keyboard_event = on_keyboard

    return ft.View(
        "/learn",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: page.go("/dashboard")),
                                word_counter
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Container(height=40),
                        ft.Text("Translate this word:", color="white70"),
                        arabic_text,
                        ft.Container(height=20),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.VOLUME_UP_ROUNDED,
                                    icon_size=40,
                                    icon_color="cyanAccent",
                                    on_click=play_audio,
                                    tooltip="Listen (or press \\)"
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.VISIBILITY,
                                    icon_size=40,
                                    icon_color="amber",
                                    on_click=lambda e: show_word(),
                                    tooltip="Show English word"
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        reveal_text,
                        ft.Container(height=20),
                        answer_field,
                        ft.Container(height=20),
                        feedback_text,
                        ft.Container(height=40),
                        progress_bar,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=40,
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.DEEP_PURPLE_900, ft.Colors.BLACK],
                )
            )
        ],
        padding=0
    )
