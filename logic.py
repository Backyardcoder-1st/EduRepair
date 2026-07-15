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

                    offset=ft.Offset(0,5)

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



        self.student_class = ft.TextField(

            label="Lớp",

            filled=True

        )



        self.student_password = ft.TextField(

            label="Mật khẩu",

            password=True,

            filled=True

        )



        self.student_confirm = ft.TextField(

            label="Nhập lại mật khẩu",

            password=True,

            filled=True

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

                    "id":"HS01",

                    "name":"Nguyễn Văn A",

                    "class":"11A1",

                    "password":"123456",

                    "score":8,

                    "role":"student",

                    "image":""

                },



                {

                    "id":"HS02",

                    "name":"Trần Thị B",

                    "class":"11A1",

                    "password":"123456",

                    "score":6,

                    "role":"student",

                    "image":""

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


        cls = self.student_class.value.strip()



        password = self.student_password.value





        if name == "":


            return False, "Chưa nhập họ tên"





        if cls == "":


            return False, "Chưa nhập lớp"





        if password == "":


            return False, "Chưa nhập mật khẩu"






        if password != self.student_confirm.value:


            return False, "Mật khẩu không khớp"








        for student in self.students:



            if (

                student.get("name") == name

                and

                student.get("class") == cls

            ):


                return False, "Học sinh đã tồn tại"







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


                ft.Text(

                    "HỆ THỐNG QUẢN LÝ HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD,

                    color=self.dark

                ),



                ft.Text(

                    "Chọn quyền truy cập",

                    size=18,

                    color=self.gray

                ),




                ft.Container(

                    height=20

                ),




                ft.Row(

                    controls=[




                        ft.Container(

                            width=200,

                            height=170,

                            bgcolor=self.blue,

                            border_radius=15,

                            padding=20,

                            content=ft.Column(

                                controls=[



                                    ft.Text(

                                        "ADMIN",

                                        size=22,

                                        color="white",

                                        weight=ft.FontWeight.BOLD

                                    ),




                                    ft.Text(

                                        "Quản lý dữ liệu",

                                        color="white"

                                    ),




                                    ft.ElevatedButton(

                                        "Đăng nhập",

                                        bgcolor="white",

                                        color=self.blue,

                                        on_click=lambda e:

                                        self.show_admin_login()

                                    )



                                ],

                                alignment=

                                ft.MainAxisAlignment.CENTER

                            )

                        ),






                        ft.Container(

                            width=200,

                            height=170,

                            bgcolor=self.green,

                            border_radius=15,

                            padding=20,

                            content=ft.Column(

                                controls=[



                                    ft.Text(

                                        "HỌC SINH",

                                        size=22,

                                        color="white",

                                        weight=ft.FontWeight.BOLD

                                    ),




                                    ft.Text(

                                        "Xem hồ sơ",

                                        color="white"

                                    ),




                                    ft.ElevatedButton(

                                        "Đăng nhập",

                                        bgcolor="white",

                                        color=self.green,

                                        on_click=lambda e:

                                        self.show_student_login()

                                    )



                                ],

                                alignment=

                                ft.MainAxisAlignment.CENTER

                            )

                        )



                    ],

                    alignment=

                    ft.MainAxisAlignment.CENTER

                )



            ],

            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER

        )





        self.root.content = self.card(

            body,

            600

        )


        self.page.update()










    # =========================
    # ĐĂNG NHẬP ADMIN
    # =========================


    def show_admin_login(self):


        def login(e):


            if self.admin_key_login.value == self.admin_key:



                self.current_user = {


                    "role":"admin"


                }



                self.show_admin_home()



            else:


                self.show_message(

                    "Sai key Admin"

                )







        body = ft.Column(

            controls=[



                self.title(

                    "ĐĂNG NHẬP ADMIN"

                ),




                self.admin_key_login,






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

            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER

        )







        self.root.content = self.card(

            body

        )


        self.page.update()











    # =========================
    # ĐĂNG NHẬP HỌC SINH
    # =========================


    def show_student_login(self):


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






            self.show_message(

                "Sai tên hoặc mật khẩu"

            )








        body = ft.Column(

            controls=[



                self.title(

                    "ĐĂNG NHẬP HỌC SINH"

                ),




                self.student_login_name,



                self.student_login_password,






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

            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER

        )






        self.root.content = self.card(

            body

        )


        self.page.update()
            # =========================
    # ĐĂNG KÝ HỌC SINH
    # =========================


    def show_register_student(self):


        def register(e):


            ok, msg = self.validate_student_register()



            if ok == False:


                self.show_message(msg)


                return






            student = {


                "id":

                self.create_student_id(),



                "name":

                self.student_name.value.strip(),



                "class":

                self.student_class.value.strip(),



                "password":

                self.student_password.value,



                "score":

                0,



                "role":

                "student",



                "image":

                ""

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



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER

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
    # TRANG ADMIN DASHBOARD
    # =========================


    def show_admin_home(self):


        total = 0

        total_score = 0

        excellent = 0

        good = 0

        average = 0

        weak = 0





        for student in self.students:



            if student.get("role") == "student":



                total += 1



                score = float(

                    student.get("score",0)

                )



                total_score += score





                if score >= 8:



                    excellent += 1



                elif score >= 6.5:



                    good += 1



                elif score >= 5:



                    average += 1



                else:


                    weak += 1





        avg_score = 0



        if total > 0:



            avg_score = round(

                total_score / total,

                2

            )







        def box(text, number, color):


            return ft.Container(



                width=150,


                height=110,


                bgcolor=color,


                border_radius=15,


                padding=15,



                content=ft.Column(


                    controls=[



                        ft.Text(


                            text,


                            color="white",


                            size=16


                        ),




                        ft.Text(


                            str(number),


                            color="white",


                            size=28,


                            weight=

                            ft.FontWeight.BOLD

                        )



                    ],



                    alignment=

                    ft.MainAxisAlignment.CENTER

                )

            )








        dashboard = ft.Column(

            controls=[



                self.title(

                    "BẢNG ĐIỀU KHIỂN ADMIN"

                ),





                ft.Row(

                    controls=[



                        box(

                            "Tổng HS",

                            total,

                            self.blue

                        ),




                        box(

                            "Điểm TB",

                            avg_score,

                            self.green

                        ),




                        box(

                            "Giỏi",

                            excellent,

                            self.orange

                        )



                    ],



                    alignment=

                    ft.MainAxisAlignment.CENTER

                ),





                ft.Row(

                    controls=[



                        box(

                            "Khá",

                            good,

                            "#7C3AED"

                        ),




                        box(

                            "Trung bình",

                            average,

                            "#0891B2"

                        ),




                        box(

                            "Yếu",

                            weak,

                            self.red

                        )



                    ],



                    alignment=

                    ft.MainAxisAlignment.CENTER

                ),





                ft.Container(

                    height=20

                ),







                self.button(

                    "Danh sách học sinh",

                    lambda e:

                    self.show_student_list(),

                    self.blue

                ),





                self.button(

                    "Thêm học sinh",

                    lambda e:

                    self.show_add_student(),

                    self.green

                ),





                self.button(

                    "Xóa học sinh",

                    lambda e:

                    self.show_manage_student(),

                    self.red

                ),





                self.button(

                    "Cập nhật điểm",

                    lambda e:

                    self.show_update_score(),

                    self.orange

                ),





                self.button(

                    "Tìm kiếm",

                    lambda e:

                    self.show_search_student(),

                    "#7C3AED"

                ),






                ft.TextButton(

                    "Đăng xuất",

                    on_click=lambda e:

                    self.logout()

                )



            ],



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER,


            scroll=

            ft.ScrollMode.AUTO

        )







        self.root.content = self.card(

            dashboard,

            700

        )



        self.page.update()
            # =========================
    # DANH SÁCH HỌC SINH
    # =========================


    def show_student_list(self):


        rows = []



        header = ft.Container(


            bgcolor=self.blue,


            padding=10,


            border_radius=8,


            content=ft.Row(

                controls=[


                    ft.Text(

                        "Mã",

                        color="white",

                        width=80

                    ),


                    ft.Text(

                        "Họ tên",

                        color="white",

                        expand=True

                    ),


                    ft.Text(

                        "Lớp",

                        color="white",

                        width=100

                    ),


                    ft.Text(

                        "Điểm",

                        color="white",

                        width=80

                    )

                ]

            )

        )



        rows.append(header)






        for student in self.students:



            if student.get("role") != "student":


                continue





            score = student.get(

                "score",

                0

            )



            rows.append(



                ft.Container(



                    bgcolor="white",



                    padding=10,



                    border_radius=8,



                    content=ft.Row(

                        controls=[



                            ft.Text(

                                student.get("id"),

                                width=80

                            ),




                            ft.Text(

                                student.get("name"),

                                expand=True

                            ),




                            ft.Text(

                                student.get("class"),

                                width=100

                            ),




                            ft.Text(

                                str(score),

                                width=80

                            )



                        ]

                    )

                )

            )







        body = ft.Column(

            controls=[



                self.title(

                    "DANH SÁCH HỌC SINH"

                ),





                ft.Column(

                    controls=rows,

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

            750

        )


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






        score = float(

            student.get(

                "score",

                0

            )

        )






        if score >= 8:


            rank = "Giỏi"



        elif score >= 6.5:


            rank = "Khá"



        elif score >= 5:


            rank = "Trung bình"



        else:


            rank = "Yếu"








        info = ft.Column(

            controls=[



                self.title(

                    "HỒ SƠ HỌC SINH"

                ),





                ft.Text(

                    "Mã: "

                    + student.get("id",""),

                    size=18

                ),




                ft.Text(

                    "Họ tên: "

                    + student.get("name",""),

                    size=18

                ),




                ft.Text(

                    "Lớp: "

                    + student.get("class",""),

                    size=18

                ),




                ft.Text(

                    "Điểm: "

                    + str(student.get("score",0)),

                    size=18

                ),




                ft.Text(

                    "Xếp loại: "

                    + rank,

                    size=18,

                    weight=ft.FontWeight.BOLD

                )



            ],



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER

        )








        if student.get("image","") != "":



            info.controls.append(



                ft.Image(


                    src_base64=

                    student.get("image"),


                    width=150,


                    height=150


                )



            )



        else:


            info.controls.append(



                ft.Text(

                    "Chưa có ảnh"

                )



            )






        info.controls.extend([



            self.image_path,





            self.button(

                "Cập nhật ảnh",

                lambda e:

                self.save_student_image(),

                self.green

            ),





            ft.TextButton(

                "Đăng xuất",

                on_click=lambda e:

                self.logout()

            )



        ])







        self.root.content = self.card(

            info

        )



        self.page.update()
            # =========================
    # ĐĂNG XUẤT
    # =========================


    def logout(self):


        self.current_user = None



        self.clear_all_form()



        self.show_role_select()







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