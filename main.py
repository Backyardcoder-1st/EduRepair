import flet as ft
from logic import AppController
import os
import mimetypes

mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")

def main(page: ft.Page):
    page.title = "Student Management System"
    page.window_width = 900
    page.window_height = 650

    # Cấu hình trang theo style Light-Theme của bạn
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Khởi tạo lớp điều khiển ứng dụng
    app = AppController(page)

    # Thêm thành phần đồ họa gốc vào giao diện trước
    page.add(app.root)

    # Kích hoạt tải dữ liệu nền
    app.start()


if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER
    )