import flet as ft
from logic import AppController
import os


def main(page: ft.Page):

    page.title = "Student Management System"

    page.window_width = 900
    page.window_height = 650


    page.theme_mode = ft.ThemeMode.LIGHT

    page.bgcolor = ft.Colors.WHITE


    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    app = AppController(page)


    page.add(app.root)


    app.start()



# Render will provide an environment variable called 'PORT'.
# If it's not found (like when you run it locally), it defaults to 8080.
port = int(os.getenv("PORT", 8080))

ft.app(
    target=main,
    host="0.0.0.0",  # Tells Flet to accept connections from the public web
    port=port
)