import flet as ft
import json
import os

class AppController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.root = ft.Container()

        self.file = "students.json"
        self.students = self.load_data()

        # login
        self.username = ft.TextField(label="Tên lớp / học sinh")
        self.student_id = ft.TextField(label="Mã học sinh")
        self.password = ft.TextField(label="Mật khẩu", password=True)

        # add student
        self.new_id = ft.TextField(label="ID")
        self.new_name = ft.TextField(label="Tên học sinh")
        self.new_score = ft.TextField(label="Điểm")

    # ================= DATA =================
    def load_data(self):
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)

        return [
            {"id": "HS01", "name": "Nguyễn Văn A", "score": 8},
            {"id": "HS02", "name": "Trần Thị B", "score": 6},
        ]

    def save_data(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.students, f, ensure_ascii=False, indent=2)

    # ================= LOGIN =================
    def show_login(self):
        self.root.content = ft.Column(
            [
                ft.Text("LOGIN SYSTEM", size=28, weight="bold"),
                self.username,
                self.student_id,
                self.password,
                ft.ElevatedButton("Đăng nhập", on_click=self.check_login),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.page.update()

    def check_login(self, e):
        if self.password.value == "123456":
            self.snack("Đăng nhập thành công")
            self.show_home()
        else:
            self.snack("Sai mật khẩu!")

    # ================= HOME =================
    def show_home(self):
        avg = self.avg_score()

        self.root.content = ft.Column(
            [
                ft.Text("HOME (NO ICON VERSION)", size=28, weight="bold"),
                ft.Text(f"📊 Điểm trung bình: {avg}"),

                ft.ElevatedButton("Danh sách học sinh", on_click=self.show_list),
                ft.ElevatedButton("Thêm học sinh", on_click=self.show_add),
                ft.ElevatedButton("Đánh giá", on_click=self.show_evaluate),
                ft.ElevatedButton("Đăng xuất", on_click=lambda e: self.show_login()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.page.update()

    # ================= LIST =================
    def show_list(self, e):
        rows = []

        for s in self.students:
            rows.append(
                ft.Row(
                    [
                        ft.Text(f"{s['id']} | {s['name']} | {s['score']}"),
                        ft.ElevatedButton(
                            "Sửa",
                            on_click=lambda e, sid=s["id"]: self.edit_student(sid)
                        ),
                        ft.ElevatedButton(
                            "Xóa",
                            style=ft.ButtonStyle(bgcolor="red", color="white"),
                            on_click=lambda e, sid=s["id"]: self.delete_student(sid)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

        rows.append(ft.ElevatedButton("⬅ Quay lại", on_click=lambda e: self.show_home()))

        self.root.content = ft.Column(
            [
                ft.Text("DANH SÁCH HỌC SINH", size=22, weight="bold"),
                *rows
            ]
        )

        self.page.update()

    # ================= ADD =================
    def show_add(self, e):
        self.root.content = ft.Column(
            [
                ft.Text("THÊM HỌC SINH", size=22, weight="bold"),
                self.new_id,
                self.new_name,
                self.new_score,
                ft.ElevatedButton("Thêm", on_click=self.add_student),
                ft.ElevatedButton("⬅ Back", on_click=lambda e: self.show_home()),
            ]
        )
        self.page.update()

    def add_student(self, e):
        try:
            self.students.append({
                "id": self.new_id.value,
                "name": self.new_name.value,
                "score": float(self.new_score.value)
            })

            self.save_data()
            self.snack("Đã thêm học sinh")
            self.show_home()

        except:
            self.snack("Dữ liệu không hợp lệ!")

    # ================= EDIT =================
    def edit_student(self, sid):
        student = next(s for s in self.students if s["id"] == sid)

        score_input = ft.TextField(value=str(student["score"]))

        def save(e):
            student["score"] = float(score_input.value)
            self.save_data()
            self.snack("Đã cập nhật")
            self.show_list(None)

        self.root.content = ft.Column(
            [
                ft.Text(f"SỬA HỌC SINH: {student['name']}", size=22),
                score_input,
                ft.ElevatedButton("Lưu", on_click=save),
                ft.ElevatedButton("⬅ Back", on_click=lambda e: self.show_list(None)),
            ]
        )
        self.page.update()

    # ================= DELETE =================
    def delete_student(self, sid):
        self.students = [s for s in self.students if s["id"] != sid]
        self.save_data()
        self.snack("Đã xóa học sinh")
        self.show_list(None)

    # ================= EVALUATE =================
    def show_evaluate(self, e):
        view = [ft.Text("ĐÁNH GIÁ", size=22, weight="bold")]

        for s in self.students:
            status = "Giỏi" if s["score"] >= 8 else "Khá / TB"
            view.append(ft.Text(f"{s['name']} → {status}"))

        view.append(ft.ElevatedButton("⬅ Back", on_click=lambda e: self.show_home()))

        self.root.content = ft.Column(view)
        self.page.update()

    # ================= AVG =================
    def avg_score(self):
        if not self.students:
            return 0
        return round(sum(s["score"] for s in self.students) / len(self.students), 2)

    # ================= SNACK =================
    def snack(self, msg):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg))
        self.page.snack_bar.open = True
        self.page.update()