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


        # FIX TRẮNG MÀN HÌNH FLET WEB
        self.root = ft.Container(
            expand=True
        )


        self.file = "students.json"



        self.db_url = base64.b64decode(
            "aHR0cHM6Ly9icm90aGVyczFnb2FsLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbS9zdHVkZW50cy5qc29u"
        ).decode()



        self.students = []

        self.current_user = None



        # KEY ADMIN

        self.admin_key = "123"



        # =========================
        # ĐĂNG NHẬP ADMIN
        # =========================

        self.admin_key_login = ft.TextField(
            label="Nhập key Admin",
            password=True,
            can_reveal_password=True
        )



        # =========================
        # ĐĂNG NHẬP HỌC SINH
        # =========================

        self.student_login_name = ft.TextField(
            label="Tên học sinh"
        )


        self.student_login_password = ft.TextField(
            label="Mật khẩu",
            password=True,
            can_reveal_password=True
        )



        # =========================
        # ĐĂNG KÝ HỌC SINH
        # =========================

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



        # =========================
        # THÊM HỌC SINH
        # =========================

        self.new_id = ft.TextField(
            label="Mã học sinh (để trống tự tạo)"
        )


        self.new_name = ft.TextField(
            label="Họ tên"
        )


        self.new_score = ft.TextField(
            label="Điểm"
        )



        # =========================
        # SỬA ĐIỂM
        # =========================

        self.edit_student_id = ft.TextField(
            label="Mã học sinh"
        )


        self.edit_score = ft.TextField(
            label="Điểm mới"
        )
            # =========================
    # KHỞI ĐỘNG ỨNG DỤNG
    # =========================

    def start(self):

        print("APP START")


        self.load_data()

        print("LOAD XONG")


        self.check_data()

        print("CHECK XONG")


        self.show_role_select()

        print("HIEN LOGIN XONG")





    # =========================
    # HIỂN THỊ THÔNG BÁO
    # =========================

    def show_message(self, message):

        try:

            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message)
            )


            self.page.snack_bar.open = True


            self.page.update()


        except Exception as e:

            print("Snack error:", e)





    # =========================
    # LOAD DỮ LIỆU
    # =========================

    def load_data(self):

        self.students = []



        # LOAD FIREBASE

        try:


            req = urllib.request.Request(

                self.db_url,

                headers={
                    "Content-Type": "application/json"
                },

                method="GET"

            )



            with urllib.request.urlopen(
                req,
                timeout=5,
                context=_context
            ) as response:


                data = json.loads(
                    response.read().decode("utf-8")
                )



                if isinstance(data, dict):

                    self.students = list(
                        data.values()
                    )


                elif isinstance(data, list):

                    self.students = [
                        x for x in data if x
                    ]



        except Exception as e:

            print("Firebase load:", e)




        # NẾU FIREBASE LỖI -> FILE LOCAL


        if len(self.students) == 0:


            try:


                if os.path.exists(self.file):


                    with open(
                        self.file,
                        "r",
                        encoding="utf-8"
                    ) as f:


                        data = json.load(f)



                        if isinstance(data, list):

                            self.students = data


                        elif isinstance(data, dict):

                            self.students = list(
                                data.values()
                            )



            except Exception as e:

                print("Local load:", e)
                        # =========================
        # DỮ LIỆU MẪU NẾU TRỐNG
        # =========================

        if len(self.students) == 0:


            self.students = [


                {
                    "id": "HS01",
                    "name": "Nguyễn Văn A",
                    "class": "11A1",
                    "password": "123456",
                    "score": 8,
                    "role": "student",
                    "image_proof": ""
                },


                {
                    "id": "HS02",
                    "name": "Trần Thị B",
                    "class": "11A1",
                    "password": "123456",
                    "score": 6,
                    "role": "student",
                    "image_proof": ""
                }


            ]





    # =========================
    # LƯU DỮ LIỆU
    # =========================

    def save_data(self):


        data = {}



        for student in self.students:


            if "id" in student:

                data[student["id"]] = student





        # LƯU FIREBASE

        try:


            req = urllib.request.Request(

                self.db_url,

                data=json.dumps(
                    data,
                    ensure_ascii=False
                ).encode("utf-8"),


                headers={
                    "Content-Type": "application/json"
                },


                method="PUT"

            )



            urllib.request.urlopen(

                req,

                timeout=5,

                context=_context

            )



        except Exception as e:

            print("Firebase save:", e)







        # SAO LƯU LOCAL


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



        except Exception as e:


            print("Local save:", e)






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
    # KIỂM TRA ĐĂNG KÝ HỌC SINH
    # =========================

    def validate_student_register(self):


        if self.student_name.value.strip() == "":

            return False, "Chưa nhập họ tên"



        if self.student_class.value.strip() == "":

            return False, "Chưa nhập lớp"



        if self.student_password.value == "":

            return False, "Chưa nhập mật khẩu"



        if self.student_password.value != self.student_confirm.value:

            return False, "Mật khẩu xác nhận không khớp"





        for student in self.students:


            if (

                student.get("role") == "student"

                and

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



        try:

            self.page.update()

        except:

            pass






    # =========================
    # TẠO MÃ HỌC SINH
    # =========================

    def create_student_id(self):


        number = 1



        while True:


            student_id = f"HS{number:02d}"


            check = False



            for student in self.students:


                if student.get("id") == student_id:


                    check = True

                    break





            if check == False:


                return student_id




            number += 1
                # =========================
    # LẤY DANH SÁCH HỌC SINH
    # =========================

    def get_students(self):


        result = []



        for student in self.students:


            if student.get("role") == "student":


                result.append(student)




        return result






    # =========================
    # ĐĂNG XUẤT
    # =========================

    def logout(self):


        self.current_user = None


        self.clear_all_form()


        self.show_role_select()






    # =========================
    # CHỌN VAI TRÒ
    # =========================

    def show_role_select(self):


        print("HIEN ROLE SELECT")



        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "BẠN LÀ AI?",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                ft.ElevatedButton(

                    "Admin",

                    width=220,

                    on_click=lambda e:
                    self.show_admin_login()

                ),





                ft.ElevatedButton(

                    "Học sinh",

                    width=220,

                    on_click=lambda e:
                    self.show_student_login()

                )



            ],



            alignment=ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=15



        )



        self.page.update()







    # =========================
    # ĐĂNG NHẬP ADMIN
    # =========================

    def show_admin_login(self):


        self.admin_key_login.value = ""



        def login(e):


            if self.admin_key_login.value.strip() == self.admin_key:



                self.current_user = {


                    "name": "Admin",

                    "role": "admin"


                }



                self.show_admin_home()



            else:


                self.show_message(
                    "Sai key Admin!"
                )





        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "ĐĂNG NHẬP ADMIN",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),



                self.admin_key_login,



                ft.ElevatedButton(

                    "Đăng nhập",

                    width=180,

                    on_click=login

                ),



                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_role_select()

                )



            ],



            alignment=ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=15



        )



        self.page.update()
            # =========================
    # TRANG ADMIN
    # =========================

    def show_admin_home(self):


        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "TRANG QUẢN TRỊ",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                ft.ElevatedButton(

                    "Danh sách học sinh",

                    width=260,

                    on_click=lambda e:
                    self.show_student_list()

                ),




                ft.ElevatedButton(

                    "Thêm học sinh",

                    width=260,

                    on_click=lambda e:
                    self.show_add_student()

                ),





                ft.ElevatedButton(

                    "Quản lý / Xóa học sinh",

                    width=260,

                    on_click=lambda e:
                    self.show_manage_student()

                ),





                ft.ElevatedButton(

                    "Cập nhật điểm",

                    width=260,

                    on_click=lambda e:
                    self.show_update_score()

                ),





                ft.ElevatedButton(

                    "Tìm kiếm học sinh",

                    width=260,

                    on_click=lambda e:
                    self.show_search_student()

                ),





                ft.Divider(),





                ft.ElevatedButton(

                    "Đăng xuất",

                    width=260,

                    on_click=lambda e:
                    self.logout()

                )



            ],



            alignment=ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=12



        )



        self.page.update()






    # =========================
    # ĐĂNG NHẬP HỌC SINH
    # =========================

    def show_student_login(self):


        def login(e):


            name = self.student_login_name.value.strip()


            password = self.student_login_password.value



            if name == "" or password == "":


                self.show_message(
                    "Vui lòng nhập đầy đủ thông tin!"
                )

                return





            for student in self.students:


                if (

                    student.get("role") == "student"

                    and

                    student.get("name") == name

                    and

                    student.get("password") == password

                ):



                    self.current_user = student


                    self.show_student_home()


                    return






            self.show_message(
                "Sai tên hoặc mật khẩu!"
            )





        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "ĐĂNG NHẬP HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                self.student_login_name,




                self.student_login_password,





                ft.ElevatedButton(

                    "Đăng nhập",

                    width=180,

                    on_click=login

                ),




                ft.ElevatedButton(

                    "Đăng ký tài khoản",

                    width=180,

                    on_click=lambda e:
                    self.show_register_student()

                ),




                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_role_select()

                )



            ],



            alignment=ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=15



        )



        self.page.update()
            # =========================
    # ĐĂNG KÝ HỌC SINH
    # =========================

    def show_register_student(self):


        def register(e):


            ok, message = self.validate_student_register()



            if not ok:


                self.show_message(message)

                return





            student = {


                "id": self.create_student_id(),


                "name":
                self.student_name.value.strip(),


                "class":
                self.student_class.value.strip(),


                "password":
                self.student_password.value,


                "score": 0,


                "role": "student",


                "image_proof": ""

            }





            self.students.append(student)



            self.save_data()



            self.show_message(
                "Đăng ký thành công!"
            )



            self.clear_all_form()



            self.show_student_login()





        self.root.content = ft.Column(



            controls=[



                ft.Text(

                    "ĐĂNG KÝ HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                self.student_name,




                self.student_class,




                self.student_password,




                self.student_confirm,





                ft.ElevatedButton(

                    "Hoàn tất đăng ký",

                    width=200,

                    on_click=register

                ),




                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_student_login()

                )



            ],



            alignment=ft.MainAxisAlignment.CENTER,



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=12



        )



        self.page.update()






    # =========================
    # TRANG HỌC SINH
    # =========================

    def show_student_home(self):


        if self.current_user is None:


            self.show_role_select()

            return





        student = self.current_user



        score = float(
            student.get("score", 0)
        )



        if score >= 8:


            rank = "Giỏi"


        elif score >= 6.5:


            rank = "Khá"


        elif score >= 5:


            rank = "Trung bình"


        else:


            rank = "Yếu"





        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "THÔNG TIN HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD

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

                    f"Xếp loại: {rank}",

                    weight=ft.FontWeight.BOLD

                ),





                ft.ElevatedButton(

                    "Đăng xuất",

                    width=180,

                    on_click=lambda e:
                    self.logout()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=12



        )



        self.page.update()
            # =========================
    # DANH SÁCH HỌC SINH
    # =========================

    def show_student_list(self):


        rows = []



        for student in self.students:


            if student.get("role") != "student":

                continue



            rows.append(


                ft.Text(

                    f"{student.get('id')} | "
                    f"{student.get('name')} | "
                    f"Lớp: {student.get('class')} | "
                    f"Điểm: {student.get('score')}",

                    size=16

                )


            )





        if len(rows) == 0:


            rows.append(

                ft.Text(
                    "Chưa có học sinh."
                )

            )





        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "DANH SÁCH HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                ft.Column(

                    controls=rows,

                    spacing=10

                ),




                ft.ElevatedButton(

                    "Quay lại",

                    width=180,

                    on_click=lambda e:
                    self.show_admin_home()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=15,



            scroll=ft.ScrollMode.AUTO



        )



        self.page.update()






    # =========================
    # THÊM HỌC SINH
    # =========================

    def show_add_student(self):


        def add_student(e):


            name = self.new_name.value.strip()



            if name == "":


                self.show_message(
                    "Chưa nhập họ tên!"
                )

                return





            if not self.check_score(
                self.new_score.value
            ):


                self.show_message(
                    "Điểm không hợp lệ!"
                )

                return





            student = {



                "id":

                self.new_id.value.strip()

                if self.new_id.value.strip()

                else

                self.create_student_id(),





                "name": name,



                "class":

                "Chưa xếp lớp",





                "password":

                "123456",





                "score":

                float(self.new_score.value),





                "role":

                "student",





                "image_proof":

                ""

            }





            self.students.append(student)



            self.save_data()



            self.show_message(
                "Đã thêm học sinh!"
            )



            self.clear_all_form()



            self.show_student_list()





        self.root.content = ft.Column(



            controls=[



                ft.Text(

                    "THÊM HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                self.new_id,




                self.new_name,




                self.new_score,





                ft.ElevatedButton(

                    "Thêm",

                    width=180,

                    on_click=add_student

                ),




                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_admin_home()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=12



        )



        self.page.update()
            # =========================
    # CẬP NHẬT ĐIỂM
    # =========================

    def show_update_score(self):


        def update(e):


            sid = self.edit_student_id.value.strip().upper()



            if sid == "":


                self.show_message(
                    "Chưa nhập mã học sinh!"
                )

                return





            if not self.check_score(
                self.edit_score.value
            ):


                self.show_message(
                    "Điểm phải từ 0 đến 10!"
                )

                return





            for student in self.students:


                if (

                    student.get("role") == "student"

                    and

                    student.get("id","").upper()
                    ==
                    sid

                ):


                    student["score"] = float(
                        self.edit_score.value
                    )


                    self.save_data()



                    self.show_message(
                        "Đã cập nhật điểm!"
                    )



                    self.show_admin_home()


                    return






            self.show_message(
                "Không tìm thấy học sinh!"
            )






        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "CẬP NHẬT ĐIỂM",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                self.edit_student_id,




                self.edit_score,





                ft.ElevatedButton(

                    "Lưu",

                    width=180,

                    on_click=update

                ),




                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_admin_home()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=12



        )



        self.page.update()






    # =========================
    # TÌM KIẾM HỌC SINH
    # =========================

    def show_search_student(self):


        keyword = ft.TextField(

            label="Nhập mã hoặc tên học sinh"

        )


        result = ft.Column()





        def search(e):


            result.controls.clear()



            key = keyword.value.strip().lower()



            if key == "":


                self.show_message(
                    "Chưa nhập từ khóa!"
                )

                return





            found = False



            for student in self.students:


                if student.get("role") != "student":

                    continue




                sid = student.get("id","").lower()


                name = student.get("name","").lower()



                if key in sid or key in name:


                    found = True



                    result.controls.append(

                        ft.Text(

                            f"{student.get('id')} | "
                            f"{student.get('name')} | "
                            f"Lớp {student.get('class')} | "
                            f"Điểm {student.get('score')}"

                        )

                    )






            if found == False:


                result.controls.append(

                    ft.Text(
                        "Không tìm thấy."
                    )

                )



            self.page.update()






        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "TÌM KIẾM HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                keyword,




                ft.ElevatedButton(

                    "Tìm",

                    width=180,

                    on_click=search

                ),




                result,





                ft.TextButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_admin_home()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=12,



            scroll=ft.ScrollMode.AUTO



        )



        self.page.update()
            # =========================
    # QUẢN LÝ / XÓA HỌC SINH
    # =========================

    def show_manage_student(self):


        rows = []



        for student in self.students:


            if student.get("role") != "student":

                continue





            rows.append(


                ft.Row(

                    controls=[



                        ft.Text(

                            f"{student.get('id')} | "
                            f"{student.get('name')}",

                            expand=True

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





        if len(rows) == 0:


            rows.append(

                ft.Text(
                    "Chưa có học sinh."
                )

            )





        self.root.content = ft.Column(


            controls=[



                ft.Text(

                    "QUẢN LÝ HỌC SINH",

                    size=30,

                    weight=ft.FontWeight.BOLD

                ),




                ft.Column(

                    controls=rows,

                    spacing=10

                ),




                ft.ElevatedButton(

                    "Quay lại",

                    width=180,

                    on_click=lambda e:
                    self.show_admin_home()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER,



            spacing=15,



            scroll=ft.ScrollMode.AUTO



        )



        self.page.update()






    # =========================
    # XÓA HỌC SINH
    # =========================

    def delete_student(self, student_id):


        for student in self.students:


            if student.get("id") == student_id:


                self.students.remove(student)


                self.save_data()


                self.show_message(
                    "Đã xóa học sinh!"
                )


                self.show_manage_student()


                return






        self.show_message(
            "Không tìm thấy học sinh!"
        )






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




            if "image_proof" not in student:


                student["image_proof"] = ""







    # =========================
    # LÀM MỚI
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