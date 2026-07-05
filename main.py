import flet as ft
from logic import AppController

def main(page: ft.Page):
    page.title = "Student Management System"
    page.window_width = 900
    page.window_height = 650
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    app = AppController(page)
    app.show_login()

    page.add(app.root)

if __name__ == "__main__":
    ft.app(target=main)