import flet as ft


def main(page: ft.Page):
    page.title = "EduRepair Portal"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Text("EduRepair System Coming Soon!", size=24, weight=ft.FontWeight.BOLD)
    )


if __name__ == "__main__":
    ft.app(target=main)