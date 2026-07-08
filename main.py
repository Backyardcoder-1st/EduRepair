import flet as ft
from logic import AppController  # Make sure this matches your logic file name


async def main(page: ft.Page):
    # 1. Set up basic page properties
    page.title = "EduRepair"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 2. Initialize the controller
    controller = AppController(page)

    # 3. Add the root container to the screen layout
    page.add(controller.root)

    # 4. FIX: Use 'await' because show_login() is now an async function!
    await controller.show_login()


# Run the application as a web-compatible web app
ft.app(target=main)