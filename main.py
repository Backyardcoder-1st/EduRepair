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

    # Màu nền web đổi thành màu tối (Xám đen)
    page.bgcolor = "#1A1A1A"

    # 1. Khởi tạo controller lặng lẽ (Chưa kích hoạt giao diện)
    app = AppController(page)

    # 2. Xây dựng khung giao diện chính và ĐƯA VÀO PAGE TRƯỚC
    container = ft.Container(
        content=app.root,
        width=500,
        padding=30,
        border_radius=15,
        bgcolor="#2D2D2D",
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=2
        )
    )
    page.add(container)

    # 3. BÂY GIỜ MỚI CHẠY START để nạp dữ liệu công khai (Sửa triệt để lỗi hộp đỏ)
    app.start()

# Khởi chạy ứng dụng hoàn toàn độc lập ở lề ngoài cùng
if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        assets_dir="assets",
    )