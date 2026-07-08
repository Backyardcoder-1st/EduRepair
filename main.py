import flet as ft
from logic import AppController  # Assumes your logic file is named logic.py


async def main(page: ft.Page):
    page.title = "HỆ THỐNG QUẢN LÝ HỌC SINH"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    controller = AppController(page)
    page.add(controller.root)

    await controller.show_login()


# This forces Flet to open a native Windows desktop application window instantly
ft.app(target=main, view=ft.AppView.FLET_APP)