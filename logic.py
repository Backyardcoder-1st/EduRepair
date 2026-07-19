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


        # KEY ADMIN

        self.admin_key = "123"


        # =========================
        # CARD GIAO DIỆN
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
        # TIÊU ĐỀ
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


        self.login_error_text = ft.Text(
            "",
            color=self.red,
            size=14,
            weight=ft.FontWeight.BOLD
        )


        self.register_error_text = ft.Text(
            "",
            color=self.red,
            size=14,
            weight=ft.FontWeight.BOLD
        )



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
        # ẢNH HỌC SINH GỬI ADMIN
        # =========================

        self.send_image_path = ft.TextField(

            label="Đường dẫn ảnh gửi Admin",

            filled=True

        )



        # =========================
        # XEM ẢNH ADMIN
        # =========================

        self.admin_image_list = ft.Column()



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


                data = json.loads(
                    response.read().decode()
                )


                if isinstance(data, dict):

                    self.students = list(
                        data.values()
                    )


                elif isinstance(data, list):

                    self.students = data


                print("Firebase load thành công")


        except Exception as e:

            print(
                "Firebase đọc lỗi:",
                e
            )



        if len(self.students) == 0:


            try:


                if os.path.exists(self.file):


                    with open(
                            self.file,
                            "r",
                            encoding="utf-8"

                    ) as f:


                        self.students = json.load(f)



                    print("Load file local")


            except Exception as e:


                print(
                    "Local lỗi:",
                    e
                )




        if len(self.students) == 0:


            self.students = [


                {

                    "id": "HS01",

                    "name": "Nguyễn Văn A",

                    "class": "A1",

                    "password": "123456",

                    "score": 8,

                    "role": "student",

                    "image": "",

                    "send_image": "",

                    "image_status": ""

                },


                {

                    "id": "HS02",

                    "name": "Trần Thị B",

                    "class": "A1",

                    "password": "123456",

                    "score": 6,

                    "role": "student",

                    "image": "",

                    "send_image": "",

                    "image_status": ""

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


            print("Backup local OK")



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

            ):


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

                self.students = list(
                    self.students.values()
                )

            else:

                self.students = []



        # bỏ dữ liệu lỗi

        self.students = [

            student

            for student in self.students

            if isinstance(student, dict)

        ]



        for student in self.students:



            if "role" not in student:

                student["role"] = "student"



            if "score" not in student:

                student["score"] = 0



            if "image" not in student:

                student["image"] = ""



            # =========================
            # THÊM DỮ LIỆU ẢNH GỬI ADMIN
            # =========================

            if "send_image" not in student:

                student["send_image"] = ""



            if "image_status" not in student:

                student["image_status"] = ""
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


        self.send_image_path.value = ""



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

                    alignment=ft.alignment.Alignment(0,0),

                    content=ft.Image(

                        src="LOGO.png",

                        width=90,

                        height=90

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

                                    height=50

                                )

                            ),



                            ft.Column(

                                spacing=2,

                                expand=True,


                                controls=[

                                    ft.Text(

                                        "ADMIN",

                                        size=14,

                                        weight=ft.FontWeight.BOLD,

                                        color=self.dark

                                    ),


                                    ft.Text(

                                        "Quản lý dữ liệu",

                                        size=11,

                                        color=self.gray

                                    )

                                ]

                            ),




                            ft.ElevatedButton(

                                "Đăng nhập",

                                bgcolor=self.blue,

                                color="white",

                                on_click=lambda e:

                                self.show_admin_login()

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

                                    height=50

                                )

                            ),



                            ft.Column(

                                spacing=2,

                                expand=True,


                                controls=[


                                    ft.Text(

                                        "HỌC SINH",

                                        size=14,

                                        weight=ft.FontWeight.BOLD,

                                        color=self.dark

                                    ),


                                    ft.Text(

                                        "Thực hiện lao động",

                                        size=11,

                                        color=self.gray

                                    )


                                ]

                            ),




                            ft.ElevatedButton(

                                "Đăng nhập",

                                bgcolor=self.green,

                                color="white",

                                on_click=lambda e:

                                self.show_student_login()

                            )

                        ]

                    )

                )


            ],


            horizontal_alignment=ft.CrossAxisAlignment.CENTER

        )



        self.root.content = self.card(body,380)


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


                self.clear_all_form()

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



        self.root.content = self.card(body,380)


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





            self.login_error_text.value = (

                "Sai tên người dùng hoặc mật khẩu"

            )


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



        self.root.content = self.card(body,380)


        self.page.update()





    # =========================
    # ĐĂNG KÝ HỌC SINH
    # =========================

    def show_register_student(self):


        self.register_error_text.value = ""



        def register(e):


            ok,msg = self.validate_student_register()



            if not ok:


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


                "image": "",


                "violations": [],


                "labor_progress": 0,


                "labor_result": ""

            }





            self.students.append(student)



            self.save_data()



            self.show_message(

                "Đăng ký thành công"

            )



            self.clear_all_form()



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

                    on_click=lambda e:

                    self.show_student_login()

                )



            ],



            horizontal_alignment=ft.CrossAxisAlignment.CENTER

        )



        self.root.content = self.card(body,380)


        self.page.update()
            # =========================
    # ĐỌC ẢNH TỪ ĐƯỜNG DẪN
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
    # HỌC SINH GỬI ẢNH CHO ADMIN
    # =========================

    def send_student_image(self):

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
                    "Đã gửi ảnh cho Admin"
                )



                self.show_student_home()



                return





    # =========================
    # ADMIN XEM ẢNH HỌC SINH
    # =========================

    def show_student_images(self):


        items = []



        for student in self.students:


            if student.get("role") != "student":

                continue




            image_data = student.get("image","")



            controls = [



                ft.Text(

                    f"{student.get('id')} - {student.get('name')}",

                    size=13,

                    weight=ft.FontWeight.BOLD

                )



            ]



            if image_data != "":



                controls.append(


                    ft.Image(

                        src_base64=image_data,

                        width=120,

                        height=120,

                        fit="cover"

                    )



                )


            else:


                controls.append(


                    ft.Text(

                        "Chưa gửi ảnh",

                        color=self.gray,

                        size=12

                    )


                )




            items.append(


                ft.Container(

                    bgcolor="white",

                    padding=10,

                    border_radius=10,


                    content=ft.Column(

                        controls=controls,

                        horizontal_alignment=ft.CrossAxisAlignment.CENTER

                    )


                )


            )





        body = ft.Column(

            controls=[



                self.title(

                    "ẢNH HỌC SINH GỬI"

                ),




                ft.Column(

                    controls=items,

                    scroll=ft.ScrollMode.AUTO,

                    height=450

                ),




                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:

                    self.show_admin_home()

                )



            ],


            horizontal_alignment=ft.CrossAxisAlignment.CENTER

        )





        self.root.content = self.card(

            body,

            650

        )



        self.page.update()





    # =========================
    # TRANG CẬP NHẬT ẢNH CÁ NHÂN
    # HỌC SINH
    # =========================

    def show_update_student_image(self):


        body = ft.Column(

            controls=[



                self.title(

                    "GỬI ẢNH CHO ADMIN"

                ),




                ft.Text(

                    "Nhập đường dẫn ảnh trên máy",

                    size=12,

                    color=self.gray

                ),




                self.image_path,




                self.button(

                    "Gửi ảnh",

                    self.send_student_image,

                    self.green

                ),




                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:

                    self.show_student_home()

                )



            ],



            horizontal_alignment=ft.CrossAxisAlignment.CENTER

        )



        self.root.content = self.card(

            body,

            380

        )



        self.page.update()
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

                                    width=46,

                                    height=46,

                                    fit="cover"

                                )

                            ),



                            ft.Column(

                                spacing=1,

                                controls=[



                                    ft.Text(

                                        "Võ Thị Yến Nhi",

                                        size=15,

                                        weight=ft.FontWeight.BOLD,

                                        color=self.dark

                                    ),



                                    ft.Text(

                                        "Quản trị viên",

                                        size=11,

                                        color=self.gray

                                    )

                                ]

                            )

                        ]

                    ),




                    ft.Container(

                        on_click=lambda e:self.logout(),


                        padding=ft.Padding(8,5,8,5),


                        border_radius=8,


                        bgcolor="#FEE2E2",


                        content=ft.Text(

                            "Đăng xuất",

                            size=11,

                            color=self.red,

                            weight=ft.FontWeight.BOLD

                        )

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


                    controls=[



                        ft.Container(


                            width=32,

                            height=32,


                            border_radius=8,


                            bgcolor=color,


                            alignment=ft.alignment.Alignment(0,0),



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




                feature_card(

                    "Danh sách đăng kí",

                    "📝",

                    self.blue,

                    "#EFF6FF",

                    lambda e:self.show_student_list()

                ),




                feature_card(

                    "Lớp học",

                    "🏫",

                    "#7C3AED",

                    "#F3E8FF",

                    lambda e:self.show_admin_classes()

                ),





                feature_card(

                    "Ảnh học sinh",

                    "🖼",

                    "#0891B2",

                    "#ECFEFF",

                    lambda e:self.show_student_images()

                ),





                feature_card(

                    "Xóa học sinh",

                    "❌",

                    self.red,

                    "#FEF2F2",

                    lambda e:self.show_manage_student()

                ),





                feature_card(

                    "Cập nhật điểm",

                    "📊",

                    self.orange,

                    "#FFF7ED",

                    lambda e:self.show_update_score()

                ),




            ],



            scroll=ft.ScrollMode.AUTO,


            spacing=10

        )






        dashboard_content = ft.Column(


            controls=[




                self.title(

                    "BẢNG ĐIỀU KHIỂN"

                ),





                ft.Container(

                    height=5

                ),




                profile_header,





                ft.Container(

                    height=15

                ),





                ft.Row(


                    controls=[



                        ft.Text(

                            "Công cụ quản lý",

                            size=14,

                            weight=ft.FontWeight.BOLD,

                            color=self.dark

                        ),




                        ft.Text(

                            "Cuộn ngang ➔",

                            size=10,

                            color=self.gray

                        )



                    ],



                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN

                ),





                ft.Container(

                    height=5

                ),




                sliding_board,





                ft.Container(

                    height=15

                ),





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



                                    ft.Text(

                                        "Tình trạng hệ thống",

                                        size=12,

                                        weight=ft.FontWeight.BOLD,

                                        color=self.dark

                                    ),



                                    ft.Text(

                                        "Đang kết nối cơ sở dữ liệu",

                                        size=11,

                                        color=self.gray

                                    )

                                ]

                            ),




                            ft.Text(

                                "Hoạt động",

                                size=10,

                                color=self.green,

                                weight=ft.FontWeight.BOLD

                            )

                        ]

                    )

                )


            ],


            horizontal_alignment=ft.CrossAxisAlignment.CENTER

        )




        self.root.content = self.card(

            dashboard_content,

            380

        )



        self.page.update()
            # =========================
    # TRANG XEM LỚP HỌC ADMIN
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



                        ft.Text(

                            "DANH SÁCH LỚP",

                            size=15,

                            weight=ft.FontWeight.BOLD,

                            color=self.dark

                        ),



                        ft.Text(

                            "Chọn một lớp để xem học sinh",

                            size=11,

                            color=self.gray

                        )

                    ]

                ),





                ft.Container(


                    padding=ft.Padding(10,6,10,6),


                    border_radius=8,


                    bgcolor="#E2E8F0",


                    on_click=lambda e:self.show_admin_home(),



                    content=ft.Text(

                        "Quay lại",

                        size=11,

                        weight=ft.FontWeight.BOLD,

                        color=self.dark

                    )

                )

            ]

        )







        class_buttons=[]



        for c in [f"A{i}" for i in range(1,11)]:



            class_buttons.append(



                ft.Container(


                    width=160,


                    height=55,


                    bgcolor="#F3E8FF",


                    border_radius=12,


                    alignment=ft.alignment.Alignment(0,0),




                    content=ft.Text(

                        c,

                        size=14,

                        color="#7C3AED",

                        weight=ft.FontWeight.BOLD

                    ),




                    on_click=lambda e,name=c:self.show_student_list(

                        class_filter=name

                    )

                )

            )







        rows=[]



        for i in range(0,len(class_buttons),2):


            rows.append(


                ft.Row(

                    controls=class_buttons[i:i+2],

                    alignment=ft.MainAxisAlignment.CENTER,

                    spacing=12

                )

            )






        body=ft.Column(


            controls=[



                top_bar,



                ft.Container(height=10),



                ft.Column(

                    controls=rows,

                    spacing=12,

                    scroll=ft.ScrollMode.AUTO

                )



            ],



            horizontal_alignment=ft.CrossAxisAlignment.CENTER

        )




        self.root.content=self.card(

            body,

            380

        )


        self.page.update()










    # =========================
    # DANH SÁCH HỌC SINH
    # =========================

    def show_student_list(self,class_filter=None):


        self.load_data()

        self.check_data()



        rows=[]





        header=ft.Container(


            bgcolor=self.blue,


            padding=10,


            border_radius=8,



            content=ft.Row(


                controls=[



                    ft.Text(

                        "Mã",

                        color="white",

                        width=50,

                        size=12

                    ),



                    ft.Text(

                        "Họ tên",

                        color="white",

                        expand=True,

                        size=12

                    ),



                    ft.Text(

                        "Lớp",

                        color="white",

                        width=50,

                        size=12

                    ),



                    ft.Text(

                        "Ảnh",

                        color="white",

                        width=50,

                        size=12

                    )

                ]

            )

        )



        rows.append(header)








        for student in self.students:



            if student.get("role")!="student":

                continue





            cls=str(

                student.get("class","")

            ).strip().lower()





            if class_filter:


                if str(class_filter).lower() not in cls:

                    continue







            image_button = ft.Text(

                "Chưa có",

                size=11,

                color=self.gray

            )






            if student.get("image","")!="":


                image_button = ft.Container(



                    width=45,

                    height=30,


                    bgcolor="#DCFCE7",


                    border_radius=6,


                    alignment=ft.alignment.Alignment(0,0),



                    content=ft.Text(

                        "Xem",

                        size=11,

                        color=self.green,

                        weight=ft.FontWeight.BOLD

                    ),




                    on_click=lambda e,s=student:self.show_single_student_image(s)

                )







            rows.append(



                ft.Container(



                    bgcolor="white",


                    padding=10,


                    border_radius=8,



                    content=ft.Row(



                        controls=[



                            ft.Text(

                                student.get("id",""),

                                width=50,

                                size=12

                            ),




                            ft.Text(

                                student.get("name",""),

                                expand=True,

                                size=12

                            ),




                            ft.Text(

                                student.get("class",""),

                                width=50,

                                size=12

                            ),




                            ft.Container(

                                width=50,

                                content=image_button

                            )



                        ]

                    )

                )

            )







        if len(rows)==1:



            rows.append(


                ft.Container(



                    padding=20,



                    content=ft.Text(

                        "Chưa có học sinh nào trong lớp này",

                        size=13,

                        color=self.gray

                    )

                )

            )







        title_text = (

            f"LỚP {class_filter}"

            if class_filter

            else

            "DANH SÁCH HỌC SINH"

        )





        body=ft.Column(


            controls=[



                ft.Row(



                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,



                    controls=[



                        ft.Text(

                            title_text,

                            size=15,

                            weight=ft.FontWeight.BOLD

                        ),



                        ft.TextButton(

                            "Quay lại",

                            on_click=lambda e:self.show_admin_classes()

                        )

                    ]

                ),





                ft.Column(


                    controls=rows,


                    height=400,


                    scroll=ft.ScrollMode.AUTO,


                    spacing=8

                )

            ]

        )




        self.root.content=self.card(

            body,

            500

        )



        self.page.update()
        # =========================
# XEM ẢNH MỘT HỌC SINH (ADMIN)
# =========================

def show_single_student_image(self, student):

    image = student.get("image", "")


    if image == "":

        self.show_message(
            "Học sinh này chưa gửi ảnh"
        )

        return



    body = ft.Column(

        controls=[


            ft.Text(

                "ẢNH HỌC SINH",

                size=20,

                weight=ft.FontWeight.BOLD,

                color=self.dark

            ),



            ft.Text(

                student.get("name",""),

                size=14,

                color=self.gray

            ),




            ft.Container(

                width=260,

                height=260,


                border_radius=15,


                content=ft.Image(

                    src_base64=image,

                    fit="cover"

                )

            ),





            ft.TextButton(

                "Quay lại",

                on_click=lambda e:self.show_student_list()

            )


        ],


        horizontal_alignment=ft.CrossAxisAlignment.CENTER

    )



    self.root.content=self.card(

        body,

        380

    )


    self.page.update()







# =========================
# TRANG XEM TẤT CẢ ẢNH HỌC SINH
# =========================


def show_student_images(self):


    self.load_data()

    self.check_data()



    items=[]



    for student in self.students:



        if student.get("role")!="student":

            continue




        if student.get("image","")=="":

            continue





        items.append(



            ft.Container(



                bgcolor="white",


                padding=10,


                border_radius=10,



                content=ft.Row(



                    controls=[




                        ft.Container(


                            width=55,


                            height=55,


                            border_radius=10,


                            content=ft.Image(

                                src_base64=student.get("image"),

                                fit="cover"

                            )

                        ),






                        ft.Column(



                            expand=True,



                            controls=[



                                ft.Text(

                                    student.get("name",""),

                                    size=13,

                                    weight=ft.FontWeight.BOLD

                                ),



                                ft.Text(

                                    "Đã gửi ảnh",

                                    size=11,

                                    color=self.green

                                )

                            ]

                        ),






                        ft.ElevatedButton(



                            "Xem",



                            on_click=lambda e,s=student:self.show_single_student_image(s)

                        )

                    ]

                )

            )

        )






    if len(items)==0:


        items.append(


            ft.Text(

                "Chưa có học sinh gửi ảnh",

                color=self.gray

            )

        )






    body=ft.Column(


        controls=[



            self.title(

                "ẢNH HỌC SINH GỬI"

            ),





            ft.Column(

                controls=items,


                scroll=ft.ScrollMode.AUTO,


                height=450

            ),





            ft.TextButton(

                "Quay lại",

                on_click=lambda e:self.show_admin_home()

            )


        ]

    )





    self.root.content=self.card(

        body,

        500

    )



    self.page.update()







# =========================
# HỌC SINH GỬI ẢNH ADMIN
# =========================


def show_send_image(self):


    path = ft.TextField(

        label="Đường dẫn ảnh",

        filled=True

    )



    message = ft.Text(

        "",

        color=self.red

    )





    def send(e):


        if path.value.strip()=="":


            message.value="Chưa nhập đường dẫn ảnh"

            self.page.update()

            return




        image=self.read_image(

            path.value.strip()

        )



        if image=="":


            message.value="Không đọc được ảnh"

            self.page.update()

            return





        for student in self.students:



            if student.get("id")==self.current_user.get("id"):



                student["image"]=image



                self.current_user=student



                break






        self.save_data()



        self.show_message(

            "Đã gửi ảnh cho Admin"

        )



        self.show_student_home()





    body=ft.Column(



        controls=[




            self.title(

                "GỬI ẢNH CHO ADMIN"

            ),




            ft.Text(

                "Chọn ảnh lao động / minh chứng",

                size=12,

                color=self.gray

            ),





            path,




            message,





            self.button(

                "Gửi ảnh",

                send,

                self.green

            ),





            ft.TextButton(

                "Quay lại",

                on_click=lambda e:self.show_student_home()

            )

        ],




        horizontal_alignment=ft.CrossAxisAlignment.CENTER

    )





    self.root.content=self.card(

        body,

        380

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


                                src="STUDENT.png",

                                width=46,

                                height=46,

                                fit="cover"

                            )

                        ),






                        ft.Column(



                            spacing=2,



                            controls=[




                                ft.Text(

                                    student.get("name",""),

                                    size=15,

                                    weight=ft.FontWeight.BOLD,

                                    color=self.dark

                                ),




                                ft.Text(

                                    "Học sinh",

                                    size=11,

                                    color=self.gray

                                ),




                                ft.Text(

                                    "ID: "+student.get("id",""),

                                    size=11,

                                    color=self.gray

                                )

                            ]

                        )

                    ]

                ),





                ft.Container(



                    bgcolor="#FEE2E2",


                    border_radius=8,


                    padding=ft.Padding(8,5,8,5),



                    on_click=lambda e:self.logout(),



                    content=ft.Text(

                        "Đăng xuất",

                        size=11,

                        color=self.red,

                        weight=ft.FontWeight.BOLD

                    )

                )

            ]

        )

    )







    def feature_card(title, text, color, bg, action):


        return ft.Container(



            width=135,


            height=120,


            bgcolor=bg,


            border_radius=15,


            padding=12,


            on_click=action,



            content=ft.Column(



                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,



                controls=[



                    ft.Container(


                        width=32,


                        height=32,


                        bgcolor=color,


                        border_radius=8,


                        alignment=ft.alignment.Alignment(0,0),



                        content=ft.Text(

                            text,

                            color="white",

                            size=15

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









    tools = ft.Row(


        controls=[




            feature_card(

                "Danh sách đăng ký",

                "DS",

                self.blue,

                "#EFF6FF",

                lambda e:self.show_student_list()

            ),




            feature_card(

                "Lớp học",

                "L",

                "#7C3AED",

                "#F3E8FF",

                lambda e:self.show_student_list(

                    class_filter=student.get("class","")

                )

            ),





            feature_card(

                "Gửi ảnh Admin",

                "Ả",

                self.green,

                "#F0FDF4",

                lambda e:self.show_send_image()

            ),






            feature_card(

                "Lỗi vi phạm",

                "!",

                self.red,

                "#FEF2F2",

                lambda e:self.show_message(

                    "Chức năng đang phát triển"

                )

            ),





            feature_card(

                "Tiến trình",

                "T",

                self.orange,

                "#FFF7ED",

                lambda e:self.show_message(

                    "Chức năng đang phát triển"

                )

            )

        ],



        spacing=10,


        scroll=ft.ScrollMode.AUTO

    )







    body=ft.Column(



        controls=[



            self.title(

                "BẢNG ĐIỀU KHIỂN"

            ),





            profile_header,




            ft.Container(height=15),





            ft.Text(

                "Công cụ học sinh",

                size=14,

                weight=ft.FontWeight.BOLD,

                color=self.dark

            ),





            tools,





            ft.Container(



                width=340,


                padding=12,


                bgcolor="#F8FAFC",


                border_radius=12,



                content=ft.Row(



                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,



                    controls=[



                        ft.Text(

                            "Trạng thái",

                            size=12,

                            weight=ft.FontWeight.BOLD

                        ),




                        ft.Text(

                            "Hoạt động",

                            size=11,

                            color=self.green

                        )

                    ]

                )

            )



        ],



        horizontal_alignment=ft.CrossAxisAlignment.CENTER

    )






    self.root.content=self.card(

        body,

        380

    )



    self.page.update()







# =========================
# ĐĂNG XUẤT
# =========================

def logout(self):


    self.current_user=None


    self.clear_all_form()


    self.show_role_select()
    # =========================
# LÀM MỚI DỮ LIỆU
# =========================

def refresh(self):


    try:


        self.load_data()


        self.check_data()



        if self.current_user:



            if self.current_user.get("role") == "admin":



                self.show_admin_home()



            else:



                self.show_student_home()



        else:



            self.show_role_select()



    except Exception as e:



        print(

            "Refresh lỗi:",

            e

        )



        self.show_message(

            "Không thể làm mới dữ liệu"

        )









# =========================
# KHỞI ĐỘNG APP
# =========================

def main(self):


    try:


        self.start()



    except Exception as e:


        print(

            "Lỗi khởi động app:",

            e

        )


        self.show_message(

            "Lỗi khởi động chương trình"

        )









# =========================
# HÀM KIỂM TRA USER HIỆN TẠI
# =========================

def get_current_student(self):


    if self.current_user is None:


        return None



    if self.current_user.get("role") != "student":


        return None



    return self.current_user







# =========================
# CẬP NHẬT ẢNH HIỂN THỊ
# =========================

def update_student_image(self):


    student=self.get_current_student()



    if student is None:


        return





    if student.get("image","")=="":


        return





    return student.get("image")









# =========================
# KIỂM TRA KẾT NỐI DATABASE
# =========================

def test_database(self):


    try:


        request=urllib.request.Request(


            self.db_url,


            method="GET"

        )



        with urllib.request.urlopen(


                request,


                timeout=5,


                context=_context


        ):



            return True




    except Exception as e:



        print(

            "Database lỗi:",

            e

        )


        return False