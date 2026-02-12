import flet as ft
from database import get_words_by_level, delete_word, delete_words_bulk, update_word

def WordsView(page: ft.Page):
    # State
    state = {
        "current_level": 1,
        "selected_ids": set(),
    }

    # --- UI Controls ---
    words_list = ft.ListView(expand=True, spacing=2, padding=10)
    select_all_checkbox = ft.Checkbox(label="Select All", value=False)
    delete_btn = ft.ElevatedButton(
        "Delete Selected",
        icon=ft.Icons.DELETE,
        bgcolor=ft.Colors.RED_900,
        color="white",
        visible=False,
    )
    word_count_text = ft.Text("", color="white70", size=14)

    # --- Functions ---
    def load_words(is_initial=False):
        words = get_words_by_level(state["current_level"])
        state["selected_ids"].clear()
        select_all_checkbox.value = False

        words_list.controls.clear()
        for w in words:
            cb = ft.Checkbox(
                value=False,
                data=w['id'],
                on_change=on_word_checked
            )
            row = ft.Container(
                content=ft.Row(
                    [
                        cb,
                        ft.Text(w['english_word'], size=16, color="white", width=150, weight=ft.FontWeight.W_500),
                        ft.Text(w['arabic_word'], size=16, color="cyanAccent", width=150),
                        ft.IconButton(
                            ft.Icons.EDIT,
                            icon_color="amber",
                            icon_size=20,
                            data=w,
                            on_click=lambda e: open_edit_dialog(e.control.data),
                            tooltip="Edit"
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color="red",
                            icon_size=20,
                            data=w['id'],
                            on_click=lambda e: confirm_delete_single(e.control.data),
                            tooltip="Delete"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                bgcolor=ft.Colors.WHITE10,
                border_radius=8,
                padding=ft.Padding(left=10, right=10, top=4, bottom=4),
            )
            words_list.controls.append(row)

        word_count_text.value = f"{len(words)} words in Level {state['current_level']}"
        delete_btn.visible = False
        
        if not is_initial:
            select_all_checkbox.update()
            word_count_text.update()
            delete_btn.update()
            words_list.update()

    def on_word_checked(e):
        word_id = e.control.data
        if e.control.value:
            state["selected_ids"].add(word_id)
        else:
            state["selected_ids"].discard(word_id)
        update_delete_btn_visibility()

    def update_delete_btn_visibility():
        delete_btn.visible = len(state["selected_ids"]) > 0
        if state["selected_ids"]:
            delete_btn.text = f"Delete Selected ({len(state['selected_ids'])})"
        delete_btn.update()

    def on_select_all(e):
        words = get_words_by_level(state["current_level"])
        state["selected_ids"].clear()
        if e.control.value:
            for w in words:
                state["selected_ids"].add(w['id'])
        # Update all checkboxes in the list
        for row_container in words_list.controls:
            cb = row_container.content.controls[0]  # First control is Checkbox
            cb.value = e.control.value
        words_list.update()
        update_delete_btn_visibility()

    select_all_checkbox.on_change = on_select_all

    def confirm_delete_single(word_id):
        def do_delete(e):
            delete_word(word_id)
            page.close(dlg)
            load_words()

        dlg = ft.AlertDialog(
            title=ft.Text("Delete Word"),
            content=ft.Text("Are you sure you want to delete this word?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close(dlg)),
                ft.TextButton("Delete", on_click=do_delete),
            ],
        )
        page.open(dlg)
        page.update()

    def confirm_delete_bulk(e):
        count = len(state["selected_ids"])
        def do_delete(e):
            delete_words_bulk(list(state["selected_ids"]))
            page.close(dlg)
            load_words()

        dlg = ft.AlertDialog(
            title=ft.Text("Delete Words"),
            content=ft.Text(f"Are you sure you want to delete {count} selected words?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close(dlg)),
                ft.TextButton("Delete All", on_click=do_delete),
            ],
        )
        page.open(dlg)
        page.update()

    delete_btn.on_click = confirm_delete_bulk

    def open_edit_dialog(word_data):
        en_field = ft.TextField(value=word_data['english_word'], label="English", width=250)
        ar_field = ft.TextField(value=word_data['arabic_word'], label="Arabic", width=250)

        def save_edit(e):
            update_word(word_data['id'], en_field.value.strip(), ar_field.value.strip())
            page.close(dlg)
            load_words()

        dlg = ft.AlertDialog(
            title=ft.Text("Edit Word"),
            content=ft.Column([en_field, ar_field], tight=True, spacing=10),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close(dlg)),
                ft.TextButton("Save", on_click=save_edit),
            ],
        )
        page.open(dlg)
        page.update()

    def on_level_tab_change(e):
        state["current_level"] = e.control.selected_index + 1
        load_words()

    # --- Level Tabs ---
    level_tabs = ft.Tabs(
        selected_index=0,
        on_change=on_level_tab_change,
        tabs=[ft.Tab(text=f"Level {i}") for i in range(1, 7)],
        indicator_color="cyanAccent",
        label_color="white",
        unselected_label_color="white54",
    )

    # Load initial data (no .update() calls since controls aren't on page yet)
    load_words(is_initial=True)

    return ft.View(
        "/words",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: page.go("/dashboard")),
                                ft.Text("Word Manager", size=24, weight=ft.FontWeight.BOLD, color="white"),
                            ],
                        ),
                        level_tabs,
                        ft.Container(height=10),
                        ft.Row(
                            [
                                select_all_checkbox,
                                word_count_text,
                                delete_btn,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=5),
                        words_list,
                    ],
                ),
                padding=20,
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
