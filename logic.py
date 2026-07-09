import flet as ft
import json
import os


class AppController:

    def __init__(self, page: ft.Page):
        self.page = page
        self.root = ft.Container()

        # 🔴 THAY LINK FIREBASE CỦA BẠN VÀO ĐÂY (Phải có đuôi .json ở cuối)
        self.db_url = "https://brothers1goal-default-rtdb.firebaseio.com/.json"

        self.file = "students.json"
        self.students = self.load_data()

        # ================= ĐĂNG NHẬP =================

        self.username = ft.TextField(
            label="Tên lớp / học sinh"
        )

        self.student_id = ft.TextField(
            label="Mã học sinh"
        )

        self.password = ft.TextField(
            label="Mật khẩu",
            password=True,
            can_reveal_password=True
        )

        # ================= THÊM HỌC SINH =================

        self.new_id = ft.TextField(
            label="ID học sinh"
        )

        self.new_name = ft.TextField(
            label="Tên học sinh"
        )

        self.new_score = ft.TextField(
            label="Điểm"
        )

        # ================= ĐĂNG KÝ =================

        self.register_name = ft.TextField(
            label="Họ và tên"
        )

        self.register_id = ft.TextField(
            label="Mã học sinh"
        )

        self.register_class = ft.TextField(
            label="Lớp"
        )

        self.register_password = ft.TextField(
            label="Mật khẩu",
            password=True,
            can_reveal_password=True
        )

        self.register_confirm = ft.TextField(
            label="Nhập lại mật khẩu",
            password=True,
            can_reveal_password=True
        )

    # ================= LOAD DATA =================

    def load_data(self):

        # 1. Tải dữ liệu từ mạng (Firebase Cloud) để tất cả mọi người đồng bộ chung dữ liệu
        try:
            import urllib.request
            req = urllib.request.Request(self.db_url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as response:
                cloud_data = json.loads(response.read().decode("utf-8"))
                if cloud_data is not None:
                    return cloud_data
        except:
            pass

        # 2. Dự phòng: Thử tải dữ liệu từ bộ nhớ Trình duyệt Web nếu mất mạng
        try:
            import js
            web_data = js.localStorage.getItem("students_storage_data")
            if web_data:
                return json.loads(web_data)
        except:
            pass

        # 3. Dự phòng: Thử tải từ file json cục bộ nếu chạy offline trên máy tính
        try:
            if os.path.exists(self.file):
                with open(
                    self.file,
                    "r",
                    encoding="utf-8"
                ) as f:
                    return json.load(f)
        except:
            pass

        return [
            {
                "id": "HS01",
                "name": "Nguyễn Văn A",
                "class": "10A1",
                "password": "123456",
                "score": 8
            },
            {
                "id": "HS02",
                "name": "Trần Thị B",
                "class": "10A1",
                "password": "123456",
                "score": 6
            }
        ]

    # ================= SAVE DATA =================

    def save_data(self):

        # 1. Gửi dữ liệu lên Cloud (Firebase) để cập nhật trực tiếp cho tất cả thiết bị khác
        try:
            import urllib.request
            req = urllib.request.Request(
                self.db_url,
                data=json.dumps(self.students, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="PUT"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                pass
        except:
            pass

        # 2. Dự phòng: Lưu vào bộ nhớ Trình duyệt Web của riêng máy này
        try:
            import js
            json_string = json.dumps(self.students, ensure_ascii=False)
            js.localStorage.setItem("students_storage_data", json_string)
        except:
            pass

        # 3. Dự phòng: Lưu vào file json cục bộ nếu đang chạy trên PyCharm máy tính
        try:
            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.students,
                    f,
                    ensure_ascii=False,
                    indent=2
                )
        except:
            pass

    # ================= TRANG ĐĂNG NHẬP =================

    def show_login(self):

        self.username.value = ""
        self.student_id.value = ""
        self.password.value = ""

        self.root.content = ft.Column(
            [

                ft.Text(
                    "HỆ THỐNG QUẢN LÝ HỌC SINH",
                    size=28,
                    weight="bold"
                ),

                self.username,

                self.student_id,

                self.password,

                ft.ElevatedButton(
                    "Đăng nhập",
                    on_click=self.check_login
                ),

                ft.Divider(),

                ft.Text(
                    "Chưa có tài khoản?"
                ),

                ft.TextButton(
                    "Đăng ký",
                    on_click=self.show_register
                )

            ],

            alignment=ft.MainAxisAlignment.CENTER,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.page.update()

# ================= KIỂM TRA ĐĂNG NHẬP =================

    def check_login(self, e):

        if self.username.value == "":
            self.snack(
                "Vui lòng nhập tên lớp hoặc học sinh"
            )
            return

        if self.student_id.value == "":
            self.snack(
                "Vui lòng nhập mã học sinh"
            )
            return

        if self.password.value == "":
            self.snack(
                "Vui lòng nhập mật khẩu"
            )
            return

        found = False

        for student in self.students:

            if (
                student["id"] == self.student_id.value
                and student["password"] == self.password.value
            ):
                found = True
                break

        if found:

            self.snack(
                "Đăng nhập thành công"
            )

            self.show_home()

        else:

            self.snack(
                "Sai thông tin đăng nhập"
            )

    # ================= TRANG ĐĂNG KÝ =================

    def show_register(self, e):

        self.register_name.value = ""
        self.register_id.value = ""
        self.register_class.value = ""
        self.register_password.value = ""
        self.register_confirm.value = ""

        self.root.content = ft.Column(
            [

                ft.Text(
                    "ĐĂNG KÝ TÀI KHOẢN",
                    size=28,
                    weight="bold"
                ),

                self.register_name,

                self.register_id,

                self.register_class,

                self.register_password,

                self.register_confirm,

                ft.ElevatedButton(
                    "Đăng ký",
                    on_click=self.register
                ),

                ft.TextButton(
                    "Quay lại",
                    on_click=lambda e: self.show_login()
                )

            ],

            alignment=ft.MainAxisAlignment.CENTER,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.page.update()

    # ================= XỬ LÝ ĐĂNG KÝ =================

    def register(self, e):

        if self.register_name.value == "":
            self.snack("Vui lòng nhập họ tên")
            return

        if self.register_id.value == "":
            self.snack("Vui lòng nhập mã học sinh")
            return

        if self.register_class.value == "":
            self.snack("Vui lòng nhập lớp")
            return

        if self.register_password.value == "":
            self.snack("Vui lòng nhập mật khẩu")
            return

        if self.register_password.value != self.register_confirm.value:
            self.snack(
                "Mật khẩu nhập lại không khớp"
            )
            return

        for student in self.students:
            if student["id"] == self.register_id.value:
                self.snack(
                    "Mã học sinh đã tồn tại"
                )
                return

        self.students.append(
            {
                "id": self.register_id.value,
                "name": self.register_name.value,
                "class": self.register_class.value,
                "password": self.register_password.value,
                "score": 0
            }
        )

        self.save_data()

        self.snack(
            "Đăng ký thành công"
        )

        self.show_login()

# ================= TRANG CHỦ =================

    def show_home(self):

        average = self.avg_score()

        self.root.content = ft.Column(
            [

                ft.Text(
                    "TRANG CHỦ",
                    size=28,
                    weight="bold"
                ),

                ft.Text(
                    f"Tổng số học sinh: {len(self.students)}"
                ),

                ft.Text(
                    f"Điểm trung bình: {average}"
                ),

                ft.ElevatedButton(
                    "Danh sách học sinh",
                    on_click=self.show_list
                ),

                ft.ElevatedButton(
                    "Thêm học sinh",
                    on_click=self.show_add
                ),

                ft.ElevatedButton(
                    "Đánh giá học sinh",
                    on_click=self.show_evaluate
                ),

                ft.ElevatedButton(
                    "Thống kê",
                    on_click=self.show_statistics
                ),

                ft.ElevatedButton(
                    "Đăng xuất",
                    on_click=lambda e: self.show_login()
                )

            ],

            alignment=ft.MainAxisAlignment.CENTER,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.page.update()

    # ================= DANH SÁCH HỌC SINH =================

    def show_list(self, e):

        controls = []

        for student in self.students:

            controls.append(

                ft.Row(
                    [

                        ft.Text(
                            f"ID: {student['id']} | "
                            f"Tên: {student['name']} | "
                            f"Điểm: {student['score']}"
                        ),

                        ft.ElevatedButton(
                            "Sửa",
                            on_click=lambda e, sid=student["id"]:
                            self.edit_student(sid)
                        ),

                        ft.ElevatedButton(
                            "Xóa",
                            on_click=lambda e, sid=student["id"]:
                            self.delete_student(sid)
                        )

                    ],

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN

                )

            )

        controls.append(

            ft.ElevatedButton(
                "Quay lại",
                on_click=lambda e: self.show_home()
            )

        )

        self.root.content = ft.Column(

            [

                ft.Text(
                    "DANH SÁCH HỌC SINH",
                    size=24,
                    weight="bold"
                ),

                *controls

            ]

        )

        self.page.update()

    # ================= THÊM HỌC SINH =================

    def show_add(self, e):

        self.new_id.value = ""
        self.new_name.value = ""
        self.new_score.value = ""

        self.root.content = ft.Column(
            [

                ft.Text(
                    "THÊM HỌC SINH",
                    size=24,
                    weight="bold"
                ),

                self.new_id,

                self.new_name,

                self.new_score,

                ft.ElevatedButton(
                    "Thêm học sinh",
                    on_click=self.add_student
                ),

                ft.ElevatedButton(
                    "Quay lại",
                    on_click=lambda e: self.show_home()
                )

            ]

        )

        self.page.update()

    def add_student(self, e):

        if self.new_id.value == "":
            self.snack(
                "Vui lòng nhập ID học sinh"
            )
            return

        if self.new_name.value == "":
            self.snack(
                "Vui lòng nhập tên học sinh"
            )
            return

        if self.new_score.value == "":
            self.snack(
                "Vui lòng nhập điểm"
            )
            return

        for student in self.students:

            if student["id"] == self.new_id.value:
                self.snack(
                    "ID học sinh đã tồn tại"
                )
                return

        try:

            score = float(
                self.new_score.value
            )

            if score < 0 or score > 10:
                self.snack(
                    "Điểm phải từ 0 đến 10"
                )
                return

            self.students.append(

                {

                    "id": self.new_id.value,

                    "name": self.new_name.value,

                    # Giữ dữ liệu đồng nhất với đăng ký
                    "class": "",

                    "password": "123456",

                    "score": score

                }

            )

            self.save_data()

            self.snack(
                "Đã thêm học sinh"
            )

            self.show_home()

        except:

            self.snack(
                "Điểm không hợp lệ"
            )

    # ================= SỬA HỌC SINH =================

    def edit_student(self, sid):

        student = None

        for s in self.students:

            if s["id"] == sid:
                student = s
                break

        if student is None:
            self.snack(
                "Không tìm thấy học sinh"
            )
            return

        name_input = ft.TextField(
            label="Tên học sinh",
            value=student["name"]
        )

        score_input = ft.TextField(
            label="Điểm",
            value=str(student["score"])
        )

        def save(e):

            if name_input.value == "":
                self.snack(
                    "Tên học sinh không được để trống"
                )
                return

            try:

                score = float(
                    score_input.value
                )

                if score < 0 or score > 10:
                    self.snack(
                        "Điểm phải từ 0 đến 10"
                    )
                    return

                student["name"] = name_input.value
                student["score"] = score

                self.save_data()

                self.snack(
                    "Cập nhật thành công"
                )

                self.show_list(None)

            except:

                self.snack(
                    "Điểm không hợp lệ"
                )

        self.root.content = ft.Column(
            [

                ft.Text(
                    "SỬA HỌC SINH",
                    size=24,
                    weight="bold"
                ),

                ft.Text(
                    f"ID: {student['id']}"
                ),

                name_input,

                score_input,

                ft.ElevatedButton(
                    "Lưu",
                    on_click=save
                ),

                ft.ElevatedButton(
                    "Quay lại",
                    on_click=lambda e: self.show_list(None)
                )

            ]

        )

        self.page.update()

# ================= XÓA HỌC SINH =================

    def delete_student(self, sid):

        for student in self.students:

            if student["id"] == sid:
                self.students.remove(student)
                break

        self.save_data()

        self.snack(
            "Đã xóa học sinh"
        )

        self.show_list(None)

    # ================= ĐÁNH GIÁ HỌC SINH =================

    def show_evaluate(self, e):

        view = []

        view.append(

            ft.Text(
                "ĐÁNH GIÁ HỌC SINH",
                size=24,
                weight="bold"
            )

        )

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

            view.append(

                ft.Text(
                    f"{student['name']} - {score} → {status}"
                )

            )

        view.append(

            ft.ElevatedButton(

                "Quay lại",

                on_click=lambda e: self.show_home()

            )

        )

        self.root.content = ft.Column(
            view
        )

        self.page.update()

    # ================= THỐNG KÊ =================

    def show_statistics(self, e):

        total = len(
            self.students
        )

        if total == 0:

            self.root.content = ft.Column(
                [
                    ft.Text(
                        "Không có dữ liệu",
                        size=20
                    ),
                    ft.ElevatedButton(
                        "Quay lại",
                        on_click=lambda e: self.show_home()
                    )
                ]
            )

            self.page.update()
            return

        gioi = 0
        kha = 0
        trungbinh = 0
        yeu = 0

        for student in self.students:

            score = student["score"]

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

                ft.Text(
                    "THỐNG KÊ",
                    size=24,
                    weight="bold"
                ),

                ft.Text(
                    f"Tổng học sinh: {total}"
                ),

                ft.Text(
                    f"Điểm trung bình: {self.avg_score()}"
                ),

                ft.Text(
                    f"Giỏi: {gioi}"
                ),

                ft.Text(
                    f"Khá: {kha}"
                ),

                ft.Text(
                    f"Trung bình: {trungbinh}"
                ),

                ft.Text(
                    f"Yếu: {yeu}"
                ),

                ft.ElevatedButton(
                    "Quay lại",
                    on_click=lambda e: self.show_home()
                )

            ]

        )

        self.page.update()

# ================= TÍNH ĐIỂM TRUNG BÌNH =================

    def avg_score(self):

        if len(self.students) == 0:
            return 0

        total = 0

        for student in self.students:
            total += student["score"]

        return round(
            total / len(self.students),
            2
        )

    # ================= THÔNG BÁO =================

    def snack(self, msg):

        self.page.snack_bar = ft.SnackBar(

            ft.Text(msg)

        )

        self.page.snack_bar.open = True

        self.page.update()