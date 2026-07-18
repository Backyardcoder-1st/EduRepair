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

        # -------------------------
        # LẤY TỪ FIREBASE
        # -------------------------

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

                data = json.loads(

                    response.read().decode()

                )

                if isinstance(data, dict):

                    self.students = list(

                        data.values()

                    )



                elif isinstance(data, list):

                    self.students = data

                print(

                    "Firebase load thành công"

                )





        except Exception as e:

            print(

                "Firebase đọc lỗi:",

                e

            )

        # -------------------------
        # NẾU FIREBASE LỖI
        # LẤY FILE LOCAL
        # -------------------------

        if len(self.students) == 0:

            try:

                if os.path.exists(

                        self.file

                ):
                    with open(

                            self.file,

                            "r",

                            encoding="utf-8"

                    ) as f:
                        self.students = json.load(f)

                    print(

                        "Load file local"

                    )





            except Exception as e:

                print(

                    "Local lỗi:",

                    e

                )

        # -------------------------
        # DATA MẪU
        # -------------------------

        if len(self.students) == 0:
            self.students = [

                {

                    "id": "HS01",

                    "name": "Nguyễn Văn A",

                    "class": "11A1",

                    "password": "123456",

                    "score": 8,

                    "role": "student",

                    "image": ""

                },

                {

                    "id": "HS02",

                    "name": "Trần Thị B",

                    "class": "11A1",

                    "password": "123456",

                    "score": 6,

                    "role": "student",

                    "image": ""

                }

            ]

            self.save_data()

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

        # luôn backup trước

        self.backup_local()

        # sau đó đồng bộ web

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

        if not isinstance(

                self.students,

                list

        ):
            self.students = []

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

    def create_student_id(self):

        number = 1

        while True:

            sid = f"HS{number:02d}"

            exists = False

            for student in self.students:

                if student.get("id") == sid:
                    exists = True

                    break

            if exists == False:
                return sid

            number += 1

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
        cls = self.student_class.value  # Dropped .strip() since it is now a Dropdown
        password = self.student_password.value

        if name == "":
            return False, "Chưa nhập họ tên"

        # --- ADD THIS BLOCK HERE ---
        if cls is None or cls == "":
            return False, "Chưa chọn lớp học"
        # ---------------------------

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

        return True, ""  # Cleaned return statement without the trailing comma bug

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
                # 1. Main Header Mascot Logo (Dinosaur Logo)
                ft.Container(
                    width=90,
                    height=90,
                    alignment=ft.alignment.Alignment(0, 0),  # Safe centering
                    content=ft.Image(
                        src="LOGO.png",  # Loads assets/logo.png
                        width=90,
                        height=90,
                    )
                ),
                ft.Text(
                    "EduRepair",  # Updated name capitalization
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.dark,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Hệ thống quản lí-đăng kí lao động",  # Slogan
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=self.dark,  # Updated color to self.dark
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Chọn quyền truy cập",
                    size=15,
                    color=self.dark,  # Updated color to self.dark
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=10),

                # 2. Admin Access Row (Width: 340, Height: 100)
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
                            # Left: Admin Image Icon
                            ft.Container(
                                width=50,
                                height=50,
                                content=ft.Image(
                                    src="ADMIN.png",  # Loads assets/admin_icon.png
                                    width=50,
                                    height=50,
                                )
                            ),
                            # Middle: Labels
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text("ADMIN", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Quản lý dữ liệu", size=11, color=self.gray),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            # Right: Button
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

                # 3. Student Access Row (Width: 340, Height: 100)
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
                            # Left: Student Image Icon
                            ft.Container(
                                width=50,
                                height=50,
                                content=ft.Image(
                                    src="STUDENT.png",  # Loads assets/student_icon.png
                                    width=50,
                                    height=50,
                                )
                            ),
                            # Middle: Labels
                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text("HỌC SINH", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Thực hiện lao động", size=11, color=self.gray),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            # Right: Button
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

        # Render the card with a mobile-optimized container width (380px)
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
                    on_click=lambda e:
                    self.show_role_select()
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(
            body,
            380  # Keeps it looking clean and aligned on mobile!
        )

        self.page.update()

    # =========================
    # ĐĂNG NHẬP HỌC SINH
    # =========================
    def show_student_login(self):
        self.login_error_text.value = ""  # Reset error message on page entry

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

            # Display small red text under the board
            self.login_error_text.value = "Sai tên người dùng hoặc mật khẩu"
            self.page.update()

        body = ft.Column(
            controls=[
                self.title(
                    "ĐĂNG NHẬP HỌC SINH"
                ),

                self.student_login_name,

                self.student_login_password,

                self.login_error_text,  # Error label placed under the input fields

                self.button(
                    "Đăng nhập",
                    login,
                    self.green  # Changed from self.green to self.blue
                ),

                self.button(
                    "Đăng ký",
                    lambda e:
                    self.show_register_student(),
                    self.orange
                ),

                ft.TextButton(
                    "Quay lại",
                    on_click=lambda e:
                    self.show_role_select()
                )

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(
            body
        )
        self.page.update()
        # =========================

    # ĐĂNG KÝ HỌC SINH
    # =========================

    def show_register_student(self):
        self.register_error_text.value = ""  # Reset error message on page entry

        def register(e):
            ok, msg = self.validate_student_register()

            if ok == False:
                # Set dynamic red error label instead of popup message
                self.register_error_text.value = msg
                self.page.update()
                return

            student = {
                "id": self.create_student_id(),
                "name": self.student_name.value.strip(),
                "class": self.student_class.value,
                "password": self.student_password.value,
                "score": 0,
                "role": "student",
                "image": ""
            }

            self.students.append(student)

            # lưu local + firebase
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

                self.register_error_text,  # Error label placed under the input fields

                self.button(
                    "Hoàn tất",
                    register,
                    self.green  # Changed from self.green to self.blue
                ),

                ft.TextButton(
                    "Quay lại",
                    on_click=lambda e:
                    self.show_student_login()
                )

            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(
            body
        )
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

                # đồng bộ Firebase

                self.save_data()

                self.show_message(

                    "Đã cập nhật ảnh"

                )

                self.show_student_home()

                return
                # =========================

        # =========================
        # TRANG ĐĂNG NHẬP ADMIN
        # =========================
        def show_admin_login(self):

            def login(e):
                key = self.admin_key_login.value.strip()

                if key == self.admin_key:
                    # Logs in under the custom admin account name!
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
                        on_click=lambda e:
                        self.show_role_select()
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            self.root.content = self.card(body, 380)
            self.page.update()
            # =========================

    # DANH SÁCH HỌC SINH
    # =========================

    # =========================
    # TRANG ADMIN DASHBOARD
    # =========================
    def show_admin_home(self):

        # 1. Profile Header Box
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
                            # Profile Avatar with ADMIN.png image
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
                            # Name and Role labels
                            ft.Column(
                                spacing=1,
                                controls=[
                                    ft.Text("Võ Thị Yến Nhi", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text("Quản trị viên", size=11, color=self.gray),
                                ]
                            )
                        ]
                    ),

                    # Log-out Mini Button
                    ft.Container(
                        # --- CHANGED THIS LINE TO TARGET THE ROLE SELECT VIEW ---
                        on_click=lambda e: self.show_role_select(),
                        # --------------------------------------------------------
                        padding=ft.Padding(8, 5, 8, 5),
                        border_radius=8,
                        bgcolor="#FEE2E2",
                        content=ft.Text("Đăng xuất", size=11, color=self.red, weight=ft.FontWeight.BOLD)
                    )
                ]
            )
        )

        # Helper card styling generator for the sliding board carousel
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
                        # Clean mini logo circle for visual interest
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
                        # Label text
                        ft.Text(
                            title,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=self.dark
                        )
                    ]
                )
            )

        # 2. Swipeable horizontal sliding board
        sliding_board = ft.Row(
            controls=[
                feature_card("Danh sách đăng kí", "📝", self.blue, "#EFF6FF", lambda e: self.show_student_list()),
                feature_card("Lỗi vi phạm", "⚠️", self.red, "#FEF2F2",
                             lambda e: self.show_message("Chức năng 'Lỗi vi phạm' đang phát triển!")),
                feature_card("Tiến trình lao động", "⏳", self.orange, "#FFF7ED",
                             lambda e: self.show_message("Chức năng 'Tiến trình' đang phát triển!")),
                feature_card("Kết quả lao động", "✅", self.green, "#F0FDF4",
                             lambda e: self.show_message("Chức năng 'Kết quả' đang phát triển!")),
            ],
            scroll=ft.ScrollMode.AUTO,  # Enables safe horizontal swiping/scrolling
            spacing=10
        )

        # Compile mobile view elements
        dashboard_content = ft.Column(
            controls=[
                self.title("BẢNG ĐIỀU KHIỂN"),
                ft.Container(height=5),

                # Render Profile Info Card
                profile_header,
                ft.Container(height=15),

                # Sliding Board Carousel Title
                ft.Row(
                    controls=[
                        ft.Text("Công cụ quản lý", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Cuộn ngang ➔", size=10, color=self.gray)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(height=5),

                # Render the sliding board
                sliding_board,
                ft.Container(height=15),

                # Minimalist System Status Info card
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

        # Output centered on clean, beautiful mobile widths (380px)
        self.root.content = self.card(dashboard_content, 380)
        self.page.update()

    def show_student_list(self):

        rows = []

        # 1. Compact Header Row scaled explicitly for mobile viewports
        header = ft.Container(
            bgcolor=self.blue,
            padding=10,
            border_radius=8,
            content=ft.Row(
                controls=[
                    ft.Text("Mã", color="white", width=50, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text("Họ tên", color="white", expand=True, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text("Lớp", color="white", width=50, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text("Điểm", color="white", width=40, size=12, weight=ft.FontWeight.BOLD)
                ]
            )
        )

        rows.append(header)

        # 2. Iterate and append student records safely using matching cell widths
        for student in self.students:
            if student.get("role") != "student":
                continue

            score = student.get("score", 0)

            rows.append(
                ft.Container(
                    bgcolor="white",
                    padding=10,
                    border_radius=8,
                    content=ft.Row(
                        controls=[
                            ft.Text(student.get("id", ""), width=50, size=12),
                            ft.Text(student.get("name", ""), expand=True, size=12, max_lines=1),
                            ft.Text(student.get("class", ""), width=50, size=12),
                            ft.Text(str(score), width=40, size=12)
                        ]
                    )
                )
            )

        # 3. Top Control Bar layout containing the Title and the top-right Back Button
        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text("DANH SÁCH ĐĂNG KÝ", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Quản lý lao động", size=11, color=self.gray)
                    ]
                ),
                # Clean, top-right absolute-style Mini Back Button
                ft.Container(
                    on_click=lambda e: self.show_admin_home() if self.current_user.get("role") == "admin" else self.show_student_home(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",  # Professional soft gray background
                    content=ft.Text("Quay lại", size=11, color=self.gray, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        # 4. Assemble components inside a dedicated layout flow
        body = ft.Column(
            spacing=15,
            controls=[
                top_bar,

                # Fixed height frame layout container to correctly activate vertical scroll mechanics
                ft.Container(
                    content=ft.Column(
                        controls=rows,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=8
                    ),
                    height=380,  # Limits frame height to force touchscreen vertical dragging
                )
            ]
        )

        # 5. Output rendering target matching standard 380px phone width
        self.root.content = self.card(body, 380)
        self.page.update()

    # =========================
    # THÊM HỌC SINH
    # =========================

    def show_add_student(self):

        def add(e):

            if self.new_name.value.strip() == "":
                self.show_message(

                    "Chưa nhập tên"

                )

                return

            if not self.check_score(

                    self.new_score.value

            ):
                self.show_message(

                    "Điểm không hợp lệ"

                )

                return

            student = {

                "id":

                    self.new_id.value.strip()

                    if self.new_id.value.strip()

                    else

                    self.create_student_id(),

                "name":

                    self.new_name.value.strip(),

                "class":

                    "Chưa xếp lớp",

                "password":

                    "123456",

                "score":

                    float(

                        self.new_score.value

                    ),

                "role":

                    "student",

                "image":

                    ""

            }

            self.students.append(student)

            # lưu local + firebase

            self.save_data()

            self.show_message(

                "Thêm học sinh thành công"

            )

            self.show_student_list()

        body = ft.Column(

            controls=[

                self.title(

                    "THÊM HỌC SINH"

                ),

                self.new_id,

                self.new_name,

                self.new_score,

                self.button(

                    "Thêm",

                    add,

                    self.green

                ),

                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:

                    self.show_admin_home()

                )

            ],

            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER

        )

        self.root.content = self.card(

            body

        )

        self.page.update()
        # =========================

    # QUẢN LÝ XÓA HỌC SINH
    # =========================

    def show_manage_student(self):

        items = []

        for student in self.students:

            if student.get("role") != "student":
                continue

            items.append(

                ft.Container(

                    bgcolor="white",

                    padding=10,

                    border_radius=10,

                    content=ft.Row(

                        controls=[

                            ft.Text(

                                student.get("id")

                                + " - "

                                + student.get("name"),

                                expand=True

                            ),

                            ft.ElevatedButton(

                                "Xóa",

                                bgcolor=self.red,

                                color="white",

                                on_click=lambda e,

                                                sid=student.get("id"):

                                self.delete_student(sid)

                            )

                        ]

                    )

                )

            )

        body = ft.Column(

            controls=[

                self.title(

                    "XÓA HỌC SINH"

                ),

                ft.Column(

                    controls=items,

                    scroll=

                    ft.ScrollMode.AUTO

                ),

                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:

                    self.show_admin_home()

                )

            ]

        )

        self.root.content = self.card(

            body,

            650

        )

        self.page.update()

    # =========================
    # XÓA HỌC SINH
    # =========================

    def delete_student(self, sid):

        for student in self.students:

            if student.get("id") == sid:
                self.students.remove(student)

                self.save_data()

                self.show_message(

                    "Đã xóa học sinh"

                )

                self.show_manage_student()

                return

    # =========================
    # CẬP NHẬT ĐIỂM
    # =========================

    def show_update_score(self):

        def update(e):

            sid = self.edit_student_id.value.strip()

            if not self.check_score(

                    self.edit_score.value

            ):
                self.show_message(

                    "Điểm không hợp lệ"

                )

                return

            for student in self.students:

                if student.get("id") == sid:
                    student["score"] = float(

                        self.edit_score.value

                    )

                    self.save_data()

                    self.show_message(

                        "Đã cập nhật điểm"

                    )

                    self.show_admin_home()

                    return

            self.show_message(

                "Không tìm thấy học sinh"

            )

        body = ft.Column(

            controls=[

                self.title(

                    "CẬP NHẬT ĐIỂM"

                ),

                self.edit_student_id,

                self.edit_score,

                self.button(

                    "Lưu",

                    update,

                    self.orange

                ),

                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:

                    self.show_admin_home()

                )

            ],

            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER

        )

        self.root.content = self.card(

            body

        )

        self.page.update()
        # =========================

    # TÌM KIẾM HỌC SINH
    # =========================

    def show_search_student(self):

        keyword = ft.TextField(

            label="Nhập tên hoặc mã học sinh",

            filled=True

        )

        result = ft.Column()

        def search(e):

            result.controls.clear()

            key = keyword.value.lower().strip()

            for student in self.students:

                name = student.get(

                    "name",

                    ""

                ).lower()

                sid = student.get(

                    "id",

                    ""

                ).lower()

                if key in name or key in sid:
                    result.controls.append(

                        ft.Container(

                            bgcolor="white",

                            padding=10,

                            border_radius=10,

                            content=ft.Text(

                                f"{student.get('id')} | "

                                f"{student.get('name')} | "

                                f"Điểm: {student.get('score')}"

                            )

                        )

                    )

            if len(result.controls) == 0:
                result.controls.append(

                    ft.Text(

                        "Không tìm thấy"

                    )

                )

            self.page.update()

        body = ft.Column(

            controls=[

                self.title(

                    "TÌM KIẾM HỌC SINH"

                ),

                keyword,

                self.button(

                    "Tìm kiếm",

                    search,

                    self.blue

                ),

                result,

                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:

                    self.show_admin_home()

                )

            ],

            scroll=

            ft.ScrollMode.AUTO

        )

        self.root.content = self.card(

            body,

            650

        )

        self.page.update()

    # =========================
    # TRANG CÁ NHÂN HỌC SINH
    # =========================

    def show_student_home(self):

        if self.current_user is None:
            self.show_role_select()
            return

        student = self.current_user

        # 1. Profile Header Box (Maintains student specific name, class, and ID)
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
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            # Profile Avatar image container
                            ft.Container(
                                width=46,
                                height=46,
                                border_radius=23,
                                content=ft.Image(
                                    src="STUDENT.png",
                                    fit="cover",
                                    width=46,
                                    height=46,
                                    border_radius=23,
                                )
                            ),
                            # Name, Role, and ID labels
                            ft.Column(
                                spacing=1,
                                controls=[
                                    ft.Text(
                                        student.get("name", "") + "-" + student.get("class", ""),
                                        size=15,
                                        weight=ft.FontWeight.BOLD,
                                        color=self.dark
                                    ),
                                    ft.Text("Học sinh", size=11, color=self.gray),
                                    ft.Text("ID: " + student.get("id", ""), size=11, color=self.gray),
                                ]
                            )
                        ]
                    ),
                    # Log-out Mini Button
                    ft.Container(
                        on_click=lambda e: self.show_student_login(),
                        padding=ft.Padding(8, 5, 8, 5),
                        border_radius=8,
                        bgcolor="#FEE2E2",
                        content=ft.Text("Đăng xuất", size=11, color=self.red, weight=ft.FontWeight.BOLD)
                    )
                ]
            )
        )

        # 2. Reusable Card Builder (Using coordinate centering system)
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
                        # Clean mini logo circle for visual interest
                        ft.Container(
                            width=32,
                            height=32,
                            border_radius=8,
                            bgcolor=color,
                            alignment=ft.alignment.Alignment(0, 0),  # Fixed: True mathematical alignment center
                            content=ft.Text(
                                icon_char,
                                size=15,
                                color="white",
                                weight=ft.FontWeight.BOLD
                            )
                        ),
                        # Label text
                        ft.Text(
                            title,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=self.dark
                        )
                    ]
                )
            )

        # 3. Swipeable horizontal sliding board mapped with student tool features
        sliding_board = ft.Row(
            controls=[
                feature_card("Phần việc đăng kí", "📝", self.blue, "#EFF6FF", lambda e: self.show_student_list()),
                feature_card("Phần việc hoàn thành", "✅", self.green, "#F0FDF4", lambda e: self.show_message("Chức năng 'Phần việc hoàn thành' đang phát triển!")),
                feature_card("Lỗi vi phạm", "⚠️", self.red, "#FEF2F2", lambda e: self.show_message("Chức năng 'Lỗi vi phạm' đang phát triển!")),
                feature_card("Tiến trình rèn luyện", "⏳", self.orange, "#FFF7ED", lambda e: self.show_message("Chức năng 'Tiến trình rèn luyện' đang phát triển!")),
            ],
            scroll=ft.ScrollMode.AUTO,  # Enables safe horizontal swiping/scrolling on mobile screens
            spacing=10
        )

        # 4. Compile mobile view elements into the master layout column
        dashboard_content = ft.Column(
            controls=[
                self.title("TRANG CÁ NHÂN"),
                ft.Container(height=5),

                # Render Profile Info Card
                profile_header,
                ft.Container(height=15),

                # Sliding Board Carousel Title - Set to "Tính năng"
                ft.Row(
                    controls=[
                        ft.Text("Tính năng", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Cuộn ngang ➔", size=10, color=self.gray)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(height=5),

                # Render the sliding board carousel
                sliding_board,
                ft.Container(height=15),

                # Minimalist System Status Info card
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

        # Output centered on clean, beautiful mobile widths (380px)
        self.root.content = self.card(dashboard_content, 380)
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

    # =========================
    # KHỞI ĐỘNG LẠI
    # =========================

    def restart(self):

        self.current_user = None

        self.load_data()

        self.check_data()

        self.show_role_select()