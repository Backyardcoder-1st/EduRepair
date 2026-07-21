import flet as ft
import json
import os
import urllib.request
import urllib.error
import ssl
import base64

try:
    _context = ssl.create_default_context()
except:
    _context = None


class AppController:

    def __init__(self, page: ft.Page):

        self.page = page

        # =========================
        # CÀI ĐẶT TRANG WEB
        # =========================

        self.page.title = "Quản lý học sinh"

        self.page.bgcolor = "#F1F5F9"

        self.page.padding = 0

        self.root = ft.Container(

            expand=True

        )

        # =========================
        # MÀU GIAO DIỆN
        # =========================

        self.blue = "#2563EB"

        self.green = "#16A34A"

        self.orange = "#EA580C"

        self.red = "#DC2626"

        self.gray = "#64748B"

        self.dark = "#0F172A"

        self.white = "#FFFFFF"

        # =========================
        # DATABASE
        # =========================

        self.file = "students.json"

        self.db_url = base64.b64decode(

            "aHR0cHM6Ly9icm90aGVyczFnb2FsLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbS9zdHVkZW50cy5qc29u"

        ).decode()

        self.students = []

        self.current_user = None

        # key admin

        self.admin_key = "123"

        # =========================
        # TẠO CARD GIAO DIỆN
        # =========================

        def create_card(content, width=500):
            return ft.Container(

                content=content,

                width=width,

                padding=25,

                bgcolor=self.white,

                border_radius=15,

                shadow=ft.BoxShadow(

                    blur_radius=15,

                    offset=ft.Offset(0, 5)

                )

            )

        self.card = create_card

        # =========================
        # TẠO TIÊU ĐỀ
        # =========================

        def title(text):
            return ft.Text(

                text,

                size=30,

                weight=ft.FontWeight.BOLD,

                color=self.dark

            )

        self.title = title

        # =========================
        # NÚT CHUNG
        # =========================

        def button(text, click, color=None):
            return ft.ElevatedButton(

                text,

                width=260,

                bgcolor=color or self.blue,

                color="white",

                on_click=click

            )

        self.button = button

        # =========================
        # FORM LOGIN
        # =========================

        self.admin_key_login = ft.TextField(

            label="Key Admin",

            password=True,

            filled=True

        )

        self.student_login_name = ft.TextField(

            label="Tên học sinh",

            filled=True

        )

        self.student_login_password = ft.TextField(

            label="Mật khẩu",

            can_reveal_password=True,

            password=True,

            filled=True

        )

        # =========================
        # FORM ĐĂNG KÝ
        # =========================

        self.student_name = ft.TextField(

            label="Họ tên",

            filled=True

        )

        self.student_class = ft.Dropdown(

            label="Lớp",

            filled=True,
            options=[
                ft.dropdown.Option("A1"),
                ft.dropdown.Option("A2"),
                ft.dropdown.Option("A3"),
                ft.dropdown.Option("A4"),
                ft.dropdown.Option("A5"),
                ft.dropdown.Option("A6"),
                ft.dropdown.Option("A7"),
                ft.dropdown.Option("A8"),
                ft.dropdown.Option("A9"),
                ft.dropdown.Option("A10"),
            ]

        )

        self.student_password = ft.TextField(

            label="Mật khẩu",
            can_reveal_password=True,

            password=True,

            filled=True

        )

        self.student_confirm = ft.TextField(

            label="Nhập lại mật khẩu",

            password=True,

            filled=True

        )

        self.login_error_text = ft.Text("", color=self.red, size=14, weight=ft.FontWeight.BOLD)
        self.register_error_text = ft.Text("", color=self.red, size=14, weight=ft.FontWeight.BOLD)

        # =========================
        # FORM ADMIN
        # =========================

        self.new_id = ft.TextField(

            label="Mã học sinh",

            filled=True

        )

        self.new_name = ft.TextField(

            label="Tên học sinh",

            filled=True

        )

        self.new_score = ft.TextField(

            label="Điểm",

            filled=True

        )

        self.edit_student_id = ft.TextField(

            label="Mã học sinh",

            filled=True

        )

        self.edit_score = ft.TextField(

            label="Điểm mới",

            filled=True

        )

        # =========================
        # ẢNH
        # =========================

        self.image_path = ft.TextField(

            label="Đường dẫn ảnh",

            filled=True

        )

    # =========================
    # THÔNG BÁO
    # =========================

    def show_message(self, text):

        try:

            self.page.snack_bar = ft.SnackBar(

                content=ft.Text(text)

            )

            self.page.snack_bar.open = True

            self.page.update()

        except:

            pass

    # =========================
    # ĐỌC DỮ LIỆU FIREBASE + LOCAL
    # =========================

    def load_data(self):
        self.students = []
        try:
            request = urllib.request.Request(
                self.db_url,
                method="GET"
            )
            with urllib.request.urlopen(
                    request,
                    timeout=8,
                    context=_context
            ) as response:
                data = json.loads(response.read().decode())
                if isinstance(data, dict):
                    self.students = list(data.values())
                elif isinstance(data, list):
                    self.students = data
                print("Firebase load thành công")
        except Exception as e:
            print("Firebase đọc lỗi:", e)

        if len(self.students) == 0:
            try:
                if os.path.exists(self.file):
                    with open(self.file, "r", encoding="utf-8") as f:
                        self.students = json.load(f)
                    print("Load file local")
            except Exception as e:
                print("Local lỗi:", e)

        if len(self.students) == 0:
            self.students = [
                {
                    "id": "HS01",
                    "name": "Nguyễn Văn A",
                    "class": "A1",
                    "password": "123456",
                    "score": 8,
                    "role": "student",
                    "image": ""
                },
                {
                    "id": "HS02",
                    "name": "Trần Thị B",
                    "class": "A1",
                    "password": "123456",
                    "score": 6,
                    "role": "student",
                    "image": ""
                }
            ]
            self.save_data()

        # AUTOMATIC DATABASE INJECTION FOR THE TEST STUDENT PROFILE:
        # If the test account ID "TEST01" does not exist, append it and sync both local .json and firebase
        has_test_student = any(isinstance(s, dict) and s.get("id") == "TEST01" for s in self.students)
        if not has_test_student:
            self.students.append({
                "id": "TEST01",
                "name": "Học Sinh Thử Nghiệm",
                "class": "11A1",
                "password": "123",
                "score": 10,
                "role": "student",
                "image": ""
            })
            self.save_data()  # Forces a persistent write to students.json locally

    # =========================
    # LƯU LOCAL
    # =========================

    def backup_local(self):

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

                    indent=4

                )

            print(

                "Backup local OK"

            )

        except Exception as e:

            print(

                "Backup lỗi:",

                e

            )

    # =========================
    # ĐỒNG BỘ FIREBASE
    # =========================

    def sync_firebase(self):

        try:

            data = json.dumps(

                self.students,

                ensure_ascii=False

            ).encode("utf-8")

            request = urllib.request.Request(

                self.db_url,

                data=data,

                method="PUT",

                headers={

                    "Content-Type":

                        "application/json"

                }

            )

            with urllib.request.urlopen(

                    request,

                    timeout=8,

                    context=_context

            ) as response:

                print(

                    "Firebase sync OK"

                )

                return True

        except Exception as e:

            print(

                "Firebase sync lỗi:",

                e

            )

            return False

    # =========================
    # SAVE CHÍNH
    # =========================

    def save_data(self):

        self.backup_local()

        ok = self.sync_firebase()

        if ok:

            print(

                "Đã lưu lên web"

            )

        else:

            print(

                "Chỉ lưu local"

            )

    # =========================
    # START APP
    # =========================

    def start(self):

        self.load_data()

        self.check_data()

        self.show_role_select()

    # =========================
    # KIỂM TRA DỮ LIỆU
    # =========================

    def check_data(self):
        if self.students is None:
            self.students = []

        if not isinstance(self.students, list):
            if isinstance(self.students, dict):
                self.students = list(self.students.values())
            else:
                self.students = []

        # CLEANUP HOLES: Filter out any None or non-dictionary entries to prevent app crashes
        self.students = [student for student in self.students if isinstance(student, dict)]

        for student in self.students:
            if "role" not in student:
                student["role"] = "student"

            if "score" not in student:
                student["score"] = 0

            if "image" not in student:
                student["image"] = ""

    # =========================
    # TẠO ID HỌC SINH
    # =========================

    def generate_student_id(self, class_name):
        if not class_name:
            return "HS01"

        # Normalize the class input name (e.g., "a1" -> "A1")
        target_class = str(class_name).strip().upper()

        existing_numbers = []

        # Look through database to find numbers used ONLY within this specific class
        for student in self.students:
            if not isinstance(student, dict) or student.get("role") != "student":
                continue

            st_class = str(student.get("class", "")).strip().upper()
            if st_class == target_class:
                st_id = str(student.get("id", "")).strip().upper()

                # Check if it follows the "HSxx" pattern
                if st_id.startswith("HS"):
                    try:
                        # Extract the numeric string part (e.g., "HS02" -> 2)
                        num = int(st_id[2:])
                        existing_numbers.append(num)
                    except ValueError:
                        pass  # Ignore custom formatted IDs that aren't pure integers

        # If this is the very first student entering this specific class section
        if not existing_numbers:
            return "HS01"

        # Grab the highest current number in this class and increment it
        next_number = max(existing_numbers) + 1
        return f"HS{next_number:02d}"

    # =========================
    # KIỂM TRA ĐIỂM
    # =========================

    def check_score(self, score):

        try:

            score = float(score)

        except:

            return False

        return 0 <= score <= 10

    # =========================
    # KIỂM TRA ĐĂNG KÝ
    # =========================

    def validate_student_register(self):
        name = self.student_name.value.strip()
        cls = self.student_class.value
        password = self.student_password.value

        if name == "":
            return False, "Chưa nhập họ tên"

        if cls is None or cls == "":
            return False, "Chưa chọn lớp học"

        if password == "":
            return False, "Chưa nhập mật khẩu"

        if password != self.student_confirm.value:
            return False, "Sai mật khẩu"

        for student in self.students:
            if (
                    student.get("name") == name
                    and
                    student.get("class") == cls
            ):
                return False, "Tài khoản đã tồn tại"

        return True, ""

    # =========================
    # XÓA FORM
    # =========================

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

        self.image_path.value = ""

        try:

            self.page.update()

        except:

            pass

    # =========================
    # MÀN HÌNH CHỌN VAI TRÒ
    # =========================

    def show_role_select(self):
        body = ft.Column(
            controls=[
                ft.Container(
                    width=90,
                    height=90,
                    alignment=ft.alignment.Alignment(0, 0),
                    content=ft.Image(
                        src="LOGO.png",
                        width=90,
                        height=90,
                    )
                ),
                ft.Text(
                    "EduRepair",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.dark,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Hệ thống quản lí-đăng kí lao động",
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=self.dark,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Chọn quyền truy cập",
                    size=15,
                    color=self.dark,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=10),

                ft.Container(
                    width=340,
                    height=100,
                    bgcolor="#F8FAFC",
                    border_radius=12,
                    padding=10,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=50,
                                height=50,
                                content=ft.Image(
                                    src="ADMIN.png",
                                    width=50,
                                    height=50,
                                )
                            ),
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text("ADMIN", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Quản lý dữ liệu", size=11, color=self.gray),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.ElevatedButton(
                                "Đăng nhập",
                                bgcolor=self.blue,
                                color="white",
                                on_click=lambda e: self.show_admin_login(),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.Padding(8, 8, 8, 8)
                                )
                            )
                        ]
                    )
                ),
                ft.Container(height=8),

                ft.Container(
                    width=340,
                    height=100,
                    bgcolor="#F8FAFC",
                    border_radius=12,
                    padding=10,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=50,
                                height=50,
                                content=ft.Image(
                                    src="STUDENT.png",
                                    width=50,
                                    height=50,
                                )
                            ),
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text("HỌC SINH", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Thực hiện lao động", size=11, color=self.gray),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.ElevatedButton(
                                "Đăng nhập",
                                bgcolor=self.green,
                                color="white",
                                on_click=lambda e: self.show_student_login(),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.Padding(8, 8, 8, 8)
                                )
                            )
                        ]
                    )
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(body, 380)
        self.page.update()

    # =========================
    # TRANG ĐĂNG NHẬP ADMIN
    # =========================

    def show_admin_login(self):

        def login(e):
            key = self.admin_key_login.value.strip()

            if key == self.admin_key:
                self.current_user = {
                    "role": "admin",
                    "name": "Võ Thị Yến Nhi"
                }
                self.show_admin_home()
            else:
                self.show_message(
                    "Sai mã bảo mật Admin!"
                )

        body = ft.Column(
            controls=[
                self.title(
                    "ĐĂNG NHẬP ADMIN"
                ),

                ft.Text(
                    "Nhập khóa cấu hình hệ thống",
                    size=13,
                    color=self.dark,
                    text_align=ft.TextAlign.CENTER
                ),

                ft.Container(height=10),

                self.admin_key_login,

                ft.Container(height=10),

                self.button(
                    "Đăng nhập",
                    login,
                    self.blue
                ),

                ft.TextButton(
                    "Quay lại",
                    on_click=lambda e: self.show_role_select()
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(body, 380)
        self.page.update()

    # =========================
    # ĐĂNG NHẬP HỌC SINH
    # =========================
    def show_student_login(self):
        self.login_error_text.value = ""

        def login(e):
            name = self.student_login_name.value.strip()
            password = self.student_login_password.value

            for student in self.students:
                if (
                        student.get("name") == name
                        and
                        student.get("password") == password
                ):
                    self.current_user = student
                    self.show_student_home()
                    return

            self.login_error_text.value = "Sai tên người dùng hoặc mật khẩu"
            self.page.update()

        body = ft.Column(
            controls=[
                self.title(
                    "ĐĂNG NHẬP HỌC SINH"
                ),

                self.student_login_name,

                self.student_login_password,

                self.login_error_text,

                self.button(
                    "Đăng nhập",
                    login,
                    self.green
                ),

                self.button(
                    "Đăng ký",
                    lambda e: self.show_register_student(),
                    self.orange
                ),

                ft.TextButton(
                    "Quay lại",
                    on_click=lambda e: self.show_role_select()
                )

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(body, 380)
        self.page.update()

    # =========================
    # ĐĂNG KÝ HỌC SINH
    # =========================
    def show_register_student(self):
        self.register_error_text.value = ""

        def register(e):
            ok, msg = self.validate_student_register()

            if ok == False:
                self.register_error_text.value = msg
                self.page.update()
                return

            student = {
                "id": self.generate_student_id(self.student_class.value),
                "name": self.student_name.value.strip(),
                "class": self.student_class.value,
                "password": self.student_password.value,
                "score": 0,
                "role": "student",
                "image": ""
            }

            self.students.append(student)

            self.save_data()

            self.show_message(
                "Đăng ký thành công"
            )

            self.show_student_login()

        body = ft.Column(
            controls=[
                self.title(
                    "ĐĂNG KÝ HỌC SINH"
                ),

                self.student_name,

                self.student_class,

                self.student_password,

                self.student_confirm,

                self.register_error_text,

                self.button(
                    "Hoàn tất",
                    register,
                    self.green
                ),

                ft.TextButton(
                    "Quay lại",
                    on_click=lambda e: self.show_student_login()
                )

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(body, 380)
        self.page.update()

    # =========================
    # ĐỌC ẢNH
    # =========================
    def read_image(self, path):

        try:

            with open(
                    path,
                    "rb"
            ) as image:
                data = base64.b64encode(
                    image.read()
                )

                return data.decode()

        except Exception as e:

            print(
                "Ảnh lỗi:",
                e
            )

            return ""

    # =========================
    # LƯU ẢNH HỌC SINH
    # =========================
    def save_student_image(self):

        if self.current_user is None:
            return

        path = self.image_path.value.strip()

        if path == "":
            self.show_message(
                "Chưa nhập đường dẫn ảnh"
            )

            return

        image = self.read_image(path)

        if image == "":
            self.show_message(
                "Không đọc được ảnh"
            )

            return

        for student in self.students:

            if student.get("id") == self.current_user.get("id"):
                student["image"] = image

                self.current_user = student

                self.save_data()

                self.show_message(
                    "Đã cập nhật ảnh"
                )

                self.show_student_home()

                return

    # =========================
    # TRANG ADMIN DASHBOARD
    # =========================
    def show_admin_home(self):

        profile_header = ft.Container(
            width=340,
            padding=12,
            bgcolor="#F8FAFC",
            border_radius=15,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(
                                width=46,
                                height=46,
                                border_radius=23,
                                content=ft.Image(
                                    src="ADMIN.png",
                                    fit="cover",
                                    width=46,
                                    height=46,
                                    border_radius=23,
                                )
                            ),
                            ft.Column(
                                spacing=1,
                                controls=[
                                    ft.Text("Võ Thị Yến Nhi", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Quản trị viên", size=11, color=self.gray),
                                ]
                            )
                        ]
                    ),
                    ft.Container(
                        on_click=lambda e: self.show_role_select(),
                        padding=ft.Padding(8, 5, 8, 5),
                        border_radius=8,
                        bgcolor="#FEE2E2",
                        content=ft.Text("Đăng xuất", size=11, color=self.red, weight=ft.FontWeight.BOLD)
                    )
                ]
            )
        )

        def feature_card(title, icon_char, color, bg_color, click_handler):
            return ft.Container(
                width=135,
                height=130,
                bgcolor=bg_color,
                border_radius=15,
                padding=12,
                on_click=click_handler,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Container(
                            width=32,
                            height=32,
                            border_radius=8,
                            bgcolor=color,
                            alignment=ft.alignment.Alignment(0, 0),
                            content=ft.Text(
                                icon_char,
                                size=15,
                                color="white",
                                weight=ft.FontWeight.BOLD
                            )
                        ),
                        ft.Text(
                            title,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=self.dark
                        )
                    ]
                )
            )

        sliding_board = ft.Row(
            controls=[
                feature_card("Danh sách đăng kí", "📝", self.blue, "#EFF6FF", lambda e: self.show_admin_registration_list()),
                feature_card("Lớp học", "🏫", "#7C3AED", "#F3E8FF", lambda e: self.show_admin_classes()),
                feature_card("Lỗi vi phạm", "⚠️", self.red, "#FEF2F2", lambda e: self.show_message("Chức năng 'Lỗi vi phạm' đang phát triển!")),
                feature_card("Tiến trình lao động", "⏳", self.orange, "#FFF7ED", lambda e: self.show_message("Chức năng 'Tiến trình' đang phát triển!")),
                feature_card("Kết quả lao động", "✅", self.green, "#F0FDF4", lambda e: self.show_message("Chức năng 'Kết quả' đang phát triển!")),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )

        dashboard_content = ft.Column(
            controls=[
                self.title("BẢNG ĐIỀU KHIỂN"),
                ft.Container(height=5),
                profile_header,
                ft.Container(height=15),
                ft.Row(
                    controls=[
                        ft.Text("Công cụ quản lý", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Cuộn ngang ➔", size=10, color=self.gray)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(height=5),
                sliding_board,
                ft.Container(height=15),
                ft.Container(
                    width=340,
                    padding=12,
                    bgcolor="#F8FAFC",
                    border_radius=12,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text("Tình trạng hệ thống", size=12, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Đang kết nối cơ sở dữ liệu", size=11, color=self.gray)
                                ]
                            ),
                            ft.Text("Hoạt động", size=10, color=self.green, weight=ft.FontWeight.BOLD)
                        ]
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(dashboard_content, 380)
        self.page.update()

        # =========================
        # TRANG XEM LỚP HỌC (ADMIN)
        # =========================
    def show_admin_classes(self):
            self.load_data()
            self.check_data()

            top_bar = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=1,
                        controls=[
                            ft.Text("DANH SÁCH LỚP", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                            ft.Text("Chọn một lớp để xem học sinh", size=11, color=self.gray)
                        ]
                    ),
                    ft.Container(
                        on_click=lambda e: self.show_admin_home(),
                        padding=ft.Padding(10, 6, 10, 6),
                        border_radius=8,
                        bgcolor="#E2E8F0",
                        content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                    )
                ]
            )

            class_buttons = []
            classes = [f"A{i}" for i in range(1, 11)]
            for c in classes:
                class_buttons.append(
                    ft.Container(
                        content=ft.Text(c, weight=ft.FontWeight.BOLD, color="#7C3AED", size=14),
                        alignment=ft.alignment.Alignment(0, 0),
                        width=160,
                        height=52,
                        bgcolor="#F3E8FF",
                        border_radius=12,
                        on_click=lambda e, name=c: self.show_student_list(class_filter=name),
                    )
                )

            grid_rows = []
            for i in range(0, len(class_buttons), 2):
                grid_rows.append(
                    ft.Row(
                        controls=class_buttons[i:i + 2],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=12
                    )
                )

            # Single centralized Delete Account button
            delete_btn = ft.Container(
                on_click=lambda e: self.show_student_list(show_delete_form=True),
                padding=ft.Padding(0, 10, 0, 10),
                border_radius=10,
                bgcolor=self.red,
                alignment=ft.alignment.Alignment(0, 0),
                content=ft.Text("Xoá tài khoản", size=13, color="white", weight=ft.FontWeight.BOLD)
            )

            body = ft.Column(
                controls=[
                    top_bar,
                    ft.Container(height=8),
                    ft.Column(
                        controls=grid_rows,
                        spacing=10,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    ft.Container(height=6),
                    delete_btn
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            self.root.content = self.card(body, 380)
            self.page.update()

    # =========================
    # DANH SÁCH LỚP HỌC (THÊM CHỨC NĂNG TÌM KIẾM VÀ XÓA HỌC SINH)
    # =========================
    def show_student_list(self, class_filter=None, show_delete_form=False, search_query=None, show_search_form=False):
        self.load_data()
        self.check_data()

        display_title = f"LỚP {class_filter.upper()}" if class_filter else "DANH SÁCH LỚP HỌC"

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(display_title, size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                ft.Container(
                    on_click=lambda e: self.show_admin_classes() if class_filter else self.show_admin_home(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",
                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        # ----------------------------------------------------
        # STATE 1: DELETE FORM
        # ----------------------------------------------------
        if show_delete_form:
            name_input = ft.TextField(label="Họ tên học sinh", text_size=12, height=48)
            id_input = ft.TextField(label="Mã ID học sinh", text_size=12, height=48)
            class_dropdown = ft.Dropdown(
                label="Lớp học",
                text_size=12,
                height=48,
                options=[ft.dropdown.Option(f"A{i}") for i in range(1, 11)]
            )
            agree_checkbox = ft.Checkbox(
                label="Tôi đồng ý với quyết định này"
            )
            error_msg = ft.Text("", color=self.red, size=11, weight=ft.FontWeight.BOLD)

            def process_deletion(e):
                if not agree_checkbox.value:
                    error_msg.value = "Lỗi: Bạn phải tích xác nhận đồng ý!"
                    self.page.update()
                    return

                typed_name = name_input.value.strip().lower() if name_input.value else ""
                typed_id = id_input.value.strip().upper() if id_input.value else ""
                typed_class = class_dropdown.value

                if not typed_name or not typed_id or not typed_class:
                    error_msg.value = "Lỗi: Vui lòng điền đầy đủ 3 trường!"
                    self.page.update()
                    return

                account_found = False
                for existing_student in self.students[:]:
                    if existing_student.get("role") != "student":
                        continue

                    db_id = str(existing_student.get("id", "")).strip().upper()
                    db_name = str(existing_student.get("name", "")).strip().lower()
                    db_class = str(existing_student.get("class", "")).strip().upper()

                    if db_id == typed_id and db_name == typed_name and db_class == typed_class.upper():
                        self.students.remove(existing_student)
                        account_found = True
                        break

                if account_found:
                    self.save_data()
                    self.show_message(f"Đã xoá vĩnh viễn tài khoản {typed_id}.")
                    self.show_student_list(class_filter, show_delete_form=False)
                else:
                    error_msg.value = "Lỗi: Thông tin không khớp với học sinh nào!"
                    self.page.update()

            delete_form_content = ft.Column(
                spacing=10,
                controls=[
                    top_bar,
                    ft.Text("XÁC NHẬN XOÁ TÀI KHOẢN", size=13, weight=ft.FontWeight.BOLD, color=self.red),
                    name_input,
                    id_input,
                    class_dropdown,
                    agree_checkbox,
                    error_msg,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.TextButton(
                                "Hủy bỏ",
                                on_click=lambda e: self.show_student_list(class_filter, show_delete_form=False)
                            ),
                            ft.ElevatedButton(
                                "Xoá vĩnh viễn",
                                bgcolor=self.red,
                                color="white",
                                on_click=process_deletion
                            )
                        ]
                    )
                ]
            )
            self.root.content = self.card(delete_form_content, 380)
            self.page.update()

        # ----------------------------------------------------
        # STATE 2: SEARCH FORM (INPUT NAME ONLY)
        # ----------------------------------------------------
        elif show_search_form:
            name_input = ft.TextField(label="Họ tên học sinh", text_size=12, height=48)
            error_msg = ft.Text("", color=self.red, size=11, weight=ft.FontWeight.BOLD)

            def process_search(e):
                typed_name = name_input.value.strip() if name_input.value else ""
                if not typed_name:
                    error_msg.value = "Lỗi: Vui lòng nhập tên học sinh!"
                    self.page.update()
                    return

                # Re-render show_student_list with search_query
                self.show_student_list(class_filter=class_filter, search_query=typed_name)

            search_form_content = ft.Column(
                spacing=12,
                controls=[
                    top_bar,
                    ft.Text("TÌM KIẾM HỌC SINH", size=13, weight=ft.FontWeight.BOLD, color=self.blue),
                    name_input,
                    error_msg,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.TextButton(
                                "Hủy bỏ",
                                on_click=lambda e: self.show_student_list(class_filter)
                            ),
                            ft.ElevatedButton(
                                "Tìm kiếm",
                                bgcolor=self.blue,
                                color="white",
                                on_click=process_search
                            )
                        ]
                    )
                ]
            )
            self.root.content = self.card(search_form_content, 380)
            self.page.update()

        # ----------------------------------------------------
        # STATE 3: SEARCH RESULTS PAGE
        # ----------------------------------------------------
        elif search_query is not None:
            results_top_bar = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(f"KẾT QUẢ: '{search_query}'", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                    ft.Container(
                        on_click=lambda e: self.show_student_list(class_filter, show_search_form=True),
                        padding=ft.Padding(10, 6, 10, 6),
                        border_radius=8,
                        bgcolor="#E2E8F0",
                        content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                    )
                ]
            )

            rows = []
            q_str = search_query.strip().lower()

            found_students = []
            for student in self.students:
                if student.get("role") != "student":
                    continue
                db_name = str(student.get("name", "")).strip().lower()
                if q_str in db_name:
                    found_students.append(student)

            if not found_students:
                rows.append(
                    ft.Container(
                        padding=20,
                        alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Text("Không có học sinh giống với thông tin tìm kiếm", size=12, color=self.gray)
                    )
                )
            else:
                for student in found_students:
                    rows.append(
                        ft.Container(
                            bgcolor="#F8FAFC",
                            padding=10,
                            border_radius=8,
                            content=ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text(student.get("name", ""), size=13, weight=ft.FontWeight.BOLD,
                                                    color=self.dark),
                                            ft.Text(f"- Lớp {student.get('class', '')}", size=12,
                                                    weight=ft.FontWeight.BOLD, color=self.blue),
                                        ]
                                    ),
                                    ft.Text(f"Mã ID: {student.get('id', '')}", size=11, color=self.gray)
                                ]
                            )
                        )
                    )

            results_content = ft.Column(
                spacing=12,
                controls=[
                    results_top_bar,
                    ft.Container(
                        content=ft.Column(controls=rows, scroll=ft.ScrollMode.AUTO, spacing=8),
                        height=250,
                    )
                ]
            )
            self.root.content = self.card(results_content, 380)
            self.page.update()

        # ----------------------------------------------------
        # STATE 4: NORMAL STUDENT TABLE (WITH 2 BUTTONS AT BOTTOM)
        # ----------------------------------------------------
        else:
            rows = []
            header = ft.Container(
                bgcolor=self.blue,
                padding=10,
                border_radius=8,
                content=ft.Row(
                    controls=[
                        ft.Text("Mã ID", color="white", width=70, size=12, weight=ft.FontWeight.BOLD),
                        ft.Text("Họ tên", color="white", expand=True, size=12, weight=ft.FontWeight.BOLD),
                        ft.Text("Lớp", color="white", width=45, size=12, weight=ft.FontWeight.BOLD),
                        ft.Text("Điểm", color="white", width=35, size=12, weight=ft.FontWeight.BOLD)
                    ]
                )
            )
            rows.append(header)

            for student in self.students:
                if student.get("role") != "student":
                    continue

                student_class_str = str(student.get("class", "")).strip().lower()

                if class_filter:
                    if str(class_filter).strip().lower() != student_class_str:
                        continue

                score = student.get("score", 0)
                rows.append(
                    ft.Container(
                        bgcolor="white",
                        padding=10,
                        border_radius=8,
                        content=ft.Row(
                            controls=[
                                ft.Text(student.get("id", ""), width=70, size=12, color=self.dark),
                                ft.Text(student.get("name", ""), expand=True, size=12, max_lines=1, color=self.dark),
                                ft.Text(student.get("class", ""), width=45, size=12, color=self.dark),
                                ft.Text(str(score), width=35, size=12, color=self.dark)
                            ]
                        )
                    )
                )

            if len(rows) == 1:
                rows.append(
                    ft.Container(
                        padding=20,
                        alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Text("Chưa có học sinh nào trong lớp này", size=12, color=self.gray)
                    )
                )

            # Two side-by-side action buttons at the bottom
            action_buttons = ft.Row(
                spacing=10,
                controls=[
                    ft.Container(
                        expand=True,
                        on_click=lambda e: self.show_student_list(class_filter, show_delete_form=True),
                        padding=ft.Padding(0, 10, 0, 10),
                        border_radius=10,
                        bgcolor=self.red,
                        alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Text("Xoá tài khoản", size=12, color="white", weight=ft.FontWeight.BOLD)
                    ),
                    ft.Container(
                        expand=True,
                        on_click=lambda e: self.show_student_list(class_filter, show_search_form=True),
                        padding=ft.Padding(0, 10, 0, 10),
                        border_radius=10,
                        bgcolor=self.blue,
                        alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Text("Tìm học sinh", size=12, color="white", weight=ft.FontWeight.BOLD)
                    )
                ]
            )

            body = ft.Column(
                spacing=12,
                controls=[
                    top_bar,
                    ft.Container(
                        content=ft.Column(controls=rows, scroll=ft.ScrollMode.AUTO, spacing=8),
                        height=210,
                    ),
                    action_buttons
                ]
            )

            self.root.content = self.card(body, 380)
            self.page.update()

    # =========================
    # TÌM KIẾM HỌC SINH
    # =========================
    def show_search_student(self, query=None):
                    self.load_data()
                    self.check_data()

                    # ----------------------------------------------------
                    # STATE 1: SEARCH FORM
                    # ----------------------------------------------------
                    if not query:
                        top_bar = ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text("TÌM KIẾM HỌC SINH", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                            ]
                        )

                        name_input = ft.TextField(label="Nhập tên học sinh", text_size=12, height=48)
                        error_msg = ft.Text("", color=self.red, size=11, weight=ft.FontWeight.BOLD)

                        def process_search(e):
                            typed_name = name_input.value.strip()
                            if not typed_name:
                                error_msg.value = "Lỗi: Vui lòng nhập tên học sinh!"
                                self.page.update()
                                return
                            # Push to results view with the typed name
                            self.show_search_student(query=typed_name)

                        form_content = ft.Column(
                            spacing=15,
                            controls=[
                                top_bar,
                                name_input,
                                error_msg,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.TextButton(
                                            "Hủy bỏ",
                                            on_click=lambda e: self.show_admin_home()
                                        ),
                                        ft.ElevatedButton(
                                            "Tìm kiếm",
                                            bgcolor=self.blue,
                                            color="white",
                                            on_click=process_search
                                        )
                                    ]
                                )
                            ]
                        )
                        self.root.content = self.card(form_content, 380)
                        self.page.update()

                    # ----------------------------------------------------
                    # STATE 2: SEARCH RESULTS
                    # ----------------------------------------------------
                    else:
                        top_bar = ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(f"KẾT QUẢ: '{query}'", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                                ft.Container(
                                    on_click=lambda e: self.show_search_student(),
                                    padding=ft.Padding(10, 6, 10, 6),
                                    border_radius=8,
                                    bgcolor="#E2E8F0",
                                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                                )
                            ]
                        )

                        rows = []
                        search_str = query.strip().lower()

                        # Filter logic (partial matching so they don't have to type the exact full name)
                        found_students = []
                        for student in self.students:
                            if student.get("role") != "student":
                                continue
                            db_name = str(student.get("name", "")).strip().lower()
                            if search_str in db_name:
                                found_students.append(student)

                        # Error State: No students found
                        if not found_students:
                            rows.append(
                                ft.Container(
                                    padding=20,
                                    alignment=ft.alignment.Alignment(0, 0),
                                    content=ft.Text("Không có học sinh giống với thông tin tìm kiếm", size=12,
                                                    color=self.gray)
                                )
                            )
                        # Success State: Map results to specific UI layout
                        else:
                            for student in found_students:
                                rows.append(
                                    ft.Container(
                                        bgcolor="#F8FAFC",
                                        padding=12,
                                        border_radius=8,
                                        content=ft.Column(
                                            spacing=2,
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Text(student.get("name", ""), size=14,
                                                                weight=ft.FontWeight.BOLD, color=self.dark),
                                                        ft.Text(f"- {student.get('class', '')}", size=12,
                                                                weight=ft.FontWeight.BOLD, color=self.blue),
                                                    ]
                                                ),
                                                ft.Text(f"Mã ID: {student.get('id', '')}", size=11, color=self.gray)
                                            ]
                                        )
                                    )
                                )

                        results_content = ft.Column(
                            spacing=12,
                            controls=[
                                top_bar,
                                ft.Container(
                                    content=ft.Column(controls=rows, scroll=ft.ScrollMode.AUTO, spacing=8),
                                    height=280,
                                )
                            ]
                        )

                        self.root.content = self.card(results_content, 380)
                        self.page.update()

    # =========================
    # DANH SÁCH ĐĂNG KÝ
    # =========================
    def show_admin_registration_list(self):
        self.load_data()
        self.check_data()

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("DANH SÁCH ĐĂNG KÝ", size=15, weight=ft.FontWeight.BOLD, color=self.dark)
                    ]
                ),
                ft.Container(
                    on_click=lambda e: self.show_admin_home(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",
                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        rows = []
        header = ft.Container(
            bgcolor=self.blue,
            padding=10,
            border_radius=8,
            content=ft.Row(
                controls=[
                    ft.Text("Mã ID", color="white", width=60, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text("Họ tên", color="white", expand=True, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text("Lớp", color="white", width=45, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text("Mật khẩu", color="white", width=65, size=12, weight=ft.FontWeight.BOLD)
                ]
            )
        )
        rows.append(header)

        for student in self.students:
            if student.get("role") != "student":
                continue

            rows.append(
                ft.Container(
                    bgcolor="white",
                    padding=10,
                    border_radius=8,
                    content=ft.Row(
                        controls=[
                            ft.Text(student.get("id", ""), width=60, size=12, color=self.dark),
                            ft.Text(student.get("name", ""), expand=True, size=12, max_lines=1, color=self.dark),
                            ft.Text(student.get("class", ""), width=45, size=12, color=self.dark),
                            ft.Text(student.get("password", ""), width=65, size=12, color=self.dark)
                        ]
                    )
                )
            )

        if len(rows) == 1:
            rows.append(
                ft.Container(
                    padding=20,
                    alignment=ft.alignment.Alignment(0, 0),
                    content=ft.Text("Chưa có học sinh nào đăng ký", size=12, color=self.gray)
                )
            )

        body = ft.Column(
            spacing=12,
            controls=[
                top_bar,
                ft.Container(
                    content=ft.Column(controls=rows, scroll=ft.ScrollMode.AUTO, spacing=8),
                    height=280,
                )
            ]
        )

        self.root.content = self.card(body, 380)
        self.page.update()

    # =========================
    # TRANG HỌC SINH
    # =========================
    def show_student_home(self):
        if not self.current_user:
            self.show_role_select()
            return

        user_name = self.current_user.get("name", "Học sinh")
        user_class = self.current_user.get("class", "")
        user_id = self.current_user.get("id", "")
        user_score = self.current_user.get("score", 0)
        user_img = self.current_user.get("image", "")

        img_control = None
        if user_img and len(user_img) > 100:
            try:
                img_control = ft.Image(
                    src_base64=user_img,
                    width=60,
                    height=60,
                    fit="cover",
                    border_radius=30
                )
            except:
                img_control = None

        if not img_control:
            img_control = ft.Container(
                width=60,
                height=60,
                border_radius=30,
                bgcolor="#E2E8F0",
                alignment=ft.alignment.Alignment(0, 0),
                content=ft.Text(
                    user_name[0].upper() if user_name else "H",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=self.blue
                )
            )

        profile_card = ft.Container(
            width=340,
            padding=15,
            bgcolor="#F8FAFC",
            border_radius=15,
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        children=[
                            ft.Row(
                                spacing=12,
                                controls=[
                                    img_control,
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(user_name, size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                                            ft.Text(f"Mã ID: {user_id}", size=11, color=self.gray),
                                            ft.Text(f"Lớp: {user_class}", size=11, color=self.gray)
                                        ]
                                    )
                                ]
                            ),
                            ft.Container(
                                on_click=lambda e: self.show_role_select(),
                                padding=ft.Padding(8, 5, 8, 5),
                                border_radius=8,
                                bgcolor="#FEE2E2",
                                content=ft.Text("Đăng xuất", size=11, color=self.red, weight=ft.FontWeight.BOLD)
                            )
                        ]
                    )
                ]
            )
        )

        score_card = ft.Container(
            width=340,
            padding=15,
            bgcolor="#EFF6FF",
            border_radius=15,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("Điểm thi đua", size=12, color=self.gray),
                            ft.Text(str(user_score), size=24, weight=ft.FontWeight.BOLD, color=self.blue)
                        ]
                    ),
                    ft.Text("Tốt", size=14, weight=ft.FontWeight.BOLD, color=self.green)
                ]
            )
        )

        dashboard_content = ft.Column(
            controls=[
                self.title("TRANG CÁ NHÂN"),
                ft.Container(height=5),
                profile_card,
                ft.Container(height=10),
                score_card,
                ft.Container(height=10),
                ft.Container(
                    width=340,
                    padding=12,
                    bgcolor="#F8FAFC",
                    border_radius=12,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text("Tình trạng hệ thống", size=12, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Đang kết nối cơ sở dữ liệu", size=11, color=self.gray)
                                ]
                            ),
                            ft.Text("Hoạt động", size=10, color=self.green, weight=ft.FontWeight.BOLD)
                        ]
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(dashboard_content, 365)
        self.page.update()

    # =========================
    # LÀM MỚI DỮ LIỆU
    # =========================
    def refresh(self):
        self.load_data()
        self.check_data()
        if self.current_user:
            if self.current_user.get("role") == "admin":
                self.show_admin_home()
            else:
                self.show_student_home()
        else:
            self.show_role_select()