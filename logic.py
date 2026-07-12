import flet as ft
import json
import os
import urllib.request
import ssl
import base64

try:
    _context = ssl.create_default_context()
except AttributeError:
    _context = None


class AppController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.file = "students.json"

        # Khởi tạo khung chứa bắt buộc để không bị lỗi 'root' undefined
        self.root = ft.Container()

        # Đường link Firebase giải mã an toàn
        self.db_url = base64.b64decode(
            "aHR0cHM6Ly9icm90aGVyczFnb2FsLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbS9zdHVkZW50cy5qc29u").decode("utf-8")

        self.students = []
        self.current_user = None
        self.admin_key = "123"

        # Tích hợp bộ chọn ảnh minh chứng Base64
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)
        self.current_image_base64 = ""

        # ================= KHAI BÁO CÁC Ô NHẬP LIỆU (SỬA LỖI CRASH) =================
        # Đăng nhập admin
        self.admin_key_login = ft.TextField(label="Mã Giám Thị / Admin", password=True, can_reveal_password=True)

        # Đăng nhập học sinh
        self.student_login_name = ft.TextField(label="Tên đăng nhập (Họ tên)")
        self.student_login_password = ft.TextField(label="Mật khẩu", password=True, can_reveal_password=True)

        # Đăng ký học sinh
        self.student_name = ft.TextField(label="Họ và tên học sinh")
        self.student_class = ft.TextField(label="Lớp học")
        self.student_password = ft.TextField(label="Mật khẩu tài khoản", password=True)
        self.student_confirm = ft.TextField(label="Xác nhận mật khẩu", password=True)

        # Admin thêm học sinh mới
        self.new_id = ft.TextField(label="Mã số (Để trống để tự tạo)")
        self.new_name = ft.TextField(label="Họ tên học sinh mới")
        self.new_score = ft.TextField(label="Điểm số ban đầu")

        # Admin sửa điểm
        self.edit_student_id = ft.TextField(label="Mã học sinh cần nâng điểm")
        self.edit_score = ft.TextField(label="Điểm mới")

    # ================= HÀM XỬ LÝ CHỌN ẢNH (BASE64) =================
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            picked_file = e.files[0]
            try:
                with open(picked_file.path, "rb") as image_file:
                    self.current_image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

                if self.current_user and self.current_user.get("role") == "student":
                    self.current_user["image_proof"] = self.current_image_base64
                    for student in self.students:
                        if student.get("id") == self.current_user.get("id"):
                            student["image_proof"] = self.current_image_base64
                            break
                    self.save_data()

                self.show_message("Đã tải ảnh minh chứng lên hệ thống thành công!")
                self.show_student_home()
            except Exception as ex:
                self.show_message("Không thể đọc file ảnh này!")

    # ================= HÀM TẢI DỮ LIỆU (LOAD DATA) =================
    def load_data(self):
        try:
            req = urllib.request.Request(
                self.db_url,
                headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
                method="GET"
            )
            with urllib.request.urlopen(req, timeout=5, context=_context) as response:
                raw_content = response.read().decode("utf-8")
                data = json.loads(raw_content)
                if data:
                    if isinstance(data, dict):
                        self.students = list(data.values())
                    elif isinstance(data, list):
                        self.students = [s for s in data if s is not None]
                    return
        except Exception as e:
            print(f"Lỗi tải dữ liệu trực tuyến: {e}")

        try:
            if os.path.exists(self.file):
                with open(self.file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.students = list(data.values())
                    elif isinstance(data, list):
                        self.students = [s for s in data if s is not None]
                    return
        except Exception as e:
            print(f"Lỗi đọc file local: {e}")

        self.students = [
            {"id": "HS01", "name": "Nguyễn Văn A", "class": "A1", "password": "123456", "score": 8, "role": "student"},
            {"id": "HS02", "name": "Trần Thị B", "class": "A1", "password": "123456", "score": 6, "role": "student"}
        ]

    # ================= HÀM LƯU DỮ LIỆU (SAVE DATA) =================
    def save_data(self):
        data_to_save = {s["id"]: s for s in self.students if isinstance(s, dict) and "id" in s}
        try:
            req = urllib.request.Request(
                self.db_url,
                data=json.dumps(data_to_save, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                method="PUT"
            )
            with urllib.request.urlopen(req, timeout=5, context=_context) as response:
                pass
        except Exception as e:
            print(f"Lỗi lưu dữ liệu trực tuyến: {e}")

        try:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.students, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi ghi file local: {e}")

    # ================= CÁC CHỨC NĂNG GIAO DIỆN (GIỮ NGUYÊN TỪNG HÀM BIỆT LẬP) =================
    def show_role_select(self):
        self.root.content = ft.Column(
            [
                ft.Text("Bạn là ai?", size=30),
                ft.ElevatedButton("Admin", on_click=lambda e: self.show_admin_login()),
                ft.ElevatedButton("Học sinh", on_click=lambda e: self.show_student_login())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_admin_login(self):
        def login(e):
            if self.admin_key_login.value == self.admin_key:
                self.current_user = {"name": "Admin", "role": "admin"}
                self.show_admin_home()
                return
            self.show_message("Sai key Admin")

        self.root.content = ft.Column(
            [
                ft.Text("Đăng nhập Admin", size=30),
                self.admin_key_login,
                ft.ElevatedButton("Đăng nhập", on_click=login),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_role_select())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_admin_home(self):
        self.root.content = ft.Column(
            [
                ft.Text("Trang Admin", size=30),
                ft.ElevatedButton("Danh sách học sinh", on_click=lambda e: self.show_student_list()),
                ft.ElevatedButton("Thêm học sinh", on_click=lambda e: self.show_add_student()),
                ft.ElevatedButton("Quản lý học sinh", on_click=lambda e: self.show_manage_student()),
                ft.ElevatedButton("Nâng điểm học sinh", on_click=lambda e: self.show_update_score()),
                ft.ElevatedButton("Tìm kiếm học sinh", on_click=lambda e: self.show_search_student()),
                ft.ElevatedButton("Đăng xuất", on_click=lambda e: self.logout())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_student_login(self):
        def login(e):
            for student in self.students:
                if (student.get("role") == "student" and
                        student.get("name") == self.student_login_name.value and
                        student.get("password") == self.student_login_password.value):
                    self.current_user = student
                    self.show_student_home()
                    return
            self.show_message("Sai thông tin học sinh")

        self.root.content = ft.Column(
            [
                ft.Text("Đăng nhập học sinh", size=30),
                self.student_login_name,
                self.student_login_password,
                ft.ElevatedButton("Đăng nhập", on_click=login),
                ft.ElevatedButton("Đăng ký học sinh", on_click=lambda e: self.show_register_student()),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_role_select())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_register_student(self):
        def register(e):
            if (self.student_name.value == "" or
                    self.student_class.value is None or
                    self.student_password.value == ""):
                self.show_message("Vui lòng nhập đầy đủ thông tin")
                return

            if self.student_password.value != self.student_confirm.value:
                self.show_message("Mật khẩu không trùng")
                return

            new_student = {
                "id": self.create_student_id(),
                "name": self.student_name.value,
                "class": self.student_class.value,
                "password": self.student_password.value,
                "score": 0,
                "role": "student"
            }
            self.students.append(new_student)
            self.save_data()
            self.show_message("Đăng ký học sinh thành công")
            self.show_student_login()

        self.root.content = ft.Column(
            [
                ft.Text("Đăng ký học sinh", size=30),
                self.student_name,
                self.student_class,
                self.student_password,
                self.student_confirm,
                ft.ElevatedButton("Đăng ký", on_click=register),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_role_select())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_student_home(self):
        student = self.current_user
        if student is None:
            self.show_role_select()
            return

        score = student.get("score", 0)
        if score >= 8:
            rank = "Giỏi"
        elif score >= 6.5:
            rank = "Khá"
        elif score >= 5:
            rank = "Trung bình"
        else:
            rank = "Yếu"

        student_controls = [
            ft.Text("Thông tin học sinh", size=30),
            ft.Text(f"Mã học sinh: {student.get('id')}"),
            ft.Text(f"Họ tên: {student.get('name')}"),
            ft.Text(f"Lớp: {student.get('class')}"),
            ft.Text(f"Điểm: {score}"),
            ft.Text(f"Xếp loại: {rank}")
        ]

        if student.get("image_proof"):
            student_controls.append(
                ft.Image(src_base64=student.get("image_proof"), width=150, height=150, fit=ft.ImageFit.CONTAIN)
            )

        student_controls.append(
            ft.ElevatedButton(
                "Tải ảnh minh chứng lao động",
                on_click=lambda _: self.file_picker.pick_files(allow_multiple=False,
                                                               file_type=ft.FilePickerFileType.IMAGE)
            )
        )

        student_controls.append(ft.ElevatedButton("Đăng xuất", on_click=lambda e: self.logout()))

        self.root.content = ft.Column(student_controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page.update()

    def show_student_list(self):
        data = []
        for student in self.students:
            if student.get("role") == "student":
                row_controls = [
                    ft.Text(
                        f"{student.get('id')} - {student.get('name')} - Lớp {student.get('class')} - Điểm {student.get('score')}")
                ]
                if student.get("image_proof"):
                    row_controls.append(
                        ft.Image(src_base64=student.get("image_proof"), width=40, height=40, fit=ft.ImageFit.CONTAIN)
                    )
                data.append(ft.Row(row_controls, alignment=ft.MainAxisAlignment.CENTER))

        self.root.content = ft.Column(
            [
                ft.Text("Danh sách học sinh", size=30),
                *data,
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_admin_home())
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_add_student(self):
        def add_student(e):
            try:
                score = int(self.new_score.value)
            except:
                score = 0

            new_student = {
                "id": self.new_id.value if self.new_id.value != "" else self.create_student_id(),
                "name": self.new_name.value,
                "class": "Chưa có",
                "password": "123456",
                "score": score,
                "role": "student"
            }
            self.students.append(new_student)
            self.save_data()
            self.show_message("Đã thêm học sinh")
            self.show_student_list()

        self.root.content = ft.Column(
            [
                ft.Text("Thêm học sinh", size=30),
                self.new_id,
                self.new_name,
                self.new_score,
                ft.ElevatedButton("Thêm", on_click=add_student),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_admin_home())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_update_score(self):
        def update(e):
            try:
                score = int(self.edit_score.value)
            except:
                self.show_message("Điểm phải là số")
                return
            self.update_score(self.edit_student_id.value, score)
            self.show_message("Cập nhật điểm thành công")

        self.root.content = ft.Column(
            [
                ft.Text("Nâng điểm học sinh", size=30),
                self.edit_student_id,
                self.edit_score,
                ft.ElevatedButton("Cập nhật", on_click=update),
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_admin_home())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def update_score(self, student_id, score):
        for student in self.students:
            if student.get("id") == student_id and student.get("role") == "student":
                student["score"] = score
                self.save_data()
                return
        self.show_message("Không tìm thấy học sinh")

    def search_student(self, keyword):
        result = []
        for student in self.students:
            if student.get("role") == "student":
                name = student.get("name", "").lower()
                sid = student.get("id", "").lower()
                if keyword.lower() in name or keyword.lower() in sid:
                    result.append(student)
        return result

    def show_search_student(self):
        keyword = ft.TextField(label="Nhập tên hoặc mã học sinh")
        result_column = ft.Column()

        def search(e):
            result_column.controls.clear()
            students = self.search_student(keyword.value)
            for student in students:
                result_column.controls.append(
                    ft.Text(f"{student.get('id')} - {student.get('name')} - Điểm {student.get('score')}")
                )
            self.page.update()

        self.root.content = ft.Column(
            [
                ft.Text("Tìm kiếm học sinh", size=30),
                keyword,
                ft.ElevatedButton("Tìm", on_click=search),
                result_column,
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_admin_home())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def show_manage_student(self):
        students_view = []
        for student in self.students:
            if student.get("role") == "student":
                students_view.append(
                    ft.Row(
                        [
                            ft.Text(f"{student.get('id')} - {student.get('name')} - Điểm {student.get('score')}"),
                            ft.ElevatedButton("Xóa", on_click=lambda e, sid=student.get("id"): self.delete_student(sid))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )

        self.root.content = ft.Column(
            [
                ft.Text("Quản lý học sinh", size=30),
                *students_view,
                ft.ElevatedButton("Quay lại", on_click=lambda e: self.show_admin_home())
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page.update()

    def delete_student(self, student_id):
        for student in self.students:
            if student.get("id") == student_id and student.get("role") == "student":
                self.students.remove(student)
                break
        self.save_data()
        self.show_manage_student()

    def create_student_id(self):
        number = 1
        while True:
            new_id = "HS" + str(number).zfill(2)
            exists = False
            for student in self.students:
                if student.get("id") == new_id:
                    exists = True
                    break
            if exists == False:
                return new_id
            number += 1

    def get_students(self):
        result = []
        for student in self.students:
            if student.get("role") == "student":
                result.append(student)
        return result

    def show_message(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def logout(self):
        self.current_user = None
        self.admin_key_login.value = ""
        self.student_login_name.value = ""
        self.student_login_password.value = ""
        self.show_role_select()

    def clear_student_login(self):
        self.student_login_name.value = ""
        self.student_login_password.value = ""
        self.page.update()

    def start(self):
        self.load_data()
        self.show_role_select()