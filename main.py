import flet as ft
from logic import AppController
import mimetypes
import os

# Point Google Auth directly to your service account key file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Set upload secret key
os.environ["FLET_SECRET_KEY"] = "edurepair_secret_key_123"
os.makedirs("uploads", exist_ok=True)

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

    if hasattr(app, "start"):
        app.start()

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        upload_dir="uploads",
        view=ft.AppView.WEB_BROWSER
    )