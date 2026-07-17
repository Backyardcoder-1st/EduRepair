import flet as ft
from logic import AppController
import mimetypes

mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")


def main(page: ft.Page):
    page.title = "Student Management System"

    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    app = AppController(page)

    page.add(app.root)

    # chỉ gọi nếu logic.py có hàm start()
    if hasattr(app, "start"):
        app.start()


if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER
    )