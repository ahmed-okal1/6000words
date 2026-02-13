import flet as ft
from database import get_difficult_words, remove_from_difficult
import os
from gtts import gTTS
import tempfile

def DifficultWordsView(page: ft.Page):
    username = page.session.get("username")
    
    # Load difficult words
    difficult_words = get_difficult_words(username, min_errors=3)
    
    if not difficult_words:
        return ft.View(
            "/difficult",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: page.go("/dashboard")),
                                    ft.Text("Difficult Words", size=24, weight=ft.FontWeight.BOLD, color="white"),
                                ],
                            ),
                            ft.Container(height=80),
                            ft.Icon(ft.Icons.CELEBRATION, size=80, color="amber"),
                            ft.Container(height=20),
                            ft.Text("No difficult words! 🎉", size=24, color="greenAccent", weight=ft.FontWeight.BOLD),
                            ft.Text("Keep up the great work!", size=16, color="white70"),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=40,
                    expand=True,
                    gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                        colors=[ft.Colors.BLUE_GREY_900, ft.Colors.BLACK],
                    )
                )
            ],
            padding=0,
        )

    # Mutable state
    state = {
        "index": 0,
        "answered": False,
        "words": difficult_words,
    }

    # --- UI Controls ---
    count_text = ft.Text(
        f"Word {1}/{len(difficult_words)} • {len(difficult_words)} difficult words",
        color="white70"
    )

    arabic_text = ft.Text(
        difficult_words[0]['arabic_word'],
        size=40,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    error_badge = ft.Text(
        f"Wrong {difficult_words[0]['error_count']} times",
        size=14,
        color="redAccent",
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

    # --- Functions ---
    def load_word():
        if state["index"] >= len(state["words"]):
            # All done!
            feedback_text.value = "🎉 All difficult words cleared!"
            feedback_text.color = "greenAccent"
            feedback_text.update()
            answer_field.visible = False
            answer_field.update()
            arabic_text.value = ""
            arabic_text.update()
            error_badge.value = ""
            error_badge.update()
            count_text.value = "All done!"
            count_text.update()
            reveal_text.visible = False
            reveal_text.update()
            return

        word = state["words"][state["index"]]
        arabic_text.value = word['arabic_word']
        arabic_text.update()
        error_badge.value = f"Wrong {word['error_count']} times"
        error_badge.update()
        count_text.value = f"Word {state['index'] + 1}/{len(state['words'])} • {len(state['words'])} difficult words"
        count_text.update()
        answer_field.value = ""
        answer_field.color = "white"
        answer_field.visible = True
        answer_field.update()
        answer_field.focus()
        feedback_text.value = ""
        feedback_text.update()
        reveal_text.value = ""
        reveal_text.visible = False
        reveal_text.update()

    def show_word():
        if state["index"] < len(state["words"]):
            word = state["words"][state["index"]]
            reveal_text.value = word['english_word']
            reveal_text.visible = True
            reveal_text.update()

    def play_audio(e):
        if state["index"] >= len(state["words"]):
            return
        word = state["words"][state["index"]]
        text = word['english_word']
        try:
            import time
            fname = f"tts_diff_{word['id']}_{int(time.time())}.mp3"
            fpath = os.path.join(tempfile.gettempdir(), fname)
            tts = gTTS(text, lang='en')
            tts.save(fpath)
            new_player = ft.Audio(src=fpath, autoplay=True)
            page.overlay.append(new_player)
            page.update()
        except Exception as ex:
            print(f"Audio error: {ex}")

    def check_answer(e):
        if state["index"] >= len(state["words"]):
            return

        if state["answered"]:
            # Second Enter: move to next
            state["index"] += 1
            state["answered"] = False
            load_word()
            return

        word = state["words"][state["index"]]
        user_input = answer_field.value.strip().lower()
        correct_answer = word['english_word'].lower()

        if user_input == correct_answer:
            state["answered"] = True
            # Remove from difficult words list
            remove_from_difficult(username, word['id'])
            feedback_text.value = "Correct! ✅ Removed from difficult words. Press Enter to continue"
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

    answer_field.on_submit = check_answer

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "\\":
            play_audio(None)

    page.on_keyboard_event = on_keyboard

    return ft.View(
        "/difficult",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: page.go("/dashboard")),
                                ft.Text("Difficult Words", size=24, weight=ft.FontWeight.BOLD, color="white"),
                            ],
                        ),
                        count_text,
                        ft.Container(height=30),
                        ft.Text("Translate this word:", color="white70"),
                        arabic_text,
                        error_badge,
                        ft.Container(height=15),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.VOLUME_UP_ROUNDED,
                                    icon_size=40,
                                    icon_color="cyanAccent",
                                    on_click=play_audio,
                                    tooltip="Listen"
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
                        ft.Container(height=15),
                        answer_field,
                        ft.Container(height=15),
                        feedback_text,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=40,
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[ft.Colors.BLUE_GREY_900, ft.Colors.BLACK],
                )
            )
        ],
        padding=0,
    )
