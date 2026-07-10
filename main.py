import flet as ft
from logic import AppController


def main(page: ft.Page):

    page.title = "Student Management System"

    page.window_width = 900
    page.window_height = 650


    # Cấu hình trang

    page.padding = 20

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.vertical_alignment = ft.MainAxisAlignment.CENTER



    # Màu nền

    page.bgcolor = "#F5F7FA"



    app = AppController(page)



    app.start()



    # Khung giao diện chính

    container = ft.Container(

        content=app.root,

        width=500,

        padding=30,

        border_radius=15,

        bgcolor="white",

        shadow=ft.BoxShadow(

            blur_radius=15,

            spread_radius=2

        )

    )



    page.add(container)



ft.app(

    target=main,

    view=ft.AppView.WEB_BROWSER

)