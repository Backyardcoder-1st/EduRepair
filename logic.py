import flet as ft
import json
import os
import urllib.request
import urllib.error
import ssl
import base64
import shutil
import io
from PIL import Image
import requests
import openpyxl
from google.oauth2.service_account import Credentials
import gspread
import traceback
import time

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
        self.history = []

        self.current_user = None

        # key admin

        self.admin_key = "123"

        # Temporary Base64 holder for image uploads
        self.temp_image_base64 = None

        # Inside __init__ in logic.py:
        self.page.on_route_change = self.handle_route_change

        # Inside __init__ in logic.py:
        self.file_picker = ft.FilePicker(
            on_result=self.on_file_picker_result,
            on_upload=self.on_file_upload_complete
        )
        self.page.overlay.append(self.file_picker)

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
    # ĐỌC DỮ LIỆU FIREBASE + LOCAL (FIXED)
    # =========================

    def load_data(self):
        # =========================
        # 1. LOAD STUDENTS
        # =========================
        loaded_students = False
        try:
            request = urllib.request.Request(self.db_url, method="GET")
            with urllib.request.urlopen(request, timeout=5, context=_context) as response:
                data = json.loads(response.read().decode())
                if isinstance(data, dict):
                    self.students = list(data.values())
                    loaded_students = True
                elif isinstance(data, list):
                    self.students = data
                    loaded_students = True
                print("Firebase students load thành công")
        except Exception as e:
            print("Firebase students đọc lỗi:", e)

        if not loaded_students:
            if os.path.exists(self.file):
                try:
                    with open(self.file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self.students = data
                except Exception as ex:
                    print("Lỗi đọc file local students.json:", ex)
            if not hasattr(self, "students") or self.students is None:
                self.students = []

        # =========================
        # 2. LOAD HISTORY FROM TOP-LEVEL ROOT NODE
        # =========================
        loaded_history = False
        try:
            base_url = self.db_url.rsplit('/', 1)[0] if '/students' in self.db_url else self.db_url.rsplit('.json', 1)[0]
            history_db_url = f"{base_url}/history.json"

            request = urllib.request.Request(history_db_url, method="GET")
            with urllib.request.urlopen(request, timeout=5, context=_context) as response:
                hist_data = json.loads(response.read().decode())
                if isinstance(hist_data, list):
                    self.history = hist_data
                    loaded_history = True
                elif isinstance(hist_data, dict):
                    self.history = list(hist_data.values())
                    loaded_history = True
                print("Firebase history load thành công từ /history")
        except Exception as e:
            print("Firebase history đọc lỗi:", e)

        if not loaded_history:
            history_file = "history.json"
            if os.path.exists(history_file):
                try:
                    with open(history_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.history = data if isinstance(data, list) else []
                except Exception as e:
                    print("Lỗi đọc file local history.json:", e)
                    self.history = []
            else:
                self.history = []

    def save_data(self):
        # 1. Save local students.json
        try:
            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(self.students, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi ghi local students.json:", e)

        # 2. Sync to Firebase Realtime Database (Students)
        try:
            if hasattr(self, "db_url") and self.db_url:
                req_data = json.dumps(self.students).encode("utf-8")
                request = urllib.request.Request(
                    self.db_url,
                    data=req_data,
                    method="PUT",
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(request, timeout=5, context=_context) as response:
                    pass
        except Exception as e:
            print("Lỗi ghi Firebase students:", e)

        # 3. Save local history.json
        try:
            if hasattr(self, "history") and self.history is not None:
                with open("history.json", "w", encoding="utf-8") as f:
                    json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi ghi file local history.json:", e)

        # 4. Sync to Firebase Realtime Database (History)
        try:
            if hasattr(self, "db_url") and self.db_url and hasattr(self, "history") and self.history is not None:
                base_url = self.db_url.rsplit('/', 1)[0] if '/students' in self.db_url else \
                self.db_url.rsplit('.json', 1)[0]
                history_db_url = f"{base_url}/history.json"

                req_data = json.dumps(self.history).encode("utf-8")
                request = urllib.request.Request(
                    history_db_url,
                    data=req_data,
                    method="PUT",
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(request, timeout=5, context=_context) as response:
                    pass
        except Exception as e:
            print("Lỗi ghi Firebase history:", e)


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

    def process_and_compress_image(file_bytes) -> str:
        """
        Takes raw uploaded image bytes, resizes them proportionally to max 480px,
        compresses JPEG quality to 70%, and returns a Base64 data string.
        """
        try:
            # 1. Open image from raw memory bytes
            img = Image.open(io.BytesIO(file_bytes)).convert("RGB")

            # 2. Proportionally resize max dimension to 480px
            img.thumbnail((480, 480), Image.Resampling.LANCZOS)

            # 3. Save compressed JPEG into an in-memory buffer
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70, optimize=True)

            # 4. Convert compressed bytes to Base64 string
            encoded_string = base64.b64encode(buffer.getvalue()).decode("utf-8")

            return f"data:image/jpeg;base64,{encoded_string}"
        except Exception as e:
            print("Image Compression Error:", e)
            return None

    def trigger_upload_picker(self, e):
        """Opens native OS File Explorer"""
        # Ensure file picker is attached to page overlay
        if self.file_picker not in self.page.overlay:
            self.page.overlay.append(self.file_picker)
            self.page.update()

        self.file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    def pick_image(self, e):
        """Triggers the file picker dialog."""
        self.file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE
        )

    def on_file_picker_result(self, e: ft.FilePickerResultEvent):
        """Triggered as soon as the user selects a file in the browser file dialog."""
        if not e.files:
            return

        f = e.files[0]

        # Local Desktop path execution
        if f.path and os.path.exists(f.path):
            with open(f.path, "rb") as file_data:
                raw_bytes = file_data.read()
            self._process_raw_image_bytes(raw_bytes, f.name)

        # Web Mode execution: Stream directly to server upload endpoint
        else:
            upload_url = self.page.get_upload_url(f.name, 600)
            self.file_picker.upload([
                ft.FilePickerUploadFile(f.name, upload_url=upload_url)
            ])

    def on_file_upload_complete(self, e: ft.FilePickerUploadEvent):
        """Triggered when browser finishes streaming file bytes to the server."""
        if e.progress == 1.0:
            uploaded_path = os.path.join("uploads", e.file_name)
            with open(uploaded_path, "rb") as f:
                raw_bytes = f.read()
            self._process_raw_image_bytes(raw_bytes, e.file_name)

    def _process_raw_image_bytes(self, raw_bytes, file_name):
        """Process raw file bytes into base64 payload without error wrapping."""
        image = Image.open(io.BytesIO(raw_bytes))
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        output = io.BytesIO()
        image.save(output, format="JPEG", quality=70, optimize=True)
        compressed_bytes = output.getvalue()

        encoded = base64.b64encode(compressed_bytes).decode("utf-8")
        self.temp_image_base64 = f"data:image/jpeg;base64,{encoded}"

        self.show_student_progress()


    def handle_route_change(self, e):
        """Lắng nghe dữ liệu Base64 từ JavaScript truyền về"""
        route = self.page.route
        if route and route.startswith("#img_upload:"):
            # Lấy chuỗi base64 thực sự
            raw_base64 = route.replace("#img_upload:", "")

            # Xóa hash trên thanh địa chỉ để không bị lặp
            self.page.route = "/"

            # Chuyển Base64 sang dạng bytes và thực hiện nén
            try:
                # Tách phần header data:image/jpeg;base64, nếu có
                if "," in raw_base64:
                    header, encoded = raw_base64.split(",", 1)
                    file_bytes = base64.b64decode(encoded)
                else:
                    file_bytes = base64.b64decode(raw_base64)

                # Nén ảnh 480px và cập nhật giao diện
                self.handle_image_selected(file_bytes)
            except Exception as err:
                print("Lỗi giải mã ảnh từ JS:", err)

    # =========================
    # SAVE CHÍNH
    # =========================


    #======================
    # START APP
    #======================

    def start(self):
        self.load_data()
        self.check_data()
        self.show_role_select()

    # =========================
    # KIỂM TRA DỮ LIỆU
    # =========================

    def check_data(self):
        # Automatically purge glitched accounts on startup
        self.purge_glitched_accounts()

        if self.students is None or not isinstance(self.students, list):
            self.students = []

        # Filter out any corrupt / non-dictionary entries
        self.students = [student for student in self.students if isinstance(student, dict)]

        for student in self.students:
            if "score" not in student:
                student["score"] = 0
            if "tasks" not in student or not isinstance(student["tasks"], list):
                student["tasks"] = []

    def generate_student_id(self, class_name):
        if not class_name:
            return "HS01A1"

        # Clean target class string (e.g., "A1", "A10")
        target_class = str(class_name).replace("Lớp ", "").replace("lớp ", "").strip().upper()
        existing_numbers = []

        # Scan all existing students belonging to this class
        for student in self.students:
            if not isinstance(student, dict):
                continue

            st_class = str(student.get("class", "")).replace("Lớp ", "").replace("lớp ", "").strip().upper()
            if st_class == target_class:
                st_id = str(student.get("id", "")).strip().upper()

                # Parse IDs following HS[numerical order][Class] format (e.g. HS01A1)
                if st_id.startswith("HS"):
                    numeric_part = st_id[2:]
                    if numeric_part.endswith(target_class):
                        numeric_part = numeric_part[:-len(target_class)]
                        try:
                            num = int(numeric_part)
                            existing_numbers.append(num)
                        except ValueError:
                            pass

        if not existing_numbers:
            return f"HS01{target_class}"

        next_number = max(existing_numbers) + 1
        return f"HS{next_number:02d}{target_class}"

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

    #=========================
    #File lưu trữ công việc
    #=========================
    def load_history(self):
        """Reads local history.json if available"""
        if not os.path.exists("history.json"):
            return []
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def sync_history_firebase(self, history_data):
        """Creates/Updates history.json endpoint in Firebase Realtime Database"""
        try:
            # Construct endpoint URL for history.json
            history_url = self.db_url.rsplit('/', 1)[0] + "/history.json"

            data = json.dumps(history_data, ensure_ascii=False).encode("utf-8")
            request = urllib.request.Request(
                history_url,
                data=data,
                method="PUT",
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(request, timeout=8, context=_context) as response:
                print("Firebase history sync OK")
                return True
        except Exception as e:
            print("Firebase history sync error:", e)
            return False

    def save_history_record(self, record):
        """Saves history record locally and syncs to Firebase history.json automatically"""
        history = self.load_history()
        history.append(record)

        # 1. Save local history.json
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving local history: {e}")

        # 2. Sync to Firebase Realtime Database automatically
        self.sync_history_firebase(history)

    def build_upload_box(self):
        """Builds the upload box with updated placeholder text and preview"""
        if self.temp_image_base64:
            # Clean base64 string if data URI prefix exists
            b64_data = (
                self.temp_image_base64.split(",")[-1]
                if "," in self.temp_image_base64
                else self.temp_image_base64
            )

            box_content = ft.Column(
                controls=[
                    ft.Image(
                        src_base64=b64_data,
                        width=220,
                        height=130,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=8
                    ),
                    ft.Text("Chạm để đổi ảnh khác", size=11, color=self.gray)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4
            )
        else:
            box_content = ft.Row(
                controls=[
                    ft.Icon(ft.icons.CLOUD_UPLOAD_OUTLINED, size=22, color=self.blue),
                    ft.Text("Chạm vào đây để nộp ảnh minh chứng", size=13, color=self.dark, weight=ft.FontWeight.W_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            )

        return ft.Container(
            content=box_content,
            padding=14,
            border=ft.border.all(1, self.blue),
            border_radius=10,
            bgcolor="#EFF6FF",
            on_click=self.trigger_upload_picker
        )

    def purge_glitched_accounts(self):
        """Scans for glitched accounts like '1' and removes them permanently."""
        if not isinstance(self.students, list):
            return

        initial_count = len(self.students)

        # Filter out any student named "1" or with ID "1"
        self.students = [
            s for s in self.students
            if isinstance(s, dict) and str(s.get("name", "")).strip() != "1" and str(s.get("id", "")).strip() != "1"
        ]

        # If glitched accounts were found and removed, save the cleaned data immediately
        if len(self.students) < initial_count:
            print("Detected glitched account '1'. Purging from database...")
            self.save_data()


    # =========================
    # CẬP NHẬT TRẠNG THÁI KHUNG UPLOAD
    # =========================
    def handle_image_selected(self, file_bytes):
        if not file_bytes:
            return

        # 1. Trạng thái đang xử lý
        self.upload_status_icon.visible = False
        self.upload_progress.visible = True
        self.upload_status_text.value = "Đang xử lý ảnh..."
        self.upload_status_text.color = self.orange
        self.page.update()

        # 2. Nén ảnh
        compressed_base64 = self.process_and_compress_image(file_bytes)

        # 3. Trạng thái kết quả
        if compressed_base64:
            self.temp_image_base64 = compressed_base64

            self.upload_progress.visible = False
            self.upload_status_icon.name = "check_circle"  # Direct string name
            self.upload_status_icon.color = self.green
            self.upload_status_icon.visible = True

            self.upload_status_text.value = "Đã tải ảnh lên thành công!"
            self.upload_status_text.color = self.green

            # Mở khóa nút Nộp bài (Chuyển sang Xanh)
            if hasattr(self, "submit_btn") and self.submit_btn:
                self.submit_btn.disabled = False
                self.submit_btn.bgcolor = self.blue
        else:
            self.temp_image_base64 = None

            self.upload_progress.visible = False
            self.upload_status_icon.name = "error"         # Direct string name
            self.upload_status_icon.color = self.red
            self.upload_status_icon.visible = True

            self.upload_status_text.value = "Lỗi xử lý ảnh, thử lại!"
            self.upload_status_text.color = self.red

            # Khóa nút Nộp bài (Giữ màu Xám)
            if hasattr(self, "submit_btn") and self.submit_btn:
                self.submit_btn.disabled = True
                self.submit_btn.bgcolor = self.gray

        self.page.update()

    # =========================
    # NỘP BÀI TỰ ĐỘNG LƯU DATABASE
    # =========================
    def submit_proof(self, task_index):
        """Submits task proof with image and updates status for Admin review"""
        if not self.temp_image_base64:
            self.show_message("Vui lòng đính kèm ảnh minh chứng!")
            return

        tasks = self.current_user.get("tasks", [])
        if 0 <= task_index < len(tasks):
            # Flag task as pending approval and attach image
            tasks[task_index]["status"] = "pending_approval"
            tasks[task_index]["proof_image"] = self.temp_image_base64

            # Save updated students list (local + Firebase)
            self.save_data()

            # Reset temp image container
            self.temp_image_base64 = None

            self.show_message("Gửi báo cáo kết quả thành công!")
            self.show_student_progress()

    def show_message(self, msg):
        snack = ft.SnackBar(content=ft.Text(msg))
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()

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
        # Dedicated error message label styled to match your login_error_text
        self.admin_error_text = ft.Text("", color=self.red, size=13, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

        def login(e):
            key = self.admin_key_login.value.strip()

            # 1. Check empty password
            if not key:
                self.admin_error_text.value = "Nhập mật khẩu"
                self.page.update()
                return

            # 2. Check correct password
            if key == self.admin_key:
                self.admin_error_text.value = ""
                self.current_user = {
                    "role": "admin",
                    "name": "Võ Thị Yến Nhi"
                }
                self.show_admin_home()
            else:
                # 3. Wrong password
                self.admin_error_text.value = "Sai mật khẩu"
                self.page.update()

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

                self.admin_error_text, # <--- Inline error message label

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
                "name": self.student_name.value.strip(),
                "id": self.generate_student_id(self.student_class.value),
                "class": self.student_class.value,
                "password": self.student_password.value,
                "score": 0,
                "tasks": []
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

                return#

    #=========================
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
                feature_card("Lớp học", "🏫", "#7C3AED", "#F3E8FF", lambda e: self.show_admin_classes()),
                feature_card("Danh sách đăng kí", "📝", self.blue, "#EFF6FF", lambda e: self.show_admin_registration_list()),
                feature_card("Tiến trình lao động", "⏳", self.orange, "#FFF7ED", lambda e: self.show_admin_labor_progress()),
                feature_card("Kết quả lao động", "✅", self.green, "#F0FDF4", lambda e: self.show_admin_labor_results()),
                feature_card("Lỗi vi phạm", "⚠️", self.red, "#FEF2F2", lambda e: self.show_message("Chức năng 'Lỗi vi phạm' đang phát triển!")),
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(dashboard_content, 380)
        self.page.update()

        # =========================
        # ADMIN: TIẾN TRÌNH LAO ĐỘNG (XEM CÔNG VIỆC ĐANG THỰC HIỆN)
        # =========================
    def show_admin_labor_progress(self):
            self.load_data()
            self.check_data()

            top_bar = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=1,
                        controls=[
                            ft.Text("TIẾN TRÌNH LAO ĐỘNG", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                            ft.Text("Công việc học sinh đang thực hiện", size=11, color=self.orange)
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

            progress_cards = []

            for student in self.students:
                if not isinstance(student, dict) or "tasks" not in student:
                    continue

                tasks = student.get("tasks", [])
                if not isinstance(tasks, list):
                    continue

                for task in tasks:
                    if not isinstance(task, dict):
                        continue

                    status = task.get("status")
                    # Strictly only show active/in-progress tasks
                    if status in ["in_progress", "Đang rèn luyện"]:
                        st_name = student.get("name", "N/A")
                        st_class = student.get("class", "")
                        st_id = student.get("id", "")

                        card = ft.Container(
                            padding=12,
                            bgcolor="#FFF7ED",
                            border=ft.Border(
                                top=ft.BorderSide(1, "#FFEDD5"),
                                bottom=ft.BorderSide(1, "#FFEDD5"),
                                left=ft.BorderSide(1, "#FFEDD5"),
                                right=ft.BorderSide(1, "#FFEDD5"),
                            ),
                            border_radius=12,
                            content=ft.Column(
                                spacing=6,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(f"{st_name} ({st_id})", size=12, weight=ft.FontWeight.BOLD,
                                                    color=self.dark),
                                            ft.Container(
                                                padding=ft.Padding(6, 2, 6, 2),
                                                bgcolor="#FFEDD5",
                                                border_radius=6,
                                                content=ft.Text(f"Lớp {st_class}", size=10, color=self.orange,
                                                                weight=ft.FontWeight.BOLD)
                                            )
                                        ]
                                    ),
                                    ft.Text(f"📌 Công việc: {task.get('job', '')}", size=12, weight=ft.FontWeight.BOLD,
                                            color=self.dark),
                                    ft.Text(f"⏱️ Thời gian: {task.get('time', '')}", size=11, color=self.gray),
                                    ft.Text(f"📝 Ghi chú: {task.get('note', '')}", size=11, color=self.gray),
                                    ft.Row(
                                        controls=[
                                            ft.Text("⚡ Trạng thái: Đang rèn luyện", size=11, color=self.orange,
                                                    weight=ft.FontWeight.BOLD)
                                        ]
                                    )
                                ]
                            )
                        )
                        progress_cards.append(card)

            if not progress_cards:
                progress_cards.append(
                    ft.Container(
                        padding=30,
                        alignment=ft.alignment.Alignment(0, 0),
                        content=ft.Text("Hiện chưa có học sinh nào đang trong tiến trình lao động.", size=12,
                                        color=self.gray, text_align=ft.TextAlign.CENTER)
                    )
                )

            list_content = ft.Column(
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                controls=progress_cards
            )

            body = ft.Column(
                spacing=12,
                controls=[
                    top_bar,
                    ft.Container(content=list_content, height=350)
                ]
            )

            card_container = ft.Container(
                content=body,
                width=380,
                padding=20,
                bgcolor=self.white,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
            )

            self.root.content = card_container
            self.page.update()

    # =========================
    # ADMIN: NGHIỆM THU LAO ĐỘNG
    # =========================

    def show_admin_labor_results(self):
        """Displays pending task approvals with zoomable proof image modal and deny/approve buttons"""
        self.load_data()
        self.check_data()

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text("NGHIỆM THU LAO ĐỘNG", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Duyệt hoặc từ chối báo cáo minh chứng", size=11, color=self.gray)
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

        # Zoomable Image Popup Modal
        def open_zoomable_image_popup(b64_data):
            if not b64_data:
                return

            clean_b64 = b64_data.split(",")[-1] if "," in b64_data else b64_data

            state = {
                "scale": 1.0,
                "x": 0.0,
                "y": 0.0
            }

            image_ctrl = ft.Image(
                src_base64=clean_b64,
                fit=ft.ImageFit.CONTAIN,
                width=320,
                height=320,
                scale=1.0,
                offset=ft.Offset(0, 0)
            )

            image_container = ft.Container(
                content=image_ctrl,
                alignment=ft.alignment.center,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                width=320,
                height=320
            )

            def update_transform():
                image_ctrl.scale = state["scale"]
                image_ctrl.offset = ft.Offset(state["x"], state["y"])
                zoom_text.value = f"{int(state['scale'] * 100)}%"
                self.page.update()

            def zoom_in(e):
                if state["scale"] < 5.0:
                    state["scale"] += 0.25
                    update_transform()

            def zoom_out(e):
                if state["scale"] > 0.5:
                    state["scale"] -= 0.25
                    if state["scale"] <= 1.0:
                        state["x"] = 0.0
                        state["y"] = 0.0
                    update_transform()

            def reset_zoom(e):
                state["scale"] = 1.0
                state["x"] = 0.0  # Fixed typo comma here
                state["y"] = 0.0
                update_transform()

            def on_scroll(e: ft.ScrollEvent):
                if e.scroll_delta_y < 0:
                    zoom_in(None)
                else:
                    zoom_out(None)

            def on_pan_update(e: ft.DragUpdateEvent):
                state["x"] += e.delta_x / 200.0
                state["y"] += e.delta_y / 200.0
                update_transform()

            def close_dlg(e):
                dialog.open = False
                self.page.update()

            zoom_text = ft.Text("100%", size=11, weight=ft.FontWeight.BOLD, color=self.gray)

            gesture_wrapper = ft.GestureDetector(
                content=image_container,
                on_scroll=on_scroll,
                on_pan_update=on_pan_update,
                drag_interval=10
            )

            dialog = ft.AlertDialog(
                content_padding=10,
                content=ft.Container(
                    width=340,
                    height=420,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            gesture_wrapper,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=6,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.REMOVE_CIRCLE_OUTLINED,
                                        icon_size=20,
                                        tooltip="Thu nhỏ",
                                        on_click=zoom_out
                                    ),
                                    zoom_text,
                                    ft.IconButton(
                                        icon=ft.icons.ADD_CIRCLE_OUTLINED,
                                        icon_size=20,
                                        tooltip="Phóng to",
                                        on_click=zoom_in
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.REFRESH_OUTLINED,
                                        icon_size=18,
                                        tooltip="Đặt lại",
                                        on_click=reset_zoom
                                    ),
                                    ft.Container(width=10),
                                    ft.TextButton("Đóng", on_click=close_dlg)
                                ]
                            )
                        ]
                    )
                )
            )
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()

        # Task Approval Handler
        def approve_task(self, student_obj, task_obj):
            if isinstance(student_obj.get("tasks"), list) and task_obj in student_obj["tasks"]:
                student_obj["tasks"].remove(task_obj)

            history_entry = {
                "student_id": student_obj.get("id", ""),
                "student_name": student_obj.get("name", ""),
                "class": student_obj.get("class", ""),
                "job": task_obj.get("job", ""),
                "time": task_obj.get("time", ""),
                "note": task_obj.get("note", ""),
                "proof_image": task_obj.get("proof_image", ""),
                "status": "complete",
                "Reason": ""
            }

            if not hasattr(self, "history") or self.history is None:
                self.history = []

            self.history.append(history_entry)
            self.save_data()

            # EXPORT TO SHEET #3 (COMPLETE)
            self.export_labor_acceptance_to_excel(
                student_name=student_obj.get("name", ""),
                student_class=student_obj.get("class", ""),
                job_title=task_obj.get("job", ""),
                job_time=task_obj.get("time", ""),
                status="Complete",
                reason=""
            )

            self.show_message(
                f"Đã duyệt công việc '{task_obj.get('job', 'N/A')}' cho {student_obj.get('name', 'Học sinh')}!"
            )
            self.show_admin_labor_results()

        # Task 3 & 4: Deny Task Handler with Popup Reason Dialog
        def open_deny_popup(student_obj, task_obj):
            reason_input = ft.TextField(
                label="Lý do từ chối",
                hint_text="Nhập lý do từ chối...",
                multiline=True,
                min_lines=3,
                max_lines=5,
                filled=True,
                autofocus=True
            )
            error_msg = ft.Text("", color=self.red, size=11)

            def close_deny_dlg(e):
                dialog.open = False
                self.page.update()

            def confirm_deny(e):
                reason_val = reason_input.value.strip() if reason_input.value else ""
                if not reason_val:
                    error_msg.value = "Vui lòng nhập lý do từ chối!"
                    self.page.update()
                    return

                # Remove from student's active pending tasks
                if isinstance(student_obj.get("tasks"), list) and task_obj in student_obj["tasks"]:
                    student_obj["tasks"].remove(task_obj)

                # Append to history
                history_entry = {
                    "student_id": student_obj.get("id", ""),
                    "student_name": student_obj.get("name", ""),
                    "class": student_obj.get("class", ""),
                    "job": task_obj.get("job", ""),
                    "time": task_obj.get("time", ""),
                    "note": task_obj.get("note", ""),
                    "proof_image": task_obj.get("proof_image", ""),
                    "status": "incomplete",
                    "Reason": reason_val
                }

                if not hasattr(self, "history") or self.history is None:
                    self.history = []

                self.history.append(history_entry)
                self.save_data()

                # EXPORT TO SHEET #3 (INCOMPLETE / DENIED)
                self.export_labor_acceptance_to_excel(
                    student_name=student_obj.get("name", ""),
                    student_class=student_obj.get("class", ""),
                    job_title=task_obj.get("job", ""),
                    job_time=task_obj.get("time", ""),
                    status="Incomplete",
                    reason=reason_val
                )

                dialog.open = False
                self.page.update()

                self.show_message(f"Đã từ chối công việc của {student_obj.get('name', 'Học sinh')}.")
                self.show_admin_labor_results()

            dialog = ft.AlertDialog(
                title=ft.Text("Từ chối báo cáo", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                content=ft.Container(
                    width=320,
                    content=ft.Column(
                        tight=True,  # Correct Flet parameter for min sizing
                        spacing=8,
                        controls=[
                            ft.Text(f"Học sinh: {student_obj.get('name', 'N/A')}", size=11, color=self.gray),
                            reason_input,
                            error_msg
                        ]
                    )
                ),
                actions=[
                    ft.TextButton("Hủy", on_click=close_deny_dlg),
                    ft.ElevatedButton(
                        "Xác nhận",
                        bgcolor=self.red,
                        color="white",
                        on_click=confirm_deny
                    )
                ]
            )
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()

        task_cards = []

        if isinstance(self.students, list):
            for student in self.students:
                if isinstance(student, dict) and "tasks" in student and isinstance(student["tasks"], list):
                    for task in student["tasks"]:
                        if isinstance(task, dict) and task.get("status") in ["pending_approval", "pending_approve"]:
                            proof_b64 = task.get("proof_image", "")

                            card = ft.Container(
                                padding=14,
                                bgcolor="#FFFFFF",
                                border=ft.border.all(1, "#E2E8F0"),
                                border_radius=12,
                                shadow=ft.BoxShadow(blur_radius=6, offset=ft.Offset(0, 2)),
                                content=ft.Column(
                                    spacing=10,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Column(
                                                    spacing=2,
                                                    controls=[
                                                        ft.Text(f"👤 {student.get('name', 'N/A')}", size=13,
                                                                weight=ft.FontWeight.BOLD, color=self.dark),
                                                        ft.Text(f"Lớp: {student.get('class', 'N/A')}", size=11,
                                                                color=self.gray)
                                                    ]
                                                ),
                                                ft.Container(
                                                    padding=ft.Padding(8, 4, 8, 4),
                                                    bgcolor="#FEF3C7",
                                                    border_radius=6,
                                                    content=ft.Text("Chờ nghiệm thu", size=10, color=self.orange,
                                                                    weight=ft.FontWeight.BOLD)
                                                )
                                            ]
                                        ),

                                        ft.Divider(height=1, color="#F1F5F9"),

                                        ft.Column(
                                            spacing=2,
                                            controls=[
                                                ft.Text(f"📌 Công việc: {task.get('job', 'N/A')}", size=11,
                                                        weight=ft.FontWeight.BOLD, color=self.dark),
                                                ft.Text(f"⏱ Thời gian: {task.get('time', 'N/A')}", size=11,
                                                        color=self.gray),
                                                ft.Text(f"📝 Ghi chú: {task.get('note', 'Không có')}", size=11,
                                                        color=self.gray)
                                            ]
                                        ),

                                        ft.Container(
                                            content=ft.Image(
                                                src_base64=proof_b64.split(",")[-1] if "," in proof_b64 else proof_b64,
                                                width=330,
                                                height=200,
                                                fit=ft.ImageFit.CONTAIN
                                            ) if proof_b64 else ft.Text("Chưa có ảnh minh chứng", size=11,
                                                                        color=self.gray),
                                            on_click=lambda e, img=proof_b64: open_zoomable_image_popup(img),
                                            tooltip="Chạm để phóng to ảnh"
                                        ),

                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.END,
                                            spacing=8,
                                            controls=[
                                                ft.Container(
                                                    on_click=lambda e, s=student, t=task: open_deny_popup(s, t),
                                                    padding=ft.Padding(12, 6, 12, 6),
                                                    bgcolor="#FEE2E2",
                                                    border_radius=6,
                                                    content=ft.Text("Từ chối", size=11, color=self.red,
                                                                    weight=ft.FontWeight.BOLD)
                                                ),
                                                ft.Container(
                                                    on_click=lambda e, s=student, t=task: approve_task(s, t),
                                                    padding=ft.Padding(14, 6, 14, 6),
                                                    bgcolor=self.green,
                                                    border_radius=6,
                                                    content=ft.Text("Duyệt", size=11, color="white",
                                                                    weight=ft.FontWeight.BOLD)
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                            task_cards.append(card)

        if not task_cards:
            task_cards.append(
                ft.Container(
                    padding=30,
                    alignment=ft.alignment.center,
                    content=ft.Text("Hiện không có báo cáo nào cần nghiệm thu.", size=12, color=self.gray,
                                    text_align=ft.TextAlign.CENTER)
                )
            )

        list_content = ft.Column(
            spacing=12,
            controls=task_cards
        )

        body = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                top_bar,
                ft.Container(height=4),
                list_content
            ]
        )

        card_container = ft.Container(
            content=body,
            width=380,
            padding=20,
            bgcolor=self.white,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
        )

        self.root.content = card_container
        self.page.update()




    # =========================
    # HỌC SINH: PHẦN VIỆC HOÀN THÀNH
    # =========================
    def show_student_completed_tasks(self):
        self.load_data()
        self.check_data()

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text("PHẦN VIỆC HOÀN THÀNH", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Lịch sử rèn luyện & nghiệm thu", size=11, color=self.gray)
                    ]
                ),
                ft.Container(
                    on_click=lambda e: self.show_student_home(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",
                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        completed_cards = []

        # Load history records from history.json
        all_history = self.load_history()

        # Filter for the currently logged-in student
        current_id = self.current_user.get("id") if isinstance(self.current_user, dict) else None
        student_history = [
            h for h in all_history
            if isinstance(h, dict) and h.get("student_id") == current_id
        ]

        for task in student_history:
            status = str(task.get("status", "")).strip()
            is_done = status in ["completed", "hoàn thành", "Đã hoàn thành"]

            card_color = "#F0FDF4" if is_done else "#FEF2F2"
            border_color = "#BBF7D0" if is_done else "#FECACA"
            badge_bg = "#DCFCE7" if is_done else "#FEE2E2"
            badge_color = self.green if is_done else self.red
            badge_text = "✅ Hoàn thành" if is_done else "❌ Chưa đạt"

            card = ft.Container(
                padding=12,
                bgcolor=card_color,
                border=ft.Border(
                    top=ft.BorderSide(1, border_color),
                    bottom=ft.BorderSide(1, border_color),
                    left=ft.BorderSide(1, border_color),
                    right=ft.BorderSide(1, border_color),
                ),
                border_radius=12,
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"📌 {task.get('job', '')}", size=12, weight=ft.FontWeight.BOLD, color=self.dark),
                                ft.Container(
                                    padding=ft.Padding(6, 2, 6, 2),
                                    bgcolor=badge_bg,
                                    border_radius=6,
                                    content=ft.Text(badge_text, size=10, color=badge_color, weight=ft.FontWeight.BOLD)
                                )
                            ]
                        ),
                        ft.Text(f"⏱️ Thời gian: {task.get('time', '')}", size=11, color=self.gray),
                        ft.Text(f"📝 Ghi chú: {task.get('note', 'Không có')}", size=11, color=self.gray),
                    ]
                )
            )
            completed_cards.append(card)

        if not completed_cards:
            completed_cards.append(
                ft.Container(
                    padding=30,
                    alignment=ft.alignment.Alignment(0, 0),
                    content=ft.Text(
                        "Chưa có lịch sử phần việc hoàn thành.",
                        size=12,
                        color=self.gray,
                        text_align=ft.TextAlign.CENTER
                    )
                )
            )

        list_content = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=completed_cards
        )

        body = ft.Column(
            spacing=12,
            controls=[
                top_bar,
                ft.Container(content=list_content, height=350)
            ]
        )

        card_container = ft.Container(
            content=body,
            width=380,
            padding=20,
            bgcolor=self.white,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
        )

        self.root.content = card_container
        self.page.update()

#=======CAUTION======CAUTION=======CAUTION======CAUTION=======CAUTION======CAUTION=======CAUTION======CAUTION=======

#FIRST HALF OF THE FILE (test.txt), THE OTHER HALF STARTS IN def show_admin_classes block (test_backup.txt)

#=======CAUTION======CAUTION=======CAUTION======CAUTION=======CAUTION======CAUTION=======CAUTION======CAUTION=======

        # =========================
        # TRANG XEM LỚP HỌC (MAIN CLASS PAGE)
        # =========================

    def show_admin_classes(self):
        """Displays grid of classes with toggleable details, independent scrolling list, and action buttons"""
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

        # 1. Group students by normalized class name
        default_classes = [f"A{i}" for i in range(1, 11)]
        students_by_class = {c: [] for c in default_classes}

        for student in self.students:
            if not isinstance(student, dict):
                continue

            raw_class = str(student.get("class", "")).strip().upper()
            if not raw_class:
                raw_class = "KHÁC"

            if raw_class not in students_by_class:
                students_by_class[raw_class] = []

            students_by_class[raw_class].append(student)

        # Container for the detail view
        detail_container_box = ft.Container(visible=False)
        selected_class_state = {"current": None}

        def view_class_students(class_name):
            # TOGGLE OFF: If clicking the currently active class while box is visible
            if selected_class_state["current"] == class_name and detail_container_box.visible:
                detail_container_box.visible = False
                detail_container_box.content = None
                selected_class_state["current"] = None
                self.page.update()
                return

            # TOGGLE ON / SWITCH CLASS
            selected_class_state["current"] = class_name
            student_list = students_by_class.get(class_name, [])

            # Header without the student count indicator
            header = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(f"Lớp {class_name}", size=13, weight=ft.FontWeight.BOLD, color=self.dark),
                    ft.Text(f"Tổng điểm: {sum(st.get('score', 0) for st in student_list)}", size=11, color=self.blue,
                            weight=ft.FontWeight.BOLD)
                ]
            )

            # Scrollable student list container
            student_items = []
            if not student_list:
                student_items.append(
                    ft.Container(
                        padding=15,
                        alignment=ft.alignment.center,
                        content=ft.Text("Chưa có học sinh trong lớp này.", size=11, color=self.gray)
                    )
                )
            else:
                for st in student_list:
                    student_items.append(
                        ft.Container(
                            padding=10,
                            bgcolor="#FFFFFF",
                            border_radius=8,
                            border=ft.border.all(1, "#E2E8F0"),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(st.get("name", "N/A"), size=12, weight=ft.FontWeight.BOLD,
                                                    color=self.dark),
                                            ft.Text(f"Mã: {st.get('id', 'N/A')}", size=10, color=self.gray)
                                        ]
                                    ),
                                    ft.Container(
                                        padding=ft.Padding(8, 4, 8, 4),
                                        bgcolor="#F0FDF4",
                                        border_radius=6,
                                        content=ft.Text(f"{st.get('score', 0)} điểm", size=11, color=self.green,
                                                        weight=ft.FontWeight.BOLD)
                                    )
                                ]
                            )
                        )
                    )

            # Scrollable view with fixed height
            list_scroll_view = ft.Container(
                content=ft.Column(
                    controls=student_items,
                    spacing=6,
                    scroll=ft.ScrollMode.AUTO
                ),
                height=180
            )

            detail_container_box.content = ft.Column(
                spacing=8,
                controls=[
                    header,
                    ft.Divider(height=4, color="#E2E8F0"),
                    list_scroll_view
                ]
            )
            detail_container_box.padding = 12
            detail_container_box.bgcolor = "#F8FAFC"
            detail_container_box.border = ft.border.all(1, "#CBD5E1")
            detail_container_box.border_radius = 12
            detail_container_box.visible = True

            self.page.update()

        # 2. Build Grid Buttons
        grid_rows = []
        all_class_keys = sorted(students_by_class.keys(),
                                key=lambda x: (0, int(x[1:])) if x.startswith("A") and x[1:].isdigit() else (1, x))

        row_controls = []
        for i, c in enumerate(all_class_keys):
            count = len(students_by_class[c])
            btn = ft.Container(
                on_click=lambda e, cls=c: view_class_students(cls),
                padding=8,
                bgcolor="#F3E8FF",
                border_radius=10,
                border=ft.border.all(1, "#D8B4FE"),
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                    controls=[
                        ft.Text(c, weight=ft.FontWeight.BOLD, color="#7C3AED", size=13),
                        ft.Text(f"{count} HS", size=9, color=self.gray)
                    ]
                )
            )
            row_controls.append(btn)

            if len(row_controls) == 5 or i == len(all_class_keys) - 1:
                grid_rows.append(ft.Row(controls=row_controls, spacing=8))
                row_controls = []

        # 3. Action Buttons (Finding & Delete Student)
        action_buttons = ft.Row(
            controls=[
                ft.Container(
                    on_click=lambda e: self.show_student_list(show_search=True),
                    padding=ft.Padding(12, 10, 12, 10),
                    border_radius=10,
                    bgcolor=self.blue,
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Text("Tìm học sinh", size=12, color="white", weight=ft.FontWeight.BOLD)
                ),
                ft.Container(
                    on_click=lambda e: self.show_student_list(show_delete_form=True),
                    padding=ft.Padding(12, 10, 12, 10),
                    border_radius=10,
                    bgcolor=self.red,
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Text("Xoá tài khoản", size=12, color="white", weight=ft.FontWeight.BOLD)
                )
            ]
        )

        body = ft.Column(
            spacing=10,
            controls=[
                top_bar,
                ft.Container(height=4),
                ft.Column(controls=grid_rows, spacing=8),
                ft.Container(height=6),
                detail_container_box,
                ft.Container(height=6),
                action_buttons
            ]
        )

        self.root.content = self.card(body, 380)
        self.page.update()

        # =========================
        # DANH SÁCH HỌC SINH CHI TIẾT (INDIVIDUAL CLASS VIEW)
        # =========================
    def show_student_list(self, class_filter=None, show_delete_form=False, search_query=None,
                              show_search_form=False):
            self.load_data()
            self.check_data()

            display_title = f"LỚP {class_filter.upper()}" if class_filter else "DANH SÁCH HỌC SINH"
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

            # 1. FORM XOÁ TÀI KHOẢN
            if show_delete_form:
                name_input = ft.TextField(label="Họ tên học sinh", text_size=12, height=48)
                id_input = ft.TextField(label="Mã ID học sinh", text_size=12, height=48)
                class_dropdown = ft.Dropdown(
                    label="Lớp học",
                    text_size=12,
                    height=48,
                    options=[ft.dropdown.Option(f"A{i}") for i in range(1, 11)]
                )
                agree_checkbox = ft.Checkbox(label="Tôi đồng ý với quyết định này")
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
                        self.show_admin_classes()
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
                                    on_click=lambda e: self.show_admin_classes()
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

            # 2. FORM TÌM KIẾM HỌC SINH
            elif show_search_form:
                name_input = ft.TextField(label="Họ tên học sinh", text_size=12, height=48)
                error_msg = ft.Text("", color=self.red, size=11, weight=ft.FontWeight.BOLD)

                def process_search(e):
                    typed_name = name_input.value.strip() if name_input.value else ""
                    if not typed_name:
                        error_msg.value = "Lỗi: Vui lòng nhập tên học sinh!"
                        self.page.update()
                        return
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
                                    on_click=lambda e: self.show_admin_classes()
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

            # 3. KẾT QUẢ TÌM KIẾM
            elif search_query is not None:
                results_top_bar = ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(f"KẾT QUẢ: '{search_query}'", size=14, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Container(
                            on_click=lambda e: self.show_admin_classes(),
                            padding=ft.Padding(10, 6, 10, 6),
                            border_radius=8,
                            bgcolor="#E2E8F0",
                            content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                        )
                    ]
                )
                rows = []
                q_str = search_query.strip().lower()
                found_students = [
                    s for s in self.students
                    if s.get("role") == "student" and q_str in str(s.get("name", "")).strip().lower()
                ]

                if not found_students:
                    rows.append(
                        ft.Container(
                            padding=20,
                            alignment=ft.alignment.Alignment(0, 0),
                            content=ft.Text("Không có học sinh trùng khớp", size=12, color=self.gray)
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
                            height=280,
                        )
                    ]
                )
                self.root.content = self.card(results_content, 380)
                self.page.update()

            # 4. DANH SÁCH BÌNH THƯỜNG (NO BOTTOM BUTTONS)
            else:
                rows = []
                header = ft.Container(
                    bgcolor=self.blue,
                    padding=10,
                    border_radius=8,
                    content=ft.Row(
                        controls=[
                            ft.Text("Mã ID", color="white", width=90, size=12, weight=ft.FontWeight.BOLD),
                            ft.Text("Họ tên", color="white", expand=True, size=12, weight=ft.FontWeight.BOLD),
                            ft.Text("Lớp", color="white", width=50, size=12, weight=ft.FontWeight.BOLD)
                        ]
                    )
                )
                rows.append(header)

                for student in self.students:
                    if student.get("role") != "student":
                        continue
                    if class_filter and str(class_filter).strip().lower() != str(
                            student.get("class", "")).strip().lower():
                        continue

                    rows.append(
                        ft.Container(
                            bgcolor="white",
                            padding=10,
                            border_radius=8,
                            content=ft.Row(
                                controls=[
                                    ft.Text(student.get("id", ""), width=90, size=12, color=self.dark),
                                    ft.Text(student.get("name", ""), expand=True, size=12, max_lines=1,
                                            color=self.dark),
                                    ft.Text(student.get("class", ""), width=50, size=12, color=self.dark)
                                ]
                            )
                        )
                    )

                table_content = ft.Column(
                    spacing=10,
                    controls=[
                        top_bar,
                        ft.Container(
                            content=ft.Column(controls=rows, scroll=ft.ScrollMode.AUTO, spacing=6),
                            height=280,
                        )
                    ]
                )
                self.root.content = self.card(table_content, 380)
                self.page.update()


            # ----------------------------------------------------
            # FORM XOÁ TÀI KHOẢN
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
                agree_checkbox = ft.Checkbox(label="Tôi đồng ý với quyết định này")
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
            # FORM TÌM KIẾM HỌC SINH
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
            # HIỂN THỊ KẾT QUẢ TÌM KIẾM
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
                found_students = [
                    s for s in self.students
                    if s.get("role") == "student" and q_str in str(s.get("name", "")).strip().lower()
                ]

                if not found_students:
                    rows.append(
                        ft.Container(
                            padding=20,
                            alignment=ft.alignment.Alignment(0, 0),
                            content=ft.Text("Không có học sinh trùng khớp", size=12, color=self.gray)
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
                                        ft.Text(f"Mã ID: {student.get('id', '')} | Điểm: {student.get('score', 0)}",
                                                size=11, color=self.gray)
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
            # DANH SÁCH BÌNH THƯỜNG DƯỚI DẠNG BẢNG
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
                    if class_filter and str(class_filter).strip().lower() != str(
                            student.get("class", "")).strip().lower():
                        continue

                    rows.append(
                        ft.Container(
                            bgcolor="white",
                            padding=10,
                            border_radius=8,
                            content=ft.Row(
                                controls=[
                                    ft.Text(student.get("id", ""), width=70, size=12, color=self.dark),
                                    ft.Text(student.get("name", ""), expand=True, size=12, max_lines=1,
                                            color=self.dark),
                                    ft.Text(student.get("class", ""), width=45, size=12, color=self.dark),
                                    ft.Text(str(student.get("score", 0)), width=35, size=12, color=self.dark)
                                ]
                            )
                        )
                    )

                table_content = ft.Column(
                    spacing=10,
                    controls=[
                        top_bar,
                        ft.Container(
                            content=ft.Column(controls=rows, scroll=ft.ScrollMode.AUTO, spacing=6),
                            height=280,
                        )
                    ]
                )
                self.root.content = self.card(table_content, 380)
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
        """Admin approves/rejects pending job registrations before they move to 'in_progress'."""
        self.load_data()
        self.check_data()

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text("DANH SÁCH ĐĂNG KÝ", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Duyệt học sinh đăng ký công việc", size=11, color=self.gray)
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

        def approve_registration(e, student, task):
            for t in student.get("tasks", []):
                if t.get("job") == task.get("job") and t.get("status") in ["pending_registration", "Chờ xét duyệt"]:
                    t["status"] = "in_progress"

                    # Push row directly to Sheet 1 in Google Sheets
                    self.export_task_to_google_sheets(
                        student_name=student.get("name", ""),
                        student_id=student.get("id", ""),
                        job_title=task.get("job", ""),
                        working_time=task.get("time", ""),
                        student_note=task.get("note", "")
                    )
                    break

            self.save_data()
            self.show_message(f"Đã duyệt đăng ký cho {student.get('name')}!")
            self.show_admin_registration_list()

        def deny_registration(student, task):
            """Deny registration: Removes task request from student's tasks"""
            if "tasks" in student and task in student["tasks"]:
                student["tasks"].remove(task)
            self.save_data()
            self.show_message(f"Đã từ chối đăng ký của {student.get('name')}!")
            self.show_admin_registration_list()

        pending_cards = []
        for student in self.students:
            if isinstance(student, dict) and "tasks" in student and isinstance(student["tasks"], list):
                for task in student["tasks"]:
                    if isinstance(task, dict) and task.get("status") in ["pending_registration", "Chờ xét duyệt"]:
                        card = ft.Container(
                            padding=12,
                            bgcolor="#F8FAFC",
                            border=ft.border.all(1, "#CBD5E1"),
                            border_radius=10,
                            content=ft.Column(
                                spacing=6,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(f"{student.get('name')} ({student.get('class')})", size=12, weight=ft.FontWeight.BOLD, color=self.dark),
                                            ft.Text(f"Mã HS: {student.get('id')}", size=10, color=self.gray)
                                        ]
                                    ),
                                    ft.Text(f"Công việc: {task.get('job')}", size=11, color=self.dark, weight=ft.FontWeight.W_500),
                                    ft.Text(f"Thời gian: {task.get('time')}", size=10, color=self.gray),
                                    ft.Container(height=4),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.END,
                                        spacing=6,
                                        controls=[
                                            ft.Container(
                                                on_click=lambda e, s=student, t=task: deny_registration(s, t),
                                                padding=ft.Padding(10, 6, 10, 6),
                                                bgcolor=self.red,
                                                border_radius=6,
                                                content=ft.Text("Từ chối", size=11, color="white", weight=ft.FontWeight.BOLD)
                                            ),
                                            ft.Container(
                                                on_click=lambda e, s=student, t=task: approve_registration(e, s, t),
                                                padding=ft.Padding(10, 6, 10, 6),
                                                bgcolor=self.blue,
                                                border_radius=6,
                                                content=ft.Text("Chấp nhận", size=11, color="white", weight=ft.FontWeight.BOLD)
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                        pending_cards.append(card)

        if not pending_cards:
            pending_cards.append(
                ft.Container(
                    padding=30,
                    alignment=ft.alignment.center,
                    content=ft.Text("Không có yêu cầu đăng ký nào cần duyệt.", size=12, color=self.gray, text_align=ft.TextAlign.CENTER)
                )
            )

        list_content = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=pending_cards
        )

        body = ft.Column(
            spacing=12,
            controls=[
                top_bar,
                ft.Container(content=list_content, height=350)
            ]
        )

        card_container = ft.Container(
            content=body,
            width=380,
            padding=20,
            bgcolor=self.white,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
        )

        self.root.content = card_container
        self.page.update()

    # =========================
    # ADMIN: TRANG NHẬP LÝ DO TỪ CHỐI
    # =========================

    def show_reject_reason_page(self, student, task):
        st_name = student.get("name", "N/A")
        st_id = student.get("id", "")
        job_title = task.get("job", "")

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("TỪ CHỐI ĐĂNG KÍ", size=15, weight=ft.FontWeight.BOLD, color=self.red),
                ft.Container(
                    on_click=lambda e: self.show_admin_registration_list(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",
                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        info_box = ft.Container(
            padding=10,
            bgcolor="#FEF2F2",
            border_radius=8,
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(f"👤 Học sinh: {st_name} ({st_id})", size=12, weight=ft.FontWeight.BOLD, color=self.dark),
                    ft.Text(f"📌 Phần việc: {job_title}", size=11, color=self.gray)
                ]
            )
        )

        reason_field = ft.TextField(
            label="Lý do từ chối",
            hint_text="Ghi rõ lý do từ chối",
            multiline=True,
            min_lines=3,
            max_lines=5,
            text_size=12,
            filled=True
        )

        error_text = ft.Text("", size=11, color=self.red, weight=ft.FontWeight.BOLD)

        def confirm_rejection(e):
            reason = reason_field.value.strip()
            if not reason:
                error_text.value = "Vui lòng nhập lý do từ chối trước khi xác nhận!"
                self.page.update()
                return

            task["status"] = "rejected_registration"
            task["reject_reason"] = reason
            self.save_data()

            self.show_message(f"Đã từ chối đơn của {st_name}.")
            self.show_admin_registration_list()

        btn_cancel = ft.ElevatedButton(
            "Hủy",
            bgcolor="#E2E8F0",
            color=self.dark,
            on_click=lambda e: self.show_admin_registration_list(),
            expand=True
        )

        btn_confirm_deny = ft.ElevatedButton(
            "Xác nhận từ chối",
            bgcolor=self.red,
            color="white",
            on_click=confirm_rejection,
            expand=True
        )

        body = ft.Column(
            spacing=12,
            controls=[
                top_bar,
                info_box,
                reason_field,
                error_text,
                ft.Row(controls=[btn_cancel, btn_confirm_deny], spacing=10)
            ]
        )

        card_container = ft.Container(
            content=body,
            width=380,
            padding=20,
            bgcolor=self.white,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
        )

        self.root.content = card_container
        self.page.update()

    # =========================
    # TRANG CHÍNH HỌC SINH
    # =========================
    def show_student_home(self):
        if not self.current_user:
            self.show_role_select()
            return

        user_name = self.current_user.get("name", "Học sinh")
        user_class = self.current_user.get("class", "")
        user_id = self.current_user.get("id", "")

        # Số lượng phần việc (thay thế bằng biến/hàm đếm thực tế nếu có)
        completed_count = getattr(self, "get_completed_count", lambda uid: 3)(user_id)
        denied_count = getattr(self, "get_denied_count", lambda uid: 1)(user_id)

        profile_card = ft.Container(
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
                                    fit="cover",
                                    width=46,
                                    height=46,
                                    border_radius=23,
                                )
                            ),
                            ft.Column(
                                spacing=1,
                                controls=[
                                    ft.Text(user_name, size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                                    ft.Text(f"Lớp {user_class} - ID: {user_id}", size=11, color=self.gray),
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
                height=120,
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
                feature_card("Phần việc đăng kí", "📝", self.blue, "#EFF6FF",
                             lambda e: self.show_job_registration()),
                feature_card("Tiến trình rèn luyện", "📈", self.orange, "#FFF7ED",
                             lambda e: self.show_student_progress()),
                feature_card("Phần việc hoàn thành", "✅", self.green, "#F0FDF4",
                             lambda e: self.show_student_completed_tasks()),
                feature_card("Lỗi vi phạm", "⚠️", self.red, "#FEF2F2",
                             lambda e: self.show_message("Chức năng Lỗi vi phạm")),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )

        # Khối thông tin bổ sung
        completed_info_box = ft.Container(
            width=340,
            padding=12,
            bgcolor="#F0FDF4",
            border_radius=12,
            border=ft.border.all(1, "#DCFCE7"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Text("✅", size=14),
                            ft.Text("Phần việc đã hoàn thành", size=13, weight=ft.FontWeight.W_600, color=self.dark)
                        ]
                    ),
                    ft.Text(f"{completed_count}", size=14, weight=ft.FontWeight.BOLD, color=self.green)
                ]
            )
        )

        denied_info_box = ft.Container(
            width=340,
            padding=12,
            bgcolor="#FEF2F2",
            border_radius=12,
            border=ft.border.all(1, "#FEE2E2"),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Text("❌", size=14),
                            ft.Text("Phần việc bị từ chối", size=13, weight=ft.FontWeight.W_600, color=self.dark)
                        ]
                    ),
                    ft.Text(f"{denied_count}", size=14, weight=ft.FontWeight.BOLD, color=self.red)
                ]
            )
        )

        body = ft.Column(
            controls=[
                self.title("TRANG HỌC SINH"),
                ft.Container(height=5),
                profile_card,
                ft.Container(height=15),
                ft.Row(
                    controls=[
                        ft.Text("Chức năng học sinh", size=13, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Cuộn ngang ➔", size=10, color=self.gray)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(height=5),
                sliding_board,
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.Text("THÔNG TIN KHÁC", size=13, weight=ft.FontWeight.BOLD, color=self.dark)
                    ]
                ),
                ft.Container(height=8),
                completed_info_box,
                ft.Container(height=8),
                denied_info_box,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.root.content = self.card(body, 380)
        self.page.update()

    #===============================
    # TRANG THÔNG TIN HỌC SINH
    #===============================
    def show_student_info(self):
        """Displays student details, completed tasks, and incomplete/active tasks."""
        self.load_data()
        self.check_data()

        if not self.current_user:
            self.show_role_select()
            return

        student_name = self.current_user.get("name", "N/A")
        student_id = self.current_user.get("id", "N/A")
        student_class = self.current_user.get("class", "N/A")

        # Fetch completed history entries for this student
        all_history = self.load_history()
        student_history = [
            h for h in all_history
            if isinstance(h, dict) and h.get("student_id") == student_id
        ]

        completed_jobs = [
            h.get("job", "Công việc không tên")
            for h in student_history
            if h.get("status") in ["complete", "completed", "hoàn thành", "Đã hoàn thành"]
        ]

        # Fetch incomplete/active tasks
        current_tasks = self.current_user.get("tasks", [])
        active_jobs = [
            t.get("job", "Công việc không tên")
            for t in current_tasks
            if isinstance(t, dict)
        ]
        rejected_jobs = [
            h.get("job", "Công việc không tên")
            for h in student_history
            if h.get("status") in ["incomplete", "rejected", "Chưa đạt"]
        ]
        incomplete_jobs = active_jobs + rejected_jobs

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("THÔNG TIN HỌC SINH", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                ft.Container(
                    on_click=lambda e: self.show_student_home(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",
                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        info_card = ft.Container(
            padding=14,
            bgcolor="#F8FAFC",
            border_radius=12,
            border=ft.border.all(1, "#E2E8F0"),
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(f"👤 Họ tên: {student_name}", size=13, weight=ft.FontWeight.BOLD, color=self.dark),
                    ft.Text(f"🆔 Mã HS: {student_id}", size=11, color=self.gray),
                    ft.Text(f"🏫 Lớp: {student_class}", size=11, color=self.gray),
                ]
            )
        )

        completed_items = [
                              ft.Container(
                                  padding=8,
                                  bgcolor="#F0FDF4",
                                  border_radius=8,
                                  content=ft.Text(f"✅ {job}", size=11, color=self.green, weight=ft.FontWeight.W_500)
                              )
                              for job in completed_jobs
                          ] or [ft.Text("Chưa có công việc nào hoàn thành.", size=11, color=self.gray)]

        incomplete_items = [
                               ft.Container(
                                   padding=8,
                                   bgcolor="#FEF2F2",
                                   border_radius=8,
                                   content=ft.Text(f"⏳ {job}", size=11, color=self.red, weight=ft.FontWeight.W_500)
                               )
                               for job in incomplete_jobs
                           ] or [ft.Text("Không có công việc chưa hoàn thành.", size=11, color=self.gray)]

        body = ft.Column(
            spacing=12,
            controls=[
                top_bar,
                info_card,
                ft.Text("Công việc đã hoàn thành", size=12, weight=ft.FontWeight.BOLD, color=self.green),
                ft.Column(controls=completed_items, spacing=6),
                ft.Text("Công việc chưa hoàn thành", size=12, weight=ft.FontWeight.BOLD, color=self.red),
                ft.Column(controls=incomplete_items, spacing=6),
            ]
        )

        card_container = ft.Container(
            content=ft.Column(controls=[body], scroll=ft.ScrollMode.AUTO, height=380),
            width=380,
            padding=16,
            bgcolor=self.white,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
        )

        self.root.content = card_container
        self.page.update()

    # =========================
    # BẢNG ĐĂNG KÍ PHẦN VIỆC (HỌC SINH)
    # =========================

    def show_job_registration(self):
        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("ĐĂNG KÍ PHẦN VIỆC", size=15, weight=ft.FontWeight.BOLD, color=self.dark)
                    ]
                ),
                ft.Container(
                    on_click=lambda e: self.show_student_home(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",
                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        subtitle = ft.Text(
            "Phần việc đăng kí sẽ được chuyển qua tiến trình rèn luyện sau khi duyệt.",
            size=11,
            color=self.gray
        )

        job_name_field = ft.TextField(
            label="Công việc (ghi kèm địa chỉ phần việc)",
            hint_text="Ví dụ: Dọn rác ở sân thể dục",
            filled=True,
            text_size=10,
        )

        job_time_field = ft.TextField(
            label="Thời gian",
            hint_text="Ví dụ: Thứ 2 17/8 đến thứ 4 19/8",
            filled=True,
            text_size=12,
        )

        job_note_field = ft.TextField(
            label="Ghi chú (nếu có)",
            hint_text="Ghi chú thêm...",
            filled=True,
            multiline=True,
            min_lines=2,
            max_lines=3,
            text_size=12,
        )

        status_text = ft.Text("", size=11, weight=ft.FontWeight.BOLD)

        def handle_cancel(e):
            self.show_student_home()

        def handle_register(e):
            if not job_name_field.value.strip() or not job_time_field.value.strip():
                status_text.value = "Vui lòng điền tên phần việc và thời gian!"
                status_text.color = self.red
                self.page.update()
                return

            if self.current_user:
                if "tasks" not in self.current_user or not isinstance(self.current_user["tasks"], list):
                    self.current_user["tasks"] = []

                # RULE: Check if student already has an ACTIVE (unfinished) task
                active_statuses = ["pending_registration", "in_progress", "pending_review", "Chờ xét duyệt",
                                   "Đang rèn luyện"]
                has_active_task = any(
                    isinstance(t, dict) and t.get("status") in active_statuses
                    for t in self.current_user["tasks"]
                )

                if has_active_task:
                    status_text.value = "Bạn đang có phần việc chưa hoàn thành!\nHãy hoàn thành công việc hiện tại trước."
                    status_text.color = self.red
                    self.page.update()
                    return

                # Create new application
                new_task = {
                    "job": job_name_field.value.strip(),
                    "time": job_time_field.value.strip(),
                    "note": job_note_field.value.strip(),
                    "status": "pending_registration"  # Status = Chờ xét duyệt
                }

                self.current_user["tasks"].append(new_task)

                # --- SYNC FIX START ---
                # Ensure the change in self.current_user is reflected in self.students before saving
                for s in self.students:
                    if isinstance(s, dict) and s.get("id") == self.current_user.get("id"):
                        s["tasks"] = self.current_user["tasks"]
                        break
                # --- SYNC FIX END ---

                self.save_data()

                status_text.value = "Đã gửi đăng kí thành công! Đang chờ Admin duyệt."
                status_text.color = self.green
                job_name_field.value = ""
                job_time_field.value = ""
                job_note_field.value = ""
                self.page.update()

        btn_cancel = ft.ElevatedButton(
            "Hủy",
            bgcolor="#E2E8F0",
            color=self.dark,
            on_click=handle_cancel,
            expand=True
        )

        btn_register = ft.ElevatedButton(
            "Đăng kí",
            bgcolor=self.blue,
            color="white",
            on_click=handle_register,
            expand=True
        )

        body = ft.Column(
            spacing=12,
            controls=[
                top_bar,
                subtitle,
                job_name_field,
                job_time_field,
                job_note_field,
                ft.Row(controls=[btn_cancel, btn_register], spacing=10),
                ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER)
            ]
        )

        card_container = ft.Container(
            content=body,
            width=380,
            padding=25,
            bgcolor=self.white,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
        )

        self.root.content = card_container
        self.page.update()
        # =========================
    # MÀN HÌNH TIẾN TRÌNH HỌC SINH
    # =========================
    def show_student_progress(self):
        """Displays ongoing tasks assigned to current student with fixed FilePicker and original card layout"""
        self.load_data()
        self.check_data()

        if not self.current_user:
            self.show_login()
            return

        top_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text("TIẾN TRÌNH RÈN LUYỆN", size=15, weight=ft.FontWeight.BOLD, color=self.dark),
                        ft.Text("Nhiệm vụ đang thực hiện", size=11, color=self.gray)
                    ]
                ),
                ft.Container(
                    on_click=lambda e: self.show_student_home(),
                    padding=ft.Padding(10, 6, 10, 6),
                    border_radius=8,
                    bgcolor="#E2E8F0",
                    content=ft.Text("Quay lại", size=11, color=self.dark, weight=ft.FontWeight.BOLD)
                )
            ]
        )

        instruction_text = ft.Text(
            "Phần việc đã đăng kí sẽ được gửi về đây, chụp ảnh ở nơi phần việc để gửi báo cáo.",
            size=11,
            color=self.gray,
            italic=True
        )

        current_student = None
        for s in self.students:
            if isinstance(s, dict) and s.get("id") == self.current_user.get("id"):
                current_student = s
                break

        task_cards = []

        def submit_report(task_obj, b64_img):
            if not b64_img:
                self.show_message("Vui lòng chọn hoặc chụp ảnh minh chứng trước khi gửi!")
                return

            task_obj["proof_image"] = b64_img
            task_obj["status"] = "pending_approval"
            self.save_data()
            self.show_message("Đã gửi báo cáo minh chứng thành công! Chờ Admin nghiệm thu.")
            self.show_student_progress()

        def open_zoomable_image_popup(b64_data):
            """Opens a popup modal with zoom controls and smooth drag-to-pan functionality."""
            if not b64_data:
                return

            clean_b64 = b64_data.split(",")[-1] if "," in b64_data else b64_data

            state = {
                "scale": 1.0,
                "x": 0.0,
                "y": 0.0
            }

            image_ctrl = ft.Image(
                src_base64=clean_b64,
                fit=ft.ImageFit.CONTAIN,
                width=320,
                height=320,
                scale=1.0,
                offset=ft.Offset(0, 0)
            )

            image_container = ft.Container(
                content=image_ctrl,
                alignment=ft.alignment.center,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                width=320,
                height=320
            )

            def update_transform():
                image_ctrl.scale = state["scale"]
                image_ctrl.offset = ft.Offset(state["x"], state["y"])
                zoom_text.value = f"{int(state['scale'] * 100)}%"
                self.page.update()

            def zoom_in(e):
                if state["scale"] < 5.0:
                    state["scale"] += 0.25
                    update_transform()

            def zoom_out(e):
                if state["scale"] > 0.5:
                    state["scale"] -= 0.25
                    if state["scale"] <= 1.0:
                        state["x"] = 0.0
                        state["y"] = 0.0
                    update_transform()

            def reset_zoom(e):
                state["scale"] = 1.0
                state["x"] = 0.0
                state["y"] = 0.0
                update_transform()

            def on_scroll(e: ft.ScrollEvent):
                if e.scroll_delta_y < 0:
                    zoom_in(None)
                else:
                    zoom_out(None)

            def on_pan_update(e: ft.DragUpdateEvent):
                state["x"] += e.delta_x / 200.0
                state["y"] += e.delta_y / 200.0
                update_transform()

            def close_dlg(e):
                dialog.open = False
                self.page.update()

            zoom_text = ft.Text("100%", size=11, weight=ft.FontWeight.BOLD, color=self.gray)

            gesture_wrapper = ft.GestureDetector(
                content=image_container,
                on_scroll=on_scroll,
                on_pan_update=on_pan_update,
                drag_interval=10
            )

            dialog = ft.AlertDialog(
                content_padding=10,
                content=ft.Container(
                    width=340,
                    height=420,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            gesture_wrapper,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=6,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.REMOVE_CIRCLE_OUTLINED,
                                        icon_size=20,
                                        tooltip="Thu nhỏ",
                                        on_click=zoom_out
                                    ),
                                    zoom_text,
                                    ft.IconButton(
                                        icon=ft.icons.ADD_CIRCLE_OUTLINED,
                                        icon_size=20,
                                        tooltip="Phóng to",
                                        on_click=zoom_in
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.REFRESH_OUTLINED,
                                        icon_size=18,
                                        tooltip="Đặt lại",
                                        on_click=reset_zoom
                                    ),
                                    ft.Container(width=10),
                                    ft.TextButton("Đóng", on_click=close_dlg)
                                ]
                            )
                        ]
                    )
                )
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

        if current_student and "tasks" in current_student and isinstance(current_student["tasks"], list):
            for task in current_student["tasks"]:
                if isinstance(task, dict):
                    status = task.get("status", "in_progress")

                    # Include tasks with status: in_progress, pending_registration, pending_approval
                    if status in ["in_progress", "pending_registration", "pending_approval", "pending_approve"]:

                        # Determine status text and block actions when pending
                        if status == "pending_registration":
                            status_text = "Đang phê duyệt"
                            status_color = self.orange
                            status_bg = "#FEF3C7"
                            is_blocked = True
                        elif status in ["pending_approval", "pending_approve"]:
                            status_text = "Đã gửi báo cáo! Đang chờ xác nhận..."
                            status_color = self.orange
                            status_bg = "#FEF3C7"
                            is_blocked = True
                        else:  # in_progress
                            status_text = "Đang thực hiện"
                            status_color = self.blue
                            status_bg = "#EFF6FF"
                            is_blocked = False

                        # Target image container for explicit updating
                        active_b64 = task.get("proof_image", "")

                        preview_img = ft.Image(
                            src_base64=active_b64 if active_b64 else None,
                            width=330,
                            height=220,
                            fit=ft.ImageFit.CONTAIN,
                            visible=bool(active_b64)
                        )

                        # Wrap preview in a clickable container to open zoom popup
                        preview_container = ft.Container(
                            content=preview_img,
                            on_click=lambda e, t=task: open_zoomable_image_popup(t.get("proof_image", "")),
                            tooltip="Chạm để phóng to ảnh"
                        )

                        placeholder_box = ft.Container(
                            width=330,
                            height=120,
                            bgcolor="#F8FAFC",
                            border_radius=8,
                            border=ft.border.all(1, "#E2E8F0"),
                            alignment=ft.alignment.center,
                            visible=not bool(active_b64),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=4,
                                controls=[
                                    ft.Text("📷", size=26),
                                    ft.Text("Chưa có ảnh minh chứng", size=10, color=self.gray)
                                ]
                            )
                        )

                        # Dynamic FilePicker Handler tied to this specific task item
                        def create_picker_and_bind(t=task, img_ctrl=preview_img, box_ctrl=placeholder_box):

                            def _process_and_update(raw_bytes):
                                with Image.open(io.BytesIO(raw_bytes)) as img:
                                    img.thumbnail((800, 800))
                                    buffer = io.BytesIO()
                                    img.save(buffer, format="JPEG", quality=70)
                                    b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

                                    # Update state & UI controls
                                    t["proof_image"] = b64_str
                                    img_ctrl.src_base64 = b64_str
                                    img_ctrl.visible = True
                                    box_ctrl.visible = False
                                    self.page.update()

                            def on_file_picked(e: ft.FilePickerResultEvent):
                                if not e.files or len(e.files) == 0:
                                    return

                                selected_file = e.files[0]

                                if selected_file.path and os.path.exists(selected_file.path):
                                    with open(selected_file.path, "rb") as f:
                                        raw_bytes = f.read()
                                    _process_and_update(raw_bytes)
                                else:
                                    upload_url = self.page.get_upload_url(selected_file.name, 600)
                                    picker.upload([
                                        ft.FilePickerUploadFile(selected_file.name, upload_url=upload_url)
                                    ])

                            def on_upload_complete(e: ft.FilePickerUploadEvent):
                                if e.progress == 1.0:
                                    uploaded_path = os.path.join("uploads", e.file_name)
                                    with open(uploaded_path, "rb") as f:
                                        raw_bytes = f.read()
                                    _process_and_update(raw_bytes)

                            picker = ft.FilePicker(on_result=on_file_picked, on_upload=on_upload_complete)
                            self.page.overlay.append(picker)
                            return picker

                        fp = create_picker_and_bind()

                        # ORIGINAL Task Card Layout (Preserved without layout modifications)
                        card = ft.Container(
                            padding=14,
                            bgcolor="#FFFFFF",
                            border=ft.border.all(1, "#E2E8F0"),
                            border_radius=12,
                            shadow=ft.BoxShadow(blur_radius=6, offset=ft.Offset(0, 2)),
                            content=ft.Column(
                                spacing=10,
                                controls=[
                                    # Top Row: Job Title & Status
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(f"{task.get('job', 'N/A')}", size=13, weight=ft.FontWeight.BOLD,
                                                    color=self.dark),
                                            ft.Container(
                                                padding=ft.Padding(8, 4, 8, 4),
                                                bgcolor=status_bg,
                                                border_radius=6,
                                                content=ft.Text(status_text, size=10, color=status_color,
                                                                weight=ft.FontWeight.BOLD)
                                            )
                                        ]
                                    ),
                                    # Task Details
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(f"⏱ Thời gian: {task.get('time', 'N/A')}", size=11, color=self.gray),
                                            ft.Text(f"📝 Ghi chú: {task.get('note', 'Không có')}", size=11, color=self.dark)
                                        ]
                                    ),

                                    ft.Divider(height=1, color="#F1F5F9"),

                                    # Image Preview Box & Buttons
                                    ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=8,
                                        controls=[
                                            placeholder_box,
                                            preview_container,
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                spacing=8,
                                                controls=[
                                                    ft.Container(
                                                        on_click=None if is_blocked else (lambda e, picker=fp: picker.pick_files(
                                                            allow_multiple=False,
                                                            allowed_extensions=["png", "jpg", "jpeg"]
                                                        )),
                                                        padding=ft.Padding(12, 6, 12, 6),
                                                        bgcolor="#E2E8F0" if is_blocked else "#E0F2FE",
                                                        border_radius=6,
                                                        content=ft.Row(
                                                            spacing=4,
                                                            controls=[
                                                                ft.Text("📁", size=11),
                                                                ft.Text("Chọn ảnh", size=11, color=self.gray if is_blocked else self.blue,
                                                                        weight=ft.FontWeight.BOLD)
                                                            ]
                                                        )
                                                    ),
                                                    ft.Container(
                                                        on_click=None if is_blocked else (lambda e, t=task: submit_report(t,
                                                                                                 t.get("proof_image", ""))),
                                                        padding=ft.Padding(14, 6, 14, 6),
                                                        bgcolor=self.gray if is_blocked else self.green,
                                                        border_radius=6,
                                                        content=ft.Text("Gửi báo cáo", size=11, color="white",
                                                                        weight=ft.FontWeight.BOLD)
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                        task_cards.append(card)

        if not task_cards:
            task_cards.append(
                ft.Container(
                    padding=30,
                    alignment=ft.alignment.center,
                    content=ft.Text("Bạn chưa có công việc nào đang thực hiện.", size=12, color=self.gray,
                                    text_align=ft.TextAlign.CENTER)
                )
            )

        list_content = ft.Column(
            spacing=12,
            controls=task_cards
        )

        body = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                top_bar,
                instruction_text,
                ft.Container(height=4),
                list_content
            ]
        )

        card_container = ft.Container(
            content=body,
            width=380,
            padding=20,
            bgcolor=self.white,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15, offset=ft.Offset(0, 5))
        )

        self.root.content = card_container
        self.page.update()

    show_student_process = show_student_progress

    # =========================================================
    # EXPORT DATA TO SHEET #1 (ĐĂNG KÝ PHẦN VIỆC)
    # =========================================================
    def export_task_to_google_sheets(self, student_name, student_id, job_title, working_time, student_note):
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
            client = gspread.authorize(creds)

            sheet_key = "1Rw16Tjror8b5b0XSdc1l6wvZbpic71Bt_OwDZbojb1I"
            sheet = client.open_by_key(sheet_key).sheet1

            # 1. Get all existing values from column B (Name column)
            col_b_values = sheet.col_values(2)

            # 2. Find the first empty row inside your table (starting after header row 5)
            next_row = len(col_b_values) + 1
            if next_row < 6:
                next_row = 6  # Start filling at Row 6

            # 3. Write directly into columns B to F for that specific row
            # Column mapping: B=Tên, C=ID, D=Công Việc, E=Thời Gian, F=Ghi Chú
            cell_range = f"B{next_row}:F{next_row}"
            new_data = [[student_name, student_id, job_title, working_time, student_note]]

            sheet.update(range_name=cell_range, values=new_data)

            print(f"Data successfully written to row {next_row}!")

        except Exception as err:
            import traceback
            traceback.print_exc()

    # =========================================================
    # EXPORT DATA TO SHEET #3 (NGHIỆM THU LAO ĐỘNG)
    # =========================================================
    def export_labor_acceptance_to_excel(self, student_name, student_class, job_title, job_time, status, reason=""):
        """
        Exports task data into Sheet #3 (Sheet3) starting after row 5.
        - Preserves pre-existing headers, titles, and legends in 'TrAnG bang tinh du lieu hoc sinh.xlsx'.
        - Updates Google Sheets (live) and saves to local Excel file.
        """
        is_approved = str(status).strip().lower() in ["complete", "completed", "hoàn thành"]
        reason_text = "" if is_approved else reason

        # ---------------------------------------------------------
        # OPTION A: Google Sheets Integration
        # ---------------------------------------------------------
        max_retries = 3
        for attempt in range(max_retries):
            try:
                scopes = [
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
                gc = gspread.authorize(creds)

                spreadsheet_key = "1Rw16Tjror8b5b0XSdc1l6wvZbpic71Bt_OwDZbojb1I"
                sh = gc.open_by_key(spreadsheet_key)
                worksheet3 = sh.get_worksheet(2)  # Sheet #3

                col_b = worksheet3.col_values(2)

                # Find the true last row after header (Row 5)
                last_valid_row = 5
                for idx, val in enumerate(col_b, start=1):
                    if idx >= 6 and val and str(val).strip() and not str(val).startswith("Column"):
                        last_valid_row = idx

                next_row = last_valid_row + 1

                row_data = [
                    student_name,  # Col B: Tên
                    student_class,  # Col C: Lớp
                    job_title,  # Col D: Công việc
                    job_time,  # Col E: Thời gian
                    reason_text  # Col F: Lý do
                ]

                cell_range = f"B{next_row}:F{next_row}"
                worksheet3.update(range_name=cell_range, values=[row_data])

                # Apply fill color on Column G
                status_cell = f"G{next_row}"
                bg_color = (
                    {"red": 0.13, "green": 0.50, "blue": 0.22} if is_approved
                    else {"red": 0.85, "green": 0.19, "blue": 0.15}
                )
                worksheet3.format(status_cell, {"backgroundColor": bg_color})

                print(f"Data successfully written to Google Sheet #3 at row {next_row}!")
                break

            except Exception as e:
                print(f"Google Sheet Export attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)

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