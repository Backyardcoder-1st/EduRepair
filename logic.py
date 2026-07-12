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

        self.file = "students.json"

        self.root = ft.Container()


        self.db_url = base64.b64decode(
            "aHR0cHM6Ly9icm90aGVyczFnb2FsLWRlZmF1bHQtcnRkYi5maXJlYmFzZWlvLmNvbS9zdHVkZW50cy5qc29u"
        ).decode("utf-8")


        self.students = []

        self.current_user = None


        # KEY ADMIN CỐ ĐỊNH

        self.admin_key = "123"



        # ================= FORM LOGIN =================


        self.admin_key_login = ft.TextField(
            label="Nhập key Admin",
            password=True,
            can_reveal_password=True
        )



        self.student_login_name = ft.TextField(
            label="Tên học sinh"
        )


        self.student_login_password = ft.TextField(
            label="Mật khẩu",
            password=True,
            can_reveal_password=True
        )




        # ================= FORM ĐĂNG KÝ =================


        self.student_name = ft.TextField(
            label="Họ tên học sinh"
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




        # ================= ADMIN THÊM HS =================


        self.new_id = ft.TextField(
            label="Mã học sinh"
        )


        self.new_name = ft.TextField(
            label="Tên học sinh"
        )


        self.new_score = ft.TextField(
            label="Điểm"
        )



        # ================= NÂNG ĐIỂM =================


        self.edit_student_id = ft.TextField(
            label="Mã học sinh"
        )


        self.edit_score = ft.TextField(
            label="Điểm mới"
        )



    # ================= RESET FORM =================


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
            # ================= LOAD DATA =================


    def load_data(self):


        try:


            req = urllib.request.Request(

                self.db_url,

                headers={

                    "User-Agent": "Mozilla/5.0",

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


                    self.students = []


                    for item in data.values():


                        if isinstance(item, dict):

                            self.students.append(item)




                elif isinstance(data, list):


                    self.students = data



                if self.students:

                    return



        except Exception as e:


            print(
                "Firebase load lỗi:",
                e
            )






        # ================= ĐỌC FILE LOCAL =================


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



                        if self.students:

                            return



        except Exception as e:


            print(
                "File local lỗi:",
                e
            )







        # ================= DỮ LIỆU MẶC ĐỊNH =================


        self.students = [


            {

                "id": "HS01",

                "name": "Nguyễn Văn A",

                "class": "A1",

                "password": "123456",

                "score": 8,

                "role": "student"

            },


            {

                "id": "HS02",

                "name": "Trần Thị B",

                "class": "A1",

                "password": "123456",

                "score": 6,

                "role": "student"

            }


        ]






    # ================= SAVE DATA =================


    def save_data(self):


        data = {}



        for student in self.students:


            if isinstance(student, dict):


                if "id" in student:


                    data[student["id"]] = student






        # Lưu Firebase


        try:


            req = urllib.request.Request(


                self.db_url,


                data=json.dumps(

                    data,

                    ensure_ascii=False

                ).encode("utf-8"),



                headers={


                    "Content-Type":

                    "application/json",


                    "User-Agent":

                    "Mozilla/5.0"


                },


                method="PUT"

            )



            urllib.request.urlopen(


                req,

                timeout=5,

                context=_context

            )



        except Exception as e:


            print(

                "Firebase save lỗi:",

                e

            )







        # Lưu máy


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


            print(

                "Lưu file lỗi:",

                e

            )
                # ================= CHỌN VAI TRÒ =================


    def show_role_select(self):


        self.root.content = ft.Column(

            [


                ft.Text(

                    "Hệ thống quản lý học sinh",

                    size=30

                ),



                ft.ElevatedButton(

                    "Admin",

                    on_click=lambda e:
                    self.show_admin_login()

                ),




                ft.ElevatedButton(

                    "Học sinh",

                    on_click=lambda e:
                    self.show_student_login()

                )



            ],


            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER


        )



        self.page.update()







    # ================= ĐĂNG NHẬP ADMIN =================


    def show_admin_login(self):



        def login(e):


            key = self.admin_key_login.value.strip()



            if key == self.admin_key:



                self.current_user = {


                    "name": "Admin",

                    "role": "admin"


                }



                self.show_admin_home()



            else:



                self.show_message(

                    "Sai key Admin"

                )







        self.root.content = ft.Column(

            [


                ft.Text(

                    "Đăng nhập Admin",

                    size=30

                ),



                self.admin_key_login,




                ft.ElevatedButton(

                    "Đăng nhập",

                    on_click=login

                ),





                ft.ElevatedButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_role_select()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER


        )



        self.page.update()








    # ================= TRANG ADMIN =================


    def show_admin_home(self):



        self.root.content = ft.Column(

            [



                ft.Text(

                    "Trang quản lý Admin",

                    size=30

                ),




                ft.ElevatedButton(

                    "Xem danh sách học sinh",

                    on_click=lambda e:
                    self.show_student_list()

                ),





                ft.ElevatedButton(

                    "Thêm học sinh",

                    on_click=lambda e:
                    self.show_add_student()

                ),




                ft.ElevatedButton(

                    "Xóa học sinh",

                    on_click=lambda e:
                    self.show_manage_student()

                ),




                ft.ElevatedButton(

                    "Nâng điểm",

                    on_click=lambda e:
                    self.show_update_score()

                ),




                ft.ElevatedButton(

                    "Tìm kiếm",

                    on_click=lambda e:
                    self.show_search_student()

                ),




                ft.ElevatedButton(

                    "Thống kê",

                    on_click=lambda e:
                    self.show_statistics()

                ),





                ft.ElevatedButton(

                    "Đăng xuất",

                    on_click=lambda e:
                    self.logout()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER


        )



        self.page.update()
            # ================= ĐĂNG NHẬP HỌC SINH =================


    def show_student_login(self):


        def login(e):


            name = self.student_login_name.value.strip()

            password = self.student_login_password.value.strip()



            for student in self.students:


                if (

                    student.get("role") == "student"

                    and student.get("name") == name

                    and student.get("password") == password

                ):



                    self.current_user = student


                    self.show_student_home()


                    return





            self.show_message(

                "Sai tên hoặc mật khẩu"

            )








        self.root.content = ft.Column(

            [



                ft.Text(

                    "Đăng nhập học sinh",

                    size=30

                ),




                self.student_login_name,



                self.student_login_password,




                ft.ElevatedButton(

                    "Đăng nhập",

                    on_click=login

                ),





                ft.ElevatedButton(

                    "Đăng ký học sinh",

                    on_click=lambda e:
                    self.show_register_student()

                ),




                ft.ElevatedButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_role_select()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER


        )



        self.page.update()







    # ================= ĐĂNG KÝ HỌC SINH =================


    def show_register_student(self):



        def register(e):


            name = self.student_name.value.strip()

            cls = self.student_class.value.strip()

            password = self.student_password.value.strip()

            confirm = self.student_confirm.value.strip()





            if name == "" or cls == "" or password == "":


                self.show_message(

                    "Nhập đầy đủ thông tin"

                )

                return






            if password != confirm:


                self.show_message(

                    "Mật khẩu không trùng"

                )

                return







            for student in self.students:



                if student.get("name") == name:



                    self.show_message(

                        "Tên đã tồn tại"

                    )

                    return






            new_student = {


                "id":

                self.create_student_id(),



                "name":

                name,



                "class":

                cls,



                "password":

                password,



                "score":

                0,



                "role":

                "student"


            }






            self.students.append(

                new_student

            )



            self.save_data()





            self.clear_register()



            self.show_message(

                "Đăng ký thành công"

            )



            self.show_student_login()








        self.root.content = ft.Column(

            [


                ft.Text(

                    "Đăng ký học sinh",

                    size=30

                ),




                self.student_name,



                self.student_class,



                self.student_password,



                self.student_confirm,





                ft.ElevatedButton(

                    "Đăng ký",

                    on_click=register

                ),





                ft.ElevatedButton(

                    "Quay lại",

                    on_click=lambda e:
                    self.show_student_login()

                )



            ],



            horizontal_alignment=
            ft.CrossAxisAlignment.CENTER


        )



        self.page.update()






    # ================= XÓA FORM ĐĂNG KÝ =================


    def clear_register(self):


        self.student_name.value = ""

        self.student_class.value = ""

        self.student_password.value = ""

        self.student_confirm.value = ""


        self.page.update()
            # ================= TRANG HỌC SINH =================


    def show_student_home(self):


        student = self.current_user



        if student is None:


            self.show_role_select()

            return






        score = student.get(

            "score",

            0

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

            [




                ft.Text(

                    "Thông tin học sinh",

                    size=30

                ),





                ft.Text(

                    "Mã: "

                    + str(student.get("id"))

                ),





                ft.Text(

                    "Họ tên: "

                    + str(student.get("name"))

                ),





                ft.Text(

                    "Lớp: "

                    + str(student.get("class"))

                ),





                ft.Text(

                    "Điểm: "

                    + str(score)

                ),




                ft.Text(

                    "Xếp loại: "

                    + rank

                ),





                ft.ElevatedButton(

                    "Đăng xuất",

                    on_click=lambda e:

                    self.logout()

                )



            ],



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER


        )




        self.page.update()










    # ================= DANH SÁCH HỌC SINH =================



    def show_student_list(self):


        controls = [


            ft.Text(

                "Danh sách học sinh",

                size=30

            )

        ]





        for student in self.students:



            if student.get("role") == "student":



                controls.append(


                    ft.Text(


                        f"{student.get('id')} - "

                        f"{student.get('name')} - "

                        f"Lớp {student.get('class')} - "

                        f"Điểm {student.get('score')}"



                    )


                )







        controls.append(



            ft.ElevatedButton(

                "Quay lại",

                on_click=lambda e:

                self.show_admin_home()

            )



        )







        self.root.content = ft.Column(


            controls,


            scroll=ft.ScrollMode.AUTO,


            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER



        )




        self.page.update()
            # ================= THÊM HỌC SINH =================


    def show_add_student(self):


        def add(e):


            name = self.new_name.value.strip()



            if name == "":


                self.show_message(

                    "Chưa nhập tên"

                )

                return





            try:


                score = int(

                    self.new_score.value

                )


            except:


                score = 0






            if score < 0 or score > 10:


                self.show_message(

                    "Điểm từ 0 đến 10"

                )

                return







            if self.new_id.value.strip() != "":


                student_id = self.new_id.value.strip()



                for s in self.students:



                    if s.get("id") == student_id:


                        self.show_message(

                            "Mã đã tồn tại"

                        )

                        return




            else:


                student_id = self.create_student_id()







            student = {



                "id":

                student_id,



                "name":

                name,



                "class":

                "Chưa có",



                "password":

                "123456",



                "score":

                score,



                "role":

                "student"



            }







            self.students.append(student)



            self.save_data()



            self.show_message(

                "Thêm thành công"

            )



            self.clear_add_student()



            self.show_student_list()






        self.root.content = ft.Column(



            [



                ft.Text(

                    "Thêm học sinh",

                    size=30

                ),





                self.new_id,



                self.new_name,



                self.new_score,





                ft.ElevatedButton(

                    "Thêm",

                    on_click=add

                ),





                ft.ElevatedButton(

                    "Quay lại",

                    on_click=lambda e:

                    self.show_admin_home()

                )



            ],



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER



        )




        self.page.update()







    # ================= XÓA FORM THÊM =================


    def clear_add_student(self):


        self.new_id.value = ""

        self.new_name.value = ""

        self.new_score.value = ""


        self.page.update()







    # ================= TẠO ID HỌC SINH =================


    def create_student_id(self):


        number = 1



        while True:



            new_id = (

                "HS"

                + str(number).zfill(2)

            )



            exists = False




            for student in self.students:



                if student.get("id") == new_id:



                    exists = True

                    break






            if exists == False:


                return new_id




            number += 1
                # ================= QUẢN LÝ HỌC SINH =================


    def show_manage_student(self):


        controls = [


            ft.Text(

                "Quản lý học sinh",

                size=30

            )


        ]





        for student in self.students:



            if student.get("role") == "student":



                sid = student.get("id")





                controls.append(



                    ft.Row(



                        [



                            ft.Text(



                                f"{sid} - "

                                f"{student.get('name')} - "

                                f"Điểm {student.get('score')}"



                            ),





                            ft.ElevatedButton(



                                "Xóa",



                                on_click=lambda e, x=sid:

                                self.delete_student(x)



                            )



                        ]



                    )



                )







        controls.append(



            ft.ElevatedButton(



                "Quay lại",



                on_click=lambda e:

                self.show_admin_home()



            )



        )








        self.root.content = ft.Column(



            controls,



            scroll=ft.ScrollMode.AUTO,



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER



        )



        self.page.update()








    # ================= XÓA HỌC SINH =================



    def delete_student(self, student_id):



        for student in self.students[:]:




            if (



                student.get("id") == student_id

                and student.get("role") == "student"



            ):



                self.students.remove(student)



                self.save_data()



                self.show_message(

                    "Đã xóa học sinh"

                )



                self.show_manage_student()



                return





        self.show_message(

            "Không tìm thấy học sinh"

        )










    # ================= NÂNG ĐIỂM =================



    def show_update_score(self):



        def update(e):


            try:


                score = int(

                    self.edit_score.value

                )



            except:


                self.show_message(

                    "Điểm phải là số"

                )

                return






            if score < 0 or score > 10:



                self.show_message(

                    "Điểm từ 0 đến 10"

                )

                return





            self.update_score(


                self.edit_student_id.value,


                score


            )



            self.show_message(

                "Cập nhật điểm xong"

            )









        self.root.content = ft.Column(



            [



                ft.Text(

                    "Nâng điểm học sinh",

                    size=30

                ),




                self.edit_student_id,



                self.edit_score,






                ft.ElevatedButton(



                    "Cập nhật",



                    on_click=update



                ),




                ft.ElevatedButton(



                    "Quay lại",



                    on_click=lambda e:

                    self.show_admin_home()



                )



            ],



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER



        )




        self.page.update()








    # ================= CẬP NHẬT ĐIỂM =================



    def update_score(self, student_id, score):


        for student in self.students:



            if (



                student.get("id") == student_id

                and student.get("role") == "student"



            ):



                student["score"] = score



                self.save_data()



                return






        self.show_message(

            "Không tìm thấy học sinh"

        )
            # ================= TÌM KIẾM HỌC SINH =================


    def search_student(self, keyword):


        result = []


        keyword = keyword.lower().strip()



        for student in self.students:



            if student.get("role") == "student":



                name = str(
                    student.get("name", "")
                ).lower()



                sid = str(
                    student.get("id", "")
                ).lower()





                if (

                    keyword in name

                    or keyword in sid

                ):


                    result.append(student)





        return result







    def show_search_student(self):


        keyword = ft.TextField(

            label="Nhập tên hoặc mã học sinh"

        )



        result_box = ft.Column()






        def search(e):


            result_box.controls.clear()



            data = self.search_student(

                keyword.value

            )





            if len(data) == 0:



                result_box.controls.append(


                    ft.Text(

                        "Không tìm thấy"

                    )



                )





            else:



                for student in data:



                    result_box.controls.append(



                        ft.Text(



                            f"{student.get('id')} - "

                            f"{student.get('name')} - "

                            f"Điểm {student.get('score')}"



                        )



                    )






            self.page.update()







        self.root.content = ft.Column(



            [



                ft.Text(

                    "Tìm kiếm học sinh",

                    size=30

                ),




                keyword,






                ft.ElevatedButton(



                    "Tìm kiếm",



                    on_click=search



                ),






                result_box,






                ft.ElevatedButton(



                    "Quay lại",



                    on_click=lambda e:

                    self.show_admin_home()



                )



            ],



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER



        )




        self.page.update()
            # ================= LẤY DANH SÁCH HỌC SINH =================


    def get_students(self):


        result = []



        for student in self.students:



            if student.get("role") == "student":


                result.append(student)





        return result







    # ================= THỐNG KÊ =================



    def get_statistics(self):


        total = 0

        gioi = 0

        kha = 0

        trung_binh = 0

        yeu = 0






        for student in self.students:



            if student.get("role") == "student":



                total += 1



                score = student.get(

                    "score",

                    0

                )





                if score >= 8:



                    gioi += 1





                elif score >= 6.5:



                    kha += 1





                elif score >= 5:



                    trung_binh += 1





                else:



                    yeu += 1






        return {



            "total":

            total,



            "gioi":

            gioi,



            "kha":

            kha,



            "trung_binh":

            trung_binh,



            "yeu":

            yeu



        }









    # ================= TRANG THỐNG KÊ =================



    def show_statistics(self):


        data = self.get_statistics()





        self.root.content = ft.Column(



            [



                ft.Text(



                    "Thống kê học sinh",

                    size=30

                ),





                ft.Text(

                    f"Tổng số học sinh: {data['total']}"

                ),





                ft.Text(

                    f"Học sinh Giỏi: {data['gioi']}"

                ),





                ft.Text(

                    f"Học sinh Khá: {data['kha']}"

                ),





                ft.Text(

                    f"Trung bình: {data['trung_binh']}"

                ),





                ft.Text(

                    f"Yếu: {data['yeu']}"

                ),





                ft.ElevatedButton(



                    "Quay lại",



                    on_click=lambda e:

                    self.show_admin_home()



                )



            ],



            horizontal_alignment=

            ft.CrossAxisAlignment.CENTER



        )




        self.page.update()










    # ================= TÌM HỌC SINH THEO ID =================



    def get_student_by_id(self, student_id):


        for student in self.students:



            if student.get("id") == student_id:


                return student




        return None
            # ================= THÔNG BÁO =================


    def show_message(self, message):


        try:


            self.page.snack_bar = ft.SnackBar(

                content=ft.Text(message)

            )



            self.page.snack_bar.open = True



            self.page.update()




        except Exception as e:


            print(

                "SnackBar lỗi:",

                e

            )









    # ================= ĐĂNG XUẤT =================



    def logout(self):


        self.current_user = None



        self.clear_all_form()



        self.show_role_select()










    # ================= KIỂM TRA ĐIỂM =================



    def check_score(self, score):


        try:


            score = float(score)



        except:



            return False





        if score < 0 or score > 10:


            return False




        return True







    # ================= RESET LOGIN =================



    def clear_student_login(self):


        self.student_login_name.value = ""


        self.student_login_password.value = ""



        self.page.update()







    # ================= KIỂM TRA ĐĂNG KÝ =================



    def validate_student_register(self):


        if self.student_name.value.strip() == "":


            return False, "Chưa nhập họ tên"





        if self.student_class.value.strip() == "":


            return False, "Chưa nhập lớp"





        if self.student_password.value.strip() == "":


            return False, "Chưa nhập mật khẩu"





        if self.student_password.value != self.student_confirm.value:



            return False, "Mật khẩu không trùng"





        return True, ""









    # ================= START APP =================



    def start(self):


        self.load_data()


        self.show_role_select()