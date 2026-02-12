import flet as ft
from database import get_user, create_user

def LandingView(page: ft.Page):
    
    def login(e):
        if not username_field.value:
            username_field.error_text = "Please enter a username"
            username_field.update()
            return
        
        user = get_user(username_field.value)
        if not user:
            user = create_user(username_field.value)
        
        page.session.set("user_id", user['id'])
        page.session.set("username", user['username'])
        page.client_storage.set("last_username", user['username'])
        page.go("/dashboard")

    username_field = ft.TextField(
        label="Username",
        border_color="white",
        color="white",
        label_style=ft.TextStyle(color="white"),
        cursor_color="white",
        width=300,
        on_submit=login
    )

    return ft.View(
        "/",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "English Mastery",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                            font_family="Roboto"
                        ),
                        ft.Text(
                            "Learn 6000 words in 6 levels",
                            size=16,
                            color=ft.Colors.WHITE70,
                        ),
                        ft.Container(height=40),
                        username_field,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Start Learning",
                            on_click=login,
                            style=ft.ButtonStyle(
                                color="black",
                                bgcolor="white",
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            width=200
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.INDIGO_900, ft.Colors.PURPLE_900],
                )
            )
        ],
        padding=0
    )
