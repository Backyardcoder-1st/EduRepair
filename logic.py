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

        # Khởi tạo khung chứa chính công khai
        self.root = ft.Container()

        # Đường link Firebase giải mã an toàn
        self.db_url = base64.b64decode(
            "aHR0cHM6Ly9icm90aGVyczFnb2FsLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbS9zdHVkZW50cy5qc29u").decode("utf-8")

        self.students = []
        self.current_user = None
        self.admin_key = "123"
        self.file_picker = None  # Sẽ khởi tạo an toàn ở hàm start()

        # ================= KHAI BÁO ĐẦY ĐỦ CÁC Ô NHẬP LIỆU ORIGINAL =================
        self.admin_key_login = ft.TextField(label="Nhập key Admin", password=True, can_reveal_password=True)
        self.student_login_name = ft.TextField(label="Tên học sinh")
        self.student_login_password = ft.TextField(label="Mật khẩu học sinh", password=True, can_reveal_password=True)

        self.student_name = ft.TextField(label="Họ và tên học sinh")
        self.student_class = ft.TextField(label="Lớp học")
        self.student_password = ft.TextField(label="Mật khẩu tài khoản", password=True)
        self.student_confirm = ft.TextField(label="Xác nhận mật khẩu", password=True)

        self.new_id = ft.TextField(label="Mã số (Để trống để tự tạo)")
        self.new_name = ft.TextField(label="Họ tên học sinh mới")
        self.new_score = ft.TextField(label="Điểm số ban đầu")

        self.edit_student_id = ft.TextField(label="Mã học sinh cần nâng điểm")
        self.edit_score = ft.TextField(label="Điểm mới")

    # ================= HÀM XỬ LÝ ẢNH MINH CHỨNG =================
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            picked_file = e.files[0]
            try:
                with open(picked_file.path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                if self.current_user and self.current_user.get("role") == "student":
                    self.current_user["image_proof"] = encoded_string
                    for student in self.students:
                        if student.get("id") == self.current_user.get("id"):
                            student["image_proof"] = encoded_string
                            break
                    self.save_data()

                self.show_message("Đã tải ảnh minh chứng lên hệ thống thành công!")
                self.show_student_home()
            except Exception as ex:
                self.show_message("Không thể đọc file ảnh này!")

    # ================= HÀM KIỂM TRA & VALIDATION =================
    def check_score(self, score):
        try:
            score = float(score)
        except:
            return False
        if score < 0 or score > 10:
            return False
        return True

    def validate_student_register(self):
        if self.student_name.value.strip() == "":
            return False, "Chưa nhập họ tên"
        if self.student_class.value.strip() == "":
            return False, "Chưa nhập lớp học"
        if self.student_password.value == "":
            return False, "Chưa nhập mật khẩu"
        if self.student_password.value != self.student_confirm.value:
            return False, "Mật khẩu xác nhận không khớp"
        return True, ""

    # ================= HÀM CLEAR FORM SYSTEMS =================
    def clear_student_login(self):
        self.student_login_name.value = ""
        self.student_login_password.value = ""
        self.page.update()

    def clear_all_form(self):
        self.admin_key_login.value = ""
        self.student_login_name.value = ""
        self.student_login_password.value = ""
        self.student_name.value = ""
        self.student_class.value = ""
        self.student_password.value = ""
        self.student_confirm.value = ""
        self.new_id.value = ""
        self.new_name.value = ""
        self.new_score.value = ""
        self.edit_student_id.value = ""
        self.edit_score.value = ""
        self.page.update()

    # ================= DATABASE ENGINE (LOAD / SAVE) =================
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

    # ================= GIAO DIỆN CHỨC NĂNG VÀ ĐIỀU HƯỚNG =================
    def show_role_select(self):
        self.root.content = ft.Column(
            [
                ft.Text("Bạn là ai?", size=30, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Admin", on_click=lambda e: self.show_admin_login(), width=200),
                ft.ElevatedButton("Học sinh", on_click=lambda e: self.show_student_login(), width=200)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
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
                ft.Text("Đăng nhập Admin", size=30, weight=ft.FontWeight.BOLD),
                self.admin_key_login,
                ft.ElevatedButton("Đăng nhập", on_click=login, width=150),
                ft.TextButton("Quay lại", on_click=lambda e: self.show_role_select())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
        self.page.update()

    def show_admin_home(self):
        self.root.content = ft.Column(
            [
                ft.Text("Trang Quản Trị Admin", size=30, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Danh sách học sinh", on_click=lambda e: self.show_student_list(), width=250),
                ft.ElevatedButton("Thêm học sinh mới", on_click=lambda e: self.show_add_student(), width=250),
                ft.ElevatedButton("Quản lý / Xóa học sinh", on_click=lambda e: self.show_manage_student(), width=250),
                ft.ElevatedButton("Nâng / Sửa điểm số", on_click=lambda e: self.show_update_score(), width=250),
                ft.ElevatedButton("Tìm kiếm học sinh", on_click=lambda e: self.show_search_student(), width=250),
                ft.ElevatedButton("Đăng xuất hệ thống", on_click=lambda e: self.logout(), bgcolor=ft.Colors.RED_100,
                                  color=ft.Colors.RED)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
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
            self.show_message("Sai thông tin học sinh hoặc mật khẩu")

        self.root.content = ft.Column(
            [
                ft.Text("Đăng nhập học sinh", size=30, weight=ft.FontWeight.BOLD),
                self.student_login_name,
                self.student_login_password,
                ft.ElevatedButton("Đăng nhập", on_click=login, width=150),
                ft.ElevatedButton("Đăng ký tài khoản mới", on_click=lambda e: self.show_register_student(), width=200),
                ft.TextButton("Quay lại", on_click=lambda e: self.show_role_select())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
        self.page.update()

    def show_register_student(self):
        def register(e):
            is_valid, msg = self.validate_student_register()
            if not is_valid:
                self.show_message(msg)
                return

            new_student = {
                "id": self.create_student_id(),
                "name": self.student_name.value,
                "class": self.student_class.value,
                "password": self.student_password.value,
                "score": 0,
                "role": "student",
                "image_proof": ""
            }
            self.students.append(new_student)
            self.save_data()
            self.show_message("Đăng ký tài khoản thành công!")
            self.show_student_login()

        self.root.content = ft.Column(
            [
                ft.Text("Đăng ký học sinh", size=30, weight=ft.FontWeight.BOLD),
                self.student_name,
                self.student_class,
                self.student_password,
                self.student_confirm,
                ft.ElevatedButton("Hoàn tất đăng ký", on_click=register, width=200),
                ft.TextButton("Quay lại", on_click=lambda e: self.show_student_login())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
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
            ft.Text("Thông tin học sinh", size=30, weight=ft.FontWeight.BOLD),
            ft.Text(f"Mã định danh: {student.get('id')}", size=16),
            ft.Text(f"Họ tên học sinh: {student.get('name')}", size=16),
            ft.Text(f"Lớp hiện tại: {student.get('class')}", size=16),
            ft.Text(f"Điểm số tích lũy: {score}", size=16),
            ft.Text(f"Xếp loại học lực: {rank}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
        ]

        if student.get("image_proof"):
            student_controls.append(
                ft.Image(src_base64=student.get("image_proof"), width=150, height=150, fit=ft.ImageFit.CONTAIN)
            )

        # PATCHED STABLE BLOCK HERE (Resolves Unresolved reference error)
        if self.file_picker is not None:
            student_controls.append(
                ft.ElevatedButton(
                    "Tải ảnh minh chứng lao động",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda e: self.file_picker.pick_files(
                        allow_multiple=False,
                        file_type=ft.FilePickerFileType.IMAGE
                    )
                )
            )
        else:
            student_controls.append(
                ft.Text("Tính năng tải ảnh minh chứng không hỗ trợ trên trình duyệt này.", color=ft.Colors.GREY)
            )

        student_controls.append(
            ft.ElevatedButton("Đăng xuất", on_click=lambda e: self.logout(), bgcolor=ft.Colors.RED_500,
                              color=ft.Colors.WHITE)
        )

        self.root.content = ft.Column(student_controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12)
        self.page.update()

    def show_student_list(self):
        data = []
        for student in self.students:
            if student.get("role") == "student":
                row_controls = [
                    ft.Text(
                        f"{student.get('id')} - {student.get('name')} - Lớp {student.get('class')} - Điểm: {student.get('score')}")
                ]
                if student.get("image_proof"):
                    row_controls.append(
                        ft.Image(src_base64=student.get("image_proof"), width=40, height=40, fit=ft.ImageFit.CONTAIN)
                    )
                data.append(ft.Row(row_controls, alignment=ft.MainAxisAlignment.CENTER, spacing=15))

        self.root.content = ft.Column(
            [
                ft.Text("Danh sách học sinh", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(content=ft.Column(data, spacing=10), padding=10),
                ft.ElevatedButton("Quay lại Menu", on_click=lambda e: self.show_admin_home())
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
        self.page.update()

    def show_add_student(self):
        def add_student(e):
            if not self.check_score(self.new_score.value):
                self.show_message("Điểm số ban đầu không hợp lệ (Phải từ 0 đến 10)")
                return

            new_student = {
                "id": self.new_id.value.strip() if self.new_id.value.strip() != "" else self.create_student_id(),
                "name": self.new_name.value.strip(),
                "class": "Chưa xếp lớp",
                "password": "123456",
                "score": float(self.new_score.value),
                "role": "student",
                "image_proof": ""
            }
            self.students.append(new_student)
            self.save_data()
            self.show_message("Đã thêm thông tin học sinh thành công!")
            self.show_student_list()

        self.root.content = ft.Column(
            [
                ft.Text("Thêm học sinh mới", size=30, weight=ft.FontWeight.BOLD),
                self.new_id,
                self.new_name,
                self.new_score,
                ft.ElevatedButton("Thêm học sinh", on_click=add_student, width=150),
                ft.TextButton("Quay lại", on_click=lambda e: self.show_admin_home())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )
        self.page.update()

    def show_update_score(self):
        def update(e):
            if not self.check_score(self.edit_score.value):
                self.show_message("Điểm nhập vào phải nằm trong khoảng từ 0 đến 10")
                return

            for student in self.students:
                if student.get("id") == self.edit_student_id.value.strip() and student.get("role") == "student":
                    student["score"] = float(self.edit_score.value)
                    self.save_data()
                    self.show_message("Cập nhật điểm thành công!")
                    self.show_admin_home()
                    return
            self.show_message("Không tìm thấy mã học sinh phù hợp")

        self.root.content = ft.Column(
            [
                ft.Text("Cập nhật điểm số", size=30, weight=ft.FontWeight.BOLD),
                self.edit_student_id,
                self.edit_score,
                ft.ElevatedButton("Cập nhật điểm", on_click=update, width=150),
                ft.TextButton("Quay lại", on_click=lambda e: self.show_admin_home())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )
        self.page.update()

    def show_search_student(self):
        keyword = ft.TextField(label="Nhập tên hoặc mã học sinh tìm kiếm")
        result_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)

        def search(e):
            result_column.controls.clear()
            search_key = keyword.value.strip().lower()
            for student in self.students:
                if student.get("role") == "student":
                    name = student.get("name", "").lower()
                    sid = student.get("id", "").lower()
                    if search_key in name or search_key in sid:
                        result_column.controls.append(
                            ft.Text(f"{student.get('id')} - {student.get('name')} - Điểm số: {student.get('score')}",
                                    size=16)
                        )
            if not result_column.controls:
                result_column.controls.append(ft.Text("Không tìm thấy kết quả trùng khớp.", color=ft.Colors.GREY))
            self.page.update()

        self.root.content = ft.Column(
            [
                ft.Text("Tìm kiếm thông tin", size=30, weight=ft.FontWeight.BOLD),
                keyword,
                ft.ElevatedButton("Tìm kiếm", on_click=search, width=120),
                ft.Divider(),
                result_column,
                ft.TextButton("Quay lại Menu", on_click=lambda e: self.show_admin_home())
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12
        )
        self.page.update()

    def show_manage_student(self):
        students_view = []
        for student in self.students:
            if student.get("role") == "student":
                students_view.append(
                    ft.Row(
                        [
                            ft.Text(f"{student.get('id')} - {student.get('name')} - Lớp: {student.get('class')}"),
                            ft.ElevatedButton("Xóa", on_click=lambda e, sid=student.get("id"): self.delete_student(sid),
                                              bgcolor=ft.Colors.RED_50)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20
                    )
                )

        self.root.content = ft.Column(
            [
                ft.Text("Quản lý hồ sơ học sinh", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(content=ft.Column(students_view, spacing=8), padding=10),
                ft.ElevatedButton("Quay lại Menu", on_click=lambda e: self.show_admin_home())
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
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
            exists = any(s.get("id") == new_id for s in self.students)
            if not exists:
                return new_id
            number += 1

    def get_students(self):
        return [s for s in self.students if s.get("role") == "student"]

    def show_message(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def logout(self):
        self.current_user = None
        self.clear_all_form()
        self.show_role_select()

    def start(self):
        # KHÓA TUYỆT ĐỐI: Nếu chạy trên trình duyệt (Web), không bao giờ tạo FilePicker
        if hasattr(self.page, "web") and self.page.web:
            self.file_picker = None
        else:
            try:
                self.file_picker = ft.FilePicker()
                self.file_picker.on_result = self.on_file_picked

                if self.file_picker not in self.page.overlay:
                    self.page.overlay.append(self.file_picker)
            except:
                self.file_picker = None

        # Tải dữ liệu và hiển thị giao diện chính
        self.load_data()
        self.show_role_select()