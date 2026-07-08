import flet as ft
import json


class AppController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.root = ft.Container()

        # Firebase Realtime Database Endpoint
        self.db_url = "https://brothers1goal-default-rtdb.firebaseio.com/students.json"
        self.students = []  # Will be loaded asynchronously from the cloud

        # ================= ĐĂNG NHẬP =================
        self.username = ft.TextField(label="Tên lớp / học sinh")
        self.student_id = ft.TextField(label="Mã học sinh")
        self.password = ft.TextField(label="Mật khẩu", password=True, can_reveal_password=True)

        # ================= THÊM HỌC SINH =================
        self.new_id = ft.TextField(label="ID học sinh")
        self.new_name = ft.TextField(label="Tên học sinh")
        self.new_score = ft.TextField(label="Điểm")

        # ================= ĐĂNG KÝ =================
        self.register_name = ft.TextField(label="Họ và tên")
        self.register_id = ft.TextField(label="Mã học sinh")
        self.register_class = ft.TextField(label="Lớp")
        self.register_password = ft.TextField(label="Mật khẩu", password=True, can_reveal_password=True)
        self.register_confirm = ft.TextField(label="Nhập lại mật khẩu", password=True, can_reveal_password=True)

    # ================= LOAD DATA FROM CLOUD =================
    async def load_data_async(self):
        try:
            res = await self.page.fetch_data_async(self.db_url, method="GET")
            if res and res.text and res.text != "null":
                data = json.loads(res.text)
                if isinstance(data, list):
                    self.students = [s for s in data if s is not None]
                    print("--- DỮ LIỆU ĐÃ TẢI THÀNH CÔNG ---")
                    print(f"Danh sách tài khoản: {self.students}")
                    return
                elif isinstance(data, dict):
                    self.students = [v for v in data.values() if v is not None]
                    print("--- DỮ LIỆU ĐÃ TẢI THÀNH CÔNG ---")
                    print(f"Danh sách tài khoản: {self.students}")
                    return
        except Exception as e:
            print(f"⚠️ LỖI KẾT NỐI CLOUD: {e}")

        # Fallback dữ liệu tạm thời nếu Cloud mất mạng
        print("⚠️ ĐANG DÙNG TÀI KHOẢN TẠM THỜI (OFFLINE)")
        self.students = [
            {"id": "HS01", "name": "Nguyễn Văn A", "class": "10A1", "password": "123456", "score": 8},
            {"id": "HS02", "name": "Trần Thị B", "class": "10A1", "password": "123456", "score": 6}
        ]

    # ================= SAVE DATA TO CLOUD =================
    async def save_data_async(self):
        try:
            # Overwrite the Firebase node with the updated student list structure
            await self.page.fetch_data_async(
                self.db_url,
                method="PUT",
                body=json.dumps(self.students, ensure_ascii=False)
            )
        except Exception as e:
            print(f"Cloud save error: {e}")

    # ================= TRANG ĐĂNG NHẬP =================
    async def show_login(self):
        # Always fetch fresh database entries when coming back to login screen
        await self.load_data_async()

        self.username.value = ""
        self.student_id.value = ""
        self.password.value = ""

        self.root.content = ft.Column(
            [
                ft.Text("HỆ THỐNG QUẢN LÝ HỌC SINH", size=28, weight="bold"),
                self.username,
                self.student_id,
                self.password,
                ft.ElevatedButton("Đăng nhập", on_click=lambda e: self.page.run_task(self.check_login)),
                ft.Divider(),
                ft.Text("Chưa có tài khoản?"),
                ft.TextButton("Đăng ký", on_click=lambda e: self.page.run_task(self.show_register))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    # ================= KIỂM TRA ĐĂNG NHẬP =================
    async def check_login(self):
        if not self.username.value or not self.student_id.value or not self.password.value:
            self.snack("Vui lòng điền đầy đủ thông tin đăng nhập")
            return

        found_student = None
        for student in self.students:
            if student.get("id") == self.student_id.value:
                found_student = student
                break

        if found_student and str(found_student.get("password")) == str(self.password.value):
            self.snack("Đăng nhập thành công")
            await self.show_home()
        else:
            self.snack("Mã học sinh hoặc mật khẩu không chính xác")

    # ================= TRANG ĐĂNG KÝ =================
    async def show_register(self):
        self.register_name.value = ""
        self.register_id.value = ""
        self.register_class.value = ""
        self.register_password.value = ""
        self.register_confirm.value = ""

        self.root.content = ft.Column(
            [
                ft.Text("ĐĂNG KÝ TÀI KHOẢN", size=28, weight="bold"),
                self.register_name,
                self.register_id,
                self.register_class,
                self.register_password,
                self.register_confirm,
                ft.ElevatedButton("Đăng ký", on_click=lambda e: self.page.run_task(self.register)),
                ft.TextButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_login))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    # ================= XỬ LÝ ĐĂNG KÝ =================
    async def register(self):
        if self.register_name.value == "" or self.register_id.value == "" or self.register_class.value == "" or self.register_password.value == "":
            self.snack("Vui lòng nhập đầy đủ thông tin")
            return

        if self.register_password.value != self.register_confirm.value:
            self.snack("Mật khẩu nhập lại không khớp")
            return

        for student in self.students:
            if student.get("id") == self.register_id.value:
                self.snack("Mã học sinh đã tồn tại")
                return

        self.students.append({
            "id": self.register_id.value,
            "name": self.register_name.value,
            "class": self.register_class.value,
            "password": self.register_password.value,
            "score": 0
        })

        await self.save_data_async()
        self.snack("Đăng ký thành công")
        await self.show_login()

    # ================= TRANG CHỦ =================
    async def show_home(self):
        average = self.avg_score()
        self.root.content = ft.Column(
            [
                ft.Text("TRANG CHỦ", size=28, weight="bold"),
                ft.Text(f"Tổng số học sinh: {len(self.students)}"),
                ft.Text(f"Điểm trung bình: {average}"),
                ft.ElevatedButton("Danh sách học sinh", on_click=lambda e: self.page.run_task(self.show_list)),
                ft.ElevatedButton("Thêm học sinh", on_click=lambda e: self.page.run_task(self.show_add)),
                ft.ElevatedButton("Đánh giá học sinh", on_click=lambda e: self.page.run_task(self.show_evaluate)),
                ft.ElevatedButton("Thống kê", on_click=lambda e: self.page.run_task(self.show_statistics)),
                ft.ElevatedButton("Đăng xuất", on_click=lambda e: self.page.run_task(self.show_login))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    # ================= DANH SÁCH HỌC SINH =================
    async def show_list(self):
        controls = []
        for student in self.students:
            sid = student.get("id", "")
            controls.append(
                ft.Row(
                    [
                        ft.Text(f"ID: {sid} | Tên: {student.get('name', '')} | Điểm: {student.get('score', 0)}"),
                        ft.ElevatedButton("Sửa", on_click=lambda e, s=sid: self.page.run_task(self.edit_student, s)),
                        ft.ElevatedButton("Xóa", on_click=lambda e, s=sid: self.page.run_task(self.delete_student, s))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )

        controls.append(ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home)))
        self.root.content = ft.Column([ft.Text("DANH SÁCH HỌC SINH", size=24, weight="bold"), *controls])
        self.page.update()

    # ================= THÊM HỌC SINH =================
    async def show_add(self):
        self.new_id.value = ""
        self.new_name.value = ""
        self.new_score.value = ""

        self.root.content = ft.Column(
            [
                ft.Text("THÊM HỌC SINH", size=24, weight="bold"),
                self.new_id,
                self.new_name,
                self.new_score,
                ft.ElevatedButton("Thêm học sinh", on_click=lambda e: self.page.run_task(self.add_student)),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home))
            ]
        )
        self.page.update()

    async def add_student(self):
        if self.new_id.value == "" or self.new_name.value == "" or self.new_score.value == "":
            self.snack("Vui lòng nhập đầy đủ thông tin")
            return

        for student in self.students:
            if student.get("id") == self.new_id.value:
                self.snack("ID học sinh đã tồn tại")
                return

        try:
            score = float(self.new_score.value)
            if score < 0 or score > 10:
                self.snack("Điểm phải từ 0 đến 10")
                return

            self.students.append({
                "id": self.new_id.value,
                "name": self.new_name.value,
                "score": score
            })

            await self.save_data_async()
            self.snack("Đã thêm học sinh")
            await self.show_home()
        except:
            self.snack("Điểm không hợp lệ")

    # ================= SỬA HỌC SINH =================
    async def edit_student(self, sid):
        student = next((s for s in self.students if s.get("id") == sid), None)
        if student is None:
            self.snack("Không tìm thấy học sinh")
            return

        name_input = ft.TextField(label="Tên học sinh", value=student.get("name", ""))
        score_input = ft.TextField(label="Điểm", value=str(student.get("score", 0)))

        async def save_edit():
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
                self.snack("Cập nhật thành công")
                await self.show_list()
            except:
                self.snack("Điểm không hợp lệ")

        self.root.content = ft.Column(
            [
                ft.Text("SỬA HỌC SINH", size=24, weight="bold"),
                ft.Text(f"ID: {sid}"),
                name_input,
                score_input,
                ft.ElevatedButton("Lưu", on_click=lambda e: self.page.run_task(save_edit)),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_list))
            ]
        )
        self.page.update()

    # ================= XÓA HỌC SINH =================
    async def delete_student(self, sid):
        self.students = [s for s in self.students if s.get("id") != sid]
        await self.save_data_async()
        self.snack("Đã xóa học sinh")
        await self.show_list()

    # ================= ĐÁNH GIÁ HỌC SINH =================
    async def show_evaluate(self):
        view = [ft.Text("ĐÁNH GIÁ HỌC SINH", size=24, weight="bold")]
        for student in self.students:
            score = student.get("score", 0)
            status = "Giỏi" if score >= 8 else "Khá" if score >= 6.5 else "Trung bình" if score >= 5 else "Yếu"
            view.append(ft.Text(f"{student.get('name', '')} - {score} → {status}"))

        view.append(ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home)))
        self.root.content = ft.Column(view)
        self.page.update()

    # ================= THỐNG KÊ =================
    async def show_statistics(self):
        total = len(self.students)
        if total == 0:
            self.root.content = ft.Column([ft.Text("Không có dữ liệu"), ft.ElevatedButton("Quay lại", on_click=lambda
                e: self.page.run_task(self.show_home))])
            self.page.update()
            return

        gioi = kha = trungbinh = yeu = 0
        for student in self.students:
            score = student.get("score", 0)
            if score >= 8:
                gioi += 1
            elif score >= 6.5:
                kha += 1
            elif score >= 5:
                trungbinh += 1
            else:
                yeu += 1

        self.root.content = ft.Column(
            [
                ft.Text("THỐNG KÊ", size=24, weight="bold"),
                ft.Text(f"Tổng học sinh: {total}"),
                ft.Text(f"Điểm trung bình: {self.avg_score()}"),
                ft.Text(f"Giỏi: {gioi}"),
                ft.Text(f"Khá: {kha}"),
                ft.Text(f"Trung bình: {trungbinh}"),
                ft.Text(f"Yếu: {yeu}"),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.page.run_task(self.show_home))
            ]
        )
        self.page.update()

    # ================= TÍNH ĐIỂM TRUNG BÌNH =================
    def avg_score(self):
        if len(self.students) == 0: return 0
        total = sum(student.get("score", 0) for student in self.students)
        return round(total / len(self.students), 2)

    # ================= THÔNG BÁO =================
    def snack(self, msg):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg))
        self.page.snack_bar.open = True
        self.page.update()