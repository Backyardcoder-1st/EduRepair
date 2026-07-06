import flet as ft
import json


class AppController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.root = ft.Container()

        # Your live Firebase cloud link address
        self.db_url = "https://brothers1goal-default-rtdb.firebaseio.com/students.json"
        self.students = []

        # ================= ĐĂNG NHẬP =================
        self.username = ft.TextField(label="Tên lớp / học sinh")
        self.student_id = ft.TextField(label="Mã học sinh")
        self.password = ft.TextField(
            label="Mật khẩu",
            password=True,
            can_reveal_password=True,
        )

        # ================= THÊM HỌC SINH =================
        self.new_id = ft.TextField(label="ID học sinh")
        self.new_name = ft.TextField(label="Tên học sinh")
        self.new_score = ft.TextField(label="Điểm")

    # ================= BROWSER-SAFE CLOUD SYNC =================
    async def load_data_async(self):
        try:
            response = await self.page.fetch_data_async(self.db_url, method="GET")
            if response and response.status_code == 200:
                data = json.loads(response.body)
                if data:
                    if isinstance(data, dict):
                        return list(data.values())
                    return [item for item in data if item is not None]
        except Exception as e:
            print(f"Cloud load error: {e}")

        # Default starting values fallback
        return [
            {"id": "HS01", "name": "Nguyễn Văn A", "score": 8.0},
            {"id": "HS02", "name": "Trần Thị B", "score": 6.0},
        ]

    async def save_data_async(self):
        try:
            await self.page.fetch_data_async(
                self.db_url,
                method="PUT",
                body=json.dumps(self.students),
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            print(f"Cloud save error: {e}")

    # ================= ĐĂNG NHẬP =================
    def show_login(self):
        self.username.value = ""
        self.student_id.value = ""
        self.password.value = ""

        self.root.content = ft.Column(
            [
                ft.Text("HỆ THỐNG QUẢN LÝ HỌC SINH", size=28, weight="bold"),
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
        if self.username.value == "":
            self.snack("Vui lòng nhập tên lớp hoặc học sinh")
            return
        if self.student_id.value == "":
            self.snack("Vui lòng nhập mã học sinh")
            return
        if self.password.value != "123456":
            self.snack("Sai mật khẩu")
            return

        self.snack("Đăng nhập thành công")
        self.page.run_task(self.show_home_async)

    # ================= TRANG CHỦ =================
    async def show_home_async(self):
        self.students = await self.load_data_async()
        average = self.avg_score()

        self.root.content = ft.Column(
            [
                ft.Text("TRANG CHỦ", size=28, weight="bold"),
                ft.Text(f"Tổng số học sinh: {len(self.students)}"),
                ft.Text(f"Điểm trung bình: {average}"),
                ft.ElevatedButton("Danh sách học sinh", on_click=lambda e: self.show_list()),
                ft.ElevatedButton("Thêm học sinh", on_click=lambda e: self.show_add()),
                ft.ElevatedButton("Đánh giá học sinh", on_click=lambda e: self.show_evaluate()),
                ft.ElevatedButton("Thống kê", on_click=lambda e: self.show_statistics()),
                ft.ElevatedButton("Đăng xuất", on_click=lambda e: self.show_login()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.page.update()

    # ================= DANH SÁCH HỌC SINH =================
    def show_list(self):
        controls = []
        for student in self.students:
            controls.append(
                ft.Row(
                    [
                        ft.Text(f"ID: {student['id']} | Tên: {student['name']} | Điểm: {student['score']}"),
                        ft.ElevatedButton("Sửa", on_click=lambda e, sid=student["id"]: self.edit_student(sid)),
                        ft.ElevatedButton("Xóa", on_click=lambda e, sid=student["id"]: self.page.run_task(
                            self.delete_student_async, sid)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

        controls.append(ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home_async)))

        self.root.content = ft.Column([ft.Text("DANH SÁCH HỌC SINH", size=24, weight="bold"), *controls])
        self.page.update()

    # ================= THÊM HỌC SINH =================
    def show_add(self):
        self.new_id.value = ""
        self.new_name.value = ""
        self.new_score.value = ""

        self.root.content = ft.Column(
            [
                ft.Text("THÊM HỌC SINH", size=24, weight="bold"),
                self.new_id,
                self.new_name,
                self.new_score,
                ft.ElevatedButton("Thêm học sinh", on_click=lambda e: self.page.run_task(self.add_student_async)),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home_async)),
            ]
        )
        self.page.update()

    async def add_student_async(self, e):
        if self.new_id.value == "":
            self.snack("Vui lòng nhập ID học sinh")
            return
        if self.new_name.value == "":
            self.snack("Vui lòng nhập tên học sinh")
            return
        if self.new_score.value == "":
            self.snack("Vui lòng nhập điểm")
            return

        for student in self.students:
            if student["id"] == self.new_id.value:
                self.snack("ID học sinh đã tồn tại")
                return

        try:
            score = float(self.new_score.value)
            if score < 0 or score > 10:
                self.snack("Điểm phải nằm trong khoảng từ 0 đến 10")
                return

            self.students.append({
                "id": self.new_id.value,
                "name": self.new_name.value,
                "score": score,
            })

            await self.save_data_async()
            self.snack("Đã thêm học sinh lên mây Cloud")
            await self.show_home_async()
        except:
            self.snack("Điểm không hợp lệ")

    # ================= SỬA HỌC SINH =================
    def edit_student(self, sid):
        student = next((s for s in self.students if s["id"] == sid), None)
        if student is None:
            self.snack("Không tìm thấy học sinh")
            return

        name_input = ft.TextField(label="Tên học sinh", value=student["name"])
        score_input = ft.TextField(label="Điểm", value=str(student["score"]))

        async def save_edit(e):
            if name_input.value == "":
                self.snack("Tên học sinh không được để trống")
                return
            try:
                score = float(score_input.value)
                if score < 0 or score > 10:
                    self.snack("Điểm phải từ 0 đến 10")
                    return

                student["name"] = name_input.value
                student["score"] = score

                await self.save_data_async()
                self.snack("Đã cập nhật học sinh thành công!")

                # Crucial fix: return cleanly to list view after backend finishes save task
                self.show_list()
            except:
                self.snack("Điểm không hợp lệ")

        self.root.content = ft.Column(
            [
                ft.Text("SỬA HỌC SINH", size=24, weight="bold"),
                ft.Text(f"ID: {student['id']}"),
                name_input,
                score_input,
                ft.ElevatedButton("Lưu", on_click=lambda e: self.page.run_task(save_edit)),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_list()),
            ]
        )
        self.page.update()

    # ================= XÓA HỌC SINH =================
    async def delete_student_async(self, sid):
        self.students = [s for s in self.students if s["id"] != sid]
        await self.save_data_async()
        self.snack("Đã xóa học sinh khỏi hệ thống")
        self.show_list()

    # ================= ĐÁNH GIÁ HỌC SINH =================
    def show_evaluate(self, e):
        view = [ft.Text("ĐÁNH GIÁ HỌC SINH", size=24, weight="bold")]

        for student in self.students:
            score = student["score"]
            if score >= 8:
                status = "Giỏi"
            elif score >= 6.5:
                status = "Khá"
            elif score >= 5:
                status = "Trung bình"
            else:
                status = "Yếu"

            view.append(ft.Text(f"{student['name']} - {score} → {status}"))

        view.append(ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home_async)))
        self.root.content = ft.Column(view)
        self.page.update()

    # ================= THỐNG KÊ =================
    def show_statistics(self, e):
        total = len(self.students)
        if total == 0:
            self.root.content = ft.Column([
                ft.Text("Không có dữ liệu"),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home_async))
            ])
            self.page.update()
            return

        total_score = sum(s["score"] for s in self.students)
        gioi = sum(1 for s in self.students if s["score"] >= 8)
        kha = sum(1 for s in self.students if 6.5 <= s["score"] < 8)
        tb = sum(1 for s in self.students if 5 <= s["score"] < 6.5)
        yeu = sum(1 for s in self.students if s["score"] < 5)

        avg = round(total_score / total, 2)

        self.root.content = ft.Column(
            [
                ft.Text("THỐNG KÊ", size=24, weight="bold"),
                ft.Text(f"Tổng học sinh: {total}"),
                ft.Text(f"Điểm trung bình: {avg}"),
                ft.Text(f"Giỏi: {gioi}"),
                ft.Text(f"Khá: {kha}"),
                ft.Text(f"Trung bình: {tb}"),
                ft.Text(f"Yếu: {yeu}"),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home_async)),
            ]
        )
        self.page.update()

    # ================= TÍNH ĐIỂM TRUNG BÌNH =================
    def avg_score(self):
        if len(self.students) == 0:
            return 0
        return round(sum(s["score"] for s in self.students) / len(self.students), 2)

    # ================= THÔNG BÁO =================
    def snack(self, msg):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg))
        self.page.snack_bar.open = True
        self.page.update()