import flet as ft
import json
import os
import urllib.request
import ssl
import base64


try:
    _context = ssl.create_default_context()
except:
    _context = None



class AppController:


    def __init__(self, page: ft.Page):

        self.page = page


        self.root = ft.Container(
            expand=True
        )


        self.file = "students.json"


        self.db_url = base64.b64decode(
            "aHR0cHM6Ly9icm90aGVyczFnb2FsLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbS9zdHVkZW50cy5qc29u"
        ).decode()



        self.students = []

        self.current_user = None



        # key admin

        self.admin_key = "123"




        # =====================
        # ẢNH HỌC SINH
        # =====================

        self.image_path = ft.TextField(
            label="Đường dẫn ảnh"
        )




        # =====================
        # FORM ADMIN
        # =====================


        self.admin_key_login = ft.TextField(
            label="Nhập key Admin",
            password=True
        )




        # =====================
        # FORM HỌC SINH LOGIN
        # =====================


        self.student_login_name = ft.TextField(
            label="Tên học sinh"
        )


        self.student_login_password = ft.TextField(
            label="Mật khẩu",
            password=True
        )




        # =====================
        # FORM ĐĂNG KÝ
        # =====================


        self.student_name = ft.TextField(
            label="Họ và tên"
        )


        self.student_class = ft.TextField(
            label="Lớp"
        )


        self.student_password = ft.TextField(
            label="Mật khẩu",
            password=True
        )


        self.student_confirm = ft.TextField(
            label="Nhập lại mật khẩu",
            password=True
        )




        # =====================
        # THÊM HỌC SINH
        # =====================


        self.new_id = ft.TextField(
            label="Mã học sinh"
        )


        self.new_name = ft.TextField(
            label="Họ tên"
        )


        self.new_score = ft.TextField(
            label="Điểm"
        )




        # =====================
        # CẬP NHẬT ĐIỂM
        # =====================


        self.edit_student_id = ft.TextField(
            label="Mã học sinh"
        )


        self.edit_score = ft.TextField(
            label="Điểm mới"
        )



    # =====================
    # START APP
    # =====================


    def start(self):


        self.load_data()


        self.check_data()


        self.show_role_select()
            # =====================
    # THÔNG BÁO
    # =====================

    def show_message(self, text):

        try:

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(text)
            )

            self.page.snack_bar.open = True

            self.page.update()


        except:

            pass




    # =====================
    # LOAD DATA
    # =====================

    def load_data(self):


        self.students = []



        # lấy Firebase

        try:


            req = urllib.request.Request(
                self.db_url,
                method="GET"
            )



            with urllib.request.urlopen(
                req,
                timeout=5,
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




        except Exception as e:


            print(
                "Firebase lỗi:",
                e
            )






        # lấy file local

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




            except Exception as e:


                print(
                    "File lỗi:",
                    e
                )







        # dữ liệu mẫu

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
                # =====================
    # SAVE DATA
    # =====================

    def save_data(self):

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



        except Exception as e:


            print(
                "Save lỗi:",
                e
            )





    # =====================
    # ĐỌC ẢNH
    # =====================

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





    # =====================
    # LƯU ẢNH HỌC SINH
    # =====================

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
                    "Gửi ảnh thành công"
                )



                self.show_student_home()



                return
                    # =====================
    # KIỂM TRA ĐIỂM
    # =====================

    def check_score(self, score):

        try:

            score = float(score)

        except:

            return False



        return 0 <= score <= 10






    # =====================
    # KIỂM TRA ĐĂNG KÝ
    # =====================

    def validate_student_register(self):


        if self.student_name.value.strip() == "":


            return False, "Chưa nhập họ tên"




        if self.student_class.value.strip() == "":


            return False, "Chưa nhập lớp"




        if self.student_password.value == "":


            return False, "Chưa nhập mật khẩu"





        if self.student_password.value != self.student_confirm.value:


            return False, "Mật khẩu không khớp"







        for student in self.students:



            if (

                student.get("name")
                ==
                self.student_name.value.strip()

                and

                student.get("class")
                ==
                self.student_class.value.strip()

            ):


                return False, "Học sinh đã tồn tại"






        return True, ""







    # =====================
    # XÓA FORM
    # =====================

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






    # =====================
    # TẠO ID HỌC SINH
    # =====================

    def create_student_id(self):


        number = 1



        while True:



            sid = f"HS{number:02d}"



            check = False



            for student in self.students:



                if student.get("id") == sid:



                    check = True





            if check == False:



                return sid




            number += 1
                # =====================
    # CHỌN VAI TRÒ
    # =====================

    def show_role_select(self):


        self.root.content = ft.Column(

            controls=[



                ft.Text(
                    "BẠN LÀ AI?",
                    size=30
                ),




                ft.ElevatedButton(

                    "Admin",

                    width=200,

                    on_click=lambda e:
                    self.show_admin_login()

                ),




                ft.ElevatedButton(

                    "Học sinh",

                    width=200,

                    on_click=lambda e:
                    self.show_student_login()

                )



            ],



            alignment=
            ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER

        )



        self.page.update()







    # =====================
    # ADMIN LOGIN
    # =====================

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





        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "ĐĂNG NHẬP ADMIN",

                    size=30

                ),




                self.admin_key_login,





                ft.ElevatedButton(


                    "Đăng nhập",


                    on_click=login


                ),




                ft.TextButton(


                    "Quay lại",


                    on_click=lambda e:
                    self.show_role_select()


                )



            ],




            alignment=
            ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER

        )



        self.page.update()
            # =====================
    # HỌC SINH LOGIN
    # =====================

    def show_student_login(self):


        def login(e):


            name = self.student_login_name.value.strip()


            password = self.student_login_password.value





            for student in self.students:



                if (

                    student.get("name")
                    ==
                    name

                    and

                    student.get("password")
                    ==
                    password

                ):



                    self.current_user = student



                    self.show_student_home()



                    return





            self.show_message(

                "Sai tên hoặc mật khẩu"

            )







        self.root.content = ft.Column(



            controls=[




                ft.Text(

                    "ĐĂNG NHẬP HỌC SINH",

                    size=30

                ),




                self.student_login_name,



                self.student_login_password,





                ft.ElevatedButton(



                    "Đăng nhập",



                    on_click=login



                ),






                ft.ElevatedButton(



                    "Đăng ký",



                    on_click=lambda e:
                    self.show_register_student()



                ),






                ft.TextButton(



                    "Quay lại",



                    on_click=lambda e:
                    self.show_role_select()



                )



            ],




            alignment=
            ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER

        )




        self.page.update()







    # =====================
    # ĐĂNG KÝ HỌC SINH
    # =====================

    def show_register_student(self):


        def register(e):


            ok, msg = self.validate_student_register()



            if not ok:


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



            self.save_data()




            self.show_message(

                "Đăng ký thành công"

            )




            self.show_student_login()





        self.root.content = ft.Column(



            controls=[



                ft.Text(

                    "ĐĂNG KÝ HỌC SINH",

                    size=30

                ),




                self.student_name,



                self.student_class,



                self.student_password,



                self.student_confirm,





                ft.ElevatedButton(



                    "Hoàn tất",



                    on_click=register



                ),





                ft.TextButton(



                    "Quay lại",



                    on_click=lambda e:
                    self.show_student_login()



                )



            ],




            alignment=
            ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER

        )




        self.page.update()
            # =====================
    # TRANG ADMIN
    # =====================

    def show_admin_home(self):


        self.root.content = ft.Column(


            controls=[




                ft.Text(

                    "TRANG QUẢN TRỊ",

                    size=30

                ),





                ft.ElevatedButton(


                    "Danh sách học sinh",


                    width=250,


                    on_click=lambda e:
                    self.show_student_list()



                ),






                ft.ElevatedButton(



                    "Thêm học sinh",



                    width=250,



                    on_click=lambda e:
                    self.show_add_student()



                ),






                ft.ElevatedButton(



                    "Xóa học sinh",



                    width=250,



                    on_click=lambda e:
                    self.show_manage_student()



                ),






                ft.ElevatedButton(



                    "Cập nhật điểm",



                    width=250,



                    on_click=lambda e:
                    self.show_update_score()



                ),






                ft.ElevatedButton(



                    "Tìm kiếm",



                    width=250,



                    on_click=lambda e:
                    self.show_search_student()



                ),






                ft.ElevatedButton(



                    "Đăng xuất",



                    width=250,



                    on_click=lambda e:
                    self.logout()



                )



            ],




            alignment=
            ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER

        )




        self.page.update()







    # =====================
    # DANH SÁCH HỌC SINH
    # =====================

    def show_student_list(self):


        rows = []



        for student in self.students:



            if student.get("role") != "student":


                continue






            rows.append(



                ft.Text(



                    f"{student.get('id')} | "
                    f"{student.get('name')} | "
                    f"Lớp {student.get('class')} | "
                    f"Điểm {student.get('score')}"



                )



            )






        if len(rows) == 0:



            rows.append(

                ft.Text(
                    "Chưa có học sinh"
                )

            )







        self.root.content = ft.Column(



            controls=[



                ft.Text(

                    "DANH SÁCH HỌC SINH",

                    size=30

                ),





                ft.Column(

                    controls=rows

                ),






                ft.ElevatedButton(



                    "Quay lại",



                    on_click=lambda e:
                    self.show_admin_home()



                )



            ],



            scroll=
            ft.ScrollMode.AUTO

        )




        self.page.update()
            # =====================
    # THÊM HỌC SINH
    # =====================

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



            self.save_data()




            self.show_message(

                "Đã thêm học sinh"

            )




            self.show_student_list()






        self.root.content = ft.Column(



            controls=[




                ft.Text(

                    "THÊM HỌC SINH",

                    size=30

                ),




                self.new_id,



                self.new_name,



                self.new_score,






                ft.ElevatedButton(



                    "Thêm",



                    on_click=add



                ),






                ft.TextButton(



                    "Quay lại",



                    on_click=lambda e:
                    self.show_admin_home()



                )



            ],




            alignment=
            ft.MainAxisAlignment.CENTER

        )




        self.page.update()







    # =====================
    # QUẢN LÝ XÓA HỌC SINH
    # =====================

    def show_manage_student(self):


        rows = []



        for student in self.students:



            if student.get("role") != "student":


                continue





            rows.append(



                ft.Row(



                    controls=[




                        ft.Text(



                            f"{student.get('id')} - "
                            f"{student.get('name')}"



                        ),






                        ft.ElevatedButton(



                            "Xóa",



                            on_click=lambda e,
                            sid=student.get("id"):
                            self.delete_student(sid)



                        )



                    ]



                )



            )






        self.root.content = ft.Column(



            controls=[




                ft.Text(

                    "XÓA HỌC SINH",

                    size=30

                ),






                ft.Column(

                    controls=rows

                ),






                ft.TextButton(



                    "Quay lại",



                    on_click=lambda e:
                    self.show_admin_home()



                )



            ],



            scroll=
            ft.ScrollMode.AUTO

        )




        self.page.update()
            # =====================
    # XÓA HỌC SINH
    # =====================

    def delete_student(self, sid):


        for student in self.students:



            if student.get("id") == sid:



                self.students.remove(student)



                self.save_data()



                self.show_message(
                    "Đã xóa"
                )



                self.show_manage_student()



                return






    # =====================
    # HỌC SINH TRANG CÁ NHÂN
    # =====================

    def show_student_home(self):


        if self.current_user is None:


            self.show_role_select()


            return





        student = self.current_user




        score = float(
            student.get("score",0)
        )





        if score >= 8:


            rank = "Giỏi"



        elif score >= 6.5:


            rank = "Khá"



        elif score >= 5:


            rank = "Trung bình"



        else:


            rank = "Yếu"






        controls = [




            ft.Text(

                "THÔNG TIN HỌC SINH",

                size=30

            ),






            ft.Text(

                f"Mã: {student.get('id')}"

            ),






            ft.Text(

                f"Họ tên: {student.get('name')}"

            ),






            ft.Text(

                f"Lớp: {student.get('class')}"

            ),






            ft.Text(

                f"Điểm: {student.get('score')}"

            ),






            ft.Text(

                f"Xếp loại: {rank}"

            )



        ]







        # hiển thị ảnh nếu có

        if student.get("image","") != "":



            controls.append(



                ft.Image(

                    src_base64=student.get("image"),

                    width=150,

                    height=150

                )



            )



        else:



            controls.append(



                ft.Text(

                    "Chưa có ảnh"

                )



            )






        controls.extend([




            self.image_path,






            ft.ElevatedButton(



                "Gửi ảnh",



                on_click=lambda e:
                self.save_student_image()



            ),






            ft.ElevatedButton(



                "Đăng xuất",



                on_click=lambda e:
                self.logout()



            )



        ])






        self.root.content = ft.Column(



            controls=controls,



            alignment=
            ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            scroll=
            ft.ScrollMode.AUTO

        )





        self.page.update()
            # =====================
    # CẬP NHẬT ĐIỂM
    # =====================

    def show_update_score(self):


        def update(e):


            sid = self.edit_student_id.value.strip()



            if not self.check_score(
                self.edit_score.value
            ):


                self.show_message(
                    "Điểm sai"
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
                "Không tìm thấy"
            )






        self.root.content = ft.Column(



            controls=[




                ft.Text(

                    "CẬP NHẬT ĐIỂM",

                    size=30

                ),





                self.edit_student_id,



                self.edit_score,






                ft.ElevatedButton(



                    "Lưu",



                    on_click=update



                ),






                ft.TextButton(



                    "Quay lại",



                    on_click=lambda e:
                    self.show_admin_home()



                )



            ]



        )



        self.page.update()







    # =====================
    # TÌM KIẾM HỌC SINH
    # =====================

    def show_search_student(self):


        keyword = ft.TextField(
            label="Nhập tên hoặc mã"
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



                        ft.Text(



                            f"{student.get('id')} | "
                            f"{student.get('name')} | "
                            f"Điểm {student.get('score')}"



                        )



                    )







            if len(result.controls) == 0:



                result.controls.append(

                    ft.Text(
                        "Không tìm thấy"
                    )

                )




            self.page.update()






        self.root.content = ft.Column(



            controls=[




                ft.Text(

                    "TÌM KIẾM HỌC SINH",

                    size=30

                ),





                keyword,





                ft.ElevatedButton(



                    "Tìm",



                    on_click=search



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




        self.page.update()







    # =====================
    # ĐĂNG XUẤT
    # =====================

    def logout(self):


        self.current_user = None



        self.clear_all_form()



        self.show_role_select()






    # =====================
    # KIỂM TRA DỮ LIỆU
    # =====================

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







    # =====================
    # LÀM MỚI DỮ LIỆU
    # =====================

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






    # =====================
    # KHỞI ĐỘNG LẠI
    # =====================

    def restart(self):


        self.current_user = None



        self.load_data()



        self.check_data()



        self.show_role_select()