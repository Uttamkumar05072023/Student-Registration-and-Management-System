from customtkinter import *
from tkcalendar import Calendar
from tkinter import messagebox,filedialog,ttk
from PIL import Image,ImageDraw,ImageFont
import datetime,qrcode,os,shutil,pymysql,tempfile,pandas,webbrowser
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as ai
ai.configure(api_key=os.getenv("API_KEY"))
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

class System(CTk):
    def __init__(self):
        super().__init__()
        # ======================= main window =======================
        self.title("Student Registration & Management System")
        self.geometry("1280x755+0+0")
        self.resizable(False,False)

        # ======================= icon image =======================
        self.iconbitmap("images/icon.ico")

        self.tabview = CTkTabview(self,corner_radius=0,width=1280,height=755,state=DISABLED)
        self.tabview.add("Login Page")
        self.tabview.add("Student Registration")
        self.tabview.add("Admin Registration")
        self.tabview.add("Student Dashboard")
        self.tabview.add("Admin Dashboard")
        self.tabview.set("Login Page")
        self.tabview.pack()
        
        # ========================================================= LOGIN PAGE =========================================================
        # ======================= background image =========================
        CTkLabel(self.tabview.tab("Login Page"),image=CTkImage(dark_image=Image.open("images/bg.jpg"),light_image=Image.open("images/bg.jpg"),size=(1280,720)),text="").pack()

        # ======================= login frame ==========================
        CTkLabel(self.tabview.tab("Login Page"),image=CTkImage(dark_image=Image.open("images/icon.png"),light_image=Image.open("images/icon.png"),size=(128,128)),text="",bg_color="white").place(x=600,y=170)
        self.login_frame = CTkFrame(self.tabview.tab("Login Page"),height=400,width=500,border_color="#b0c404",border_width=3,bg_color="white",fg_color="#f1f7be",corner_radius=20)
        CTkLabel(self.login_frame,text="Welcome Back!",text_color="blue",font=CTkFont(family="times new roman",size=50,weight="bold")).place(x=80,y=20)
        
        # ====== Combobox ======
        CTkLabel(self.login_frame,image=CTkImage(dark_image=Image.open("images/login_type.png"),light_image=Image.open("images/login_type.png"),size=(32,32)),text="Login type",compound=LEFT,font=CTkFont(family="times new roman",size=30,weight="bold"),text_color="black").place(x=10,y=100)
        self.login_type = StringVar(value="Student")
        CTkComboBox(self.login_frame,variable=self.login_type,values=["Admin","Student"],font=CTkFont(family="times new roman",size=25),dropdown_font=CTkFont(family="times new roman",size=25),dropdown_fg_color="#f1f7be",dropdown_text_color="black",dropdown_hover_color="#b0c404",button_color="#b0c404",button_hover_color="#8e9e02",width=300,height=40,text_color="blue",border_color="#b0c404",fg_color="#f1f7be",corner_radius=10,state="readonly").place(x=180,y=100)

        # ====== Username Entry ======
        CTkLabel(self.login_frame,image=CTkImage(dark_image=Image.open("images/user_img.png"),light_image=Image.open("images/user_img.png"),size=(32,32)),text="Username",compound=LEFT,font=CTkFont(family="times new roman",size=30,weight="bold"),text_color="black").place(x=10,y=160)
        self.user_entry = CTkEntry(self.login_frame,placeholder_text="Enter your username",placeholder_text_color="#b0c404",font=CTkFont(family="times new roman",size=25),width=300,height=40,fg_color="transparent",text_color="blue",border_color="#b0c404",corner_radius=10)
        self.user_entry.place(x=180,y=160)
        self.user_entry.bind("<Enter>", lambda event: self.user_entry.configure(border_color="blue"))
        self.user_entry.bind("<Leave>", lambda event: self.user_entry.configure(border_color="#b0c404"))

        # ====== Password Entry =====
        CTkLabel(self.login_frame,image=CTkImage(dark_image=Image.open("images/pass_img.png"),light_image=Image.open("images/pass_img.png"),size=(32,32)),text="Password",compound=LEFT,font=CTkFont(family="times new roman",size=30,weight="bold"),text_color="black").place(x=10,y=220)
        self.pass_entry = CTkEntry(self.login_frame,placeholder_text="Enter your password",placeholder_text_color="#b0c404",font=CTkFont(family="times new roman",size=25),width=300,height=40,fg_color="transparent",text_color="blue",border_color="#b0c404",corner_radius=10,show="*")
        self.pass_entry.place(x=180,y=220)
        self.pass_entry.bind("<Enter>", lambda event: self.pass_entry.configure(border_color="blue"))
        self.pass_entry.bind("<Leave>", lambda event: self.pass_entry.configure(border_color="#b0c404"))

        # ===== Buttons =====
        self.register_btn = CTkButton(self.login_frame,text="Register",width=200,height=40,font=CTkFont(family="times new roman",size=25),fg_color="#1f7bd1",hover_color="#0d4cd4",text_color="white",corner_radius=10,state=DISABLED,command=lambda:self.tabview.set("Admin Registration") if self.login_type.get() == "Admin" else self.tabview.set("Student Registration"))
        self.register_btn.place(x=40,y=290)
        self.login_btn = CTkButton(self.login_frame,text="Login",width=200,height=40,font=CTkFont(family="times new roman",size=25),fg_color="#1f7bd1",hover_color="#0d4cd4",text_color="white",corner_radius=10,state=DISABLED,command=self.login)
        self.login_btn.place(x=260,y=290)
        self.forgot_password = CTkButton(self.login_frame,text="Forgot password?",font=CTkFont(family="times new roman",size=25),fg_color="transparent",text_color="red",hover_color="#f1f7be",state=DISABLED,command=self.forgot_password_email)
        self.forgot_password.place(x=150,y=340)
        self.forgot_password.bind("<Enter>", lambda event: self.forgot_password.configure(text_color="blue"))
        self.forgot_password.bind("<Leave>", lambda event: self.forgot_password.configure(text_color="red"))
        self.db_btn = CTkButton(self.tabview.tab("Login Page"),image=CTkImage(light_image=Image.open("images/db_absent.png"),dark_image=Image.open("images/db_absent.png"),size=(42,42)),text="",width=0,height=0,fg_color="white",hover=False,command=self.connect_to_db_window)
        self.db_btn.place(x=630,y=670)
        
        self.login_frame.place(x=400,y=270)

        # ======================================================= Student Registration Form ========================================================
        # ======================= Label & Date time =========================
        self.tabview.tab("Student Registration").configure(fg_color="light blue")
        CTkLabel(self.tabview.tab("Student Registration"),text="STUDENT  REGISTRATION  FORM",text_color="black",font=CTkFont(family="times new roman",size=50,weight="bold"),bg_color="light blue").pack()
        self.date_time = CTkLabel(self.tabview.tab("Student Registration"),text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),bg_color="light blue")
        self.date_time.place(x=1180,y=0)
        self.date_time_update()
        CTkButton(self.tabview.tab("Student Registration"),image=CTkImage(light_image=Image.open("images/back.png"),dark_image=Image.open("images/back.png"),size=(40,40)),text="",width=0,bg_color="light blue",corner_radius=20,command=lambda:self.tabview.set("Login Page")).place(x=10,y=10)

        # ======================= student registration frame =========================
        self.student_registration_frame = CTkFrame(self.tabview.tab("Student Registration"),height=600,width=1120,border_color="deep sky blue",border_width=3,bg_color="light blue",fg_color="white",corner_radius=20)

        # === Image section ====
        self.image_frame = CTkFrame(self.student_registration_frame,height=580,width=270,border_color="deep sky blue",border_width=3,bg_color="white",fg_color="white",corner_radius=20)
        self.photo_frame = CTkFrame(self.image_frame,height=250,width=190,border_color="black",border_width=3,bg_color="white",fg_color="black",corner_radius=10)
        self.student_image = CTkImage(light_image=Image.open("images/upload image.png"),dark_image=Image.open("images/upload image.png"),size=(180,240))
        self.photo_frame_img = CTkLabel(self.photo_frame,text="",image=self.student_image,width=180,height=240)
        self.photo_frame_img.place(x=5,y=5)
        self.photo_frame.place(x=40,y=40)
        CTkButton(self.image_frame,text="upload image",width=190,height=40,fg_color="#1f7bd1",hover_color="deep sky blue",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),command=self.upload_image).place(x=40,y=350)
        self.image_frame.place(x=10,y=10)

        # === Student Details section ===
        self.student_details_section = CTkFrame(self.student_registration_frame,height=580,width=400,border_color="deep sky blue",border_width=3,bg_color="white",fg_color="white",corner_radius=20)
        CTkLabel(self.student_details_section,text="Student Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=100,y=25)

        CTkLabel(self.student_details_section,text="Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=100)
        self.name_entry = CTkEntry(self.student_details_section,placeholder_text="Enter your name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.name_entry.place(x=130,y=95)
        self.name_entry.bind("<Enter>",lambda event:self.name_entry.configure(border_color="deep sky blue"))
        self.name_entry.bind("<Leave>",lambda event:self.name_entry.configure(border_color="black"))

        CTkLabel(self.student_details_section,text="D.O.B*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=150)
        self.dob_entry = CTkEntry(self.student_details_section,placeholder_text="DD/MM/YYYY",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10,state="readonly")
        self.dob_entry.place(x=130,y=145)
        CTkButton(self.student_details_section,text="get",height=40,width=10,fg_color="#1f7bd1",hover_color="deep sky blue",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),border_color="black",border_width=2,command=self.getDate).place(x=340,y=145)
        self.dob_entry.bind("<Enter>",lambda event:self.dob_entry.configure(border_color="deep sky blue"))
        self.dob_entry.bind("<Leave>",lambda event:self.dob_entry.configure(border_color="black"))

        CTkLabel(self.student_details_section,text="Gender*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=200)
        self.gender_entry = StringVar(value = "")
        CTkRadioButton(self.student_details_section,variable=self.gender_entry,text="Male",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Male").place(x=130,y=195)
        CTkRadioButton(self.student_details_section,variable=self.gender_entry,text="Female",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Female").place(x=230,y=195)
        
        CTkLabel(self.student_details_section,text="Class*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=250)
        self.class_entry = CTkComboBox(self.student_details_section,values=["Select Class","B.Tech - I","B.Tech - II","B.Tech - III","B.Tech - IV","M.Tech - I","M.Tech - II"],font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10,state="readonly")
        self.class_entry.place(x=130,y=245)
        self.class_entry.set("Select Class")
        self.class_entry.bind("<Enter>",lambda event:self.class_entry.configure(border_color="deep sky blue"))
        self.class_entry.bind("<Leave>",lambda event:self.class_entry.configure(border_color="black"))

        CTkLabel(self.student_details_section,text="Field*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=300)
        self.field_entry = CTkEntry(self.student_details_section,placeholder_text="Enter your field",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.field_entry.place(x=130,y=295)
        self.field_entry.bind("<Enter>",lambda event:self.field_entry.configure(border_color="deep sky blue"))
        self.field_entry.bind("<Leave>",lambda event:self.field_entry.configure(border_color="black"))

        CTkLabel(self.student_details_section,text="Roll no.*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=350)
        self.roll_no_entry = CTkEntry(self.student_details_section,placeholder_text="Enter your Roll no",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.roll_no_entry.place(x=130,y=345)
        self.roll_no_entry.bind("<Enter>",lambda event:self.roll_no_entry.configure(border_color="deep sky blue"))
        self.roll_no_entry.bind("<Leave>",lambda event:self.roll_no_entry.configure(border_color="black"))

        CTkLabel(self.student_details_section,text="Email*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=400)
        self.email_entry = CTkEntry(self.student_details_section,placeholder_text="Enter your email",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.email_entry.place(x=130,y=395)
        self.email_entry.bind("<Enter>",lambda event:self.email_entry.configure(border_color="deep sky blue"))
        self.email_entry.bind("<Leave>",lambda event:self.email_entry.configure(border_color="black"))

        CTkLabel(self.student_details_section,text="Phone*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=450)
        self.phone_entry = CTkEntry(self.student_details_section,placeholder_text="Enter your phone",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.phone_entry.place(x=130,y=445)
        self.phone_entry.bind("<Enter>",lambda event:self.phone_entry.configure(border_color="deep sky blue"))
        self.phone_entry.bind("<Leave>",lambda event:self.phone_entry.configure(border_color="black"))

        CTkLabel(self.student_details_section,text="Password*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=500)
        self.password_entry = CTkEntry(self.student_details_section,placeholder_text="Enter your password",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.password_entry.place(x=130,y=495)
        self.password_entry.bind("<Enter>",lambda event:self.password_entry.configure(border_color="deep sky blue"))
        self.password_entry.bind("<Leave>",lambda event:self.password_entry.configure(border_color="black"))

        self.student_details_section.place(x=295,y=10)

        # === Parent details section ===
        self.parent_details_section = CTkFrame(self.student_registration_frame,height=580,width=400,border_color="deep sky blue",border_width=3,bg_color="white",fg_color="white",corner_radius=20)
        CTkLabel(self.parent_details_section,text="Parent Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=100,y=25)

        CTkLabel(self.parent_details_section,text="Father's Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=100)
        self.father_name_entry = CTkEntry(self.parent_details_section,placeholder_text="Enter your father's name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.father_name_entry.place(x=180,y=95)
        self.father_name_entry.bind("<Enter>",lambda event:self.father_name_entry.configure(border_color="deep sky blue"))
        self.father_name_entry.bind("<Leave>",lambda event:self.father_name_entry.configure(border_color="black"))

        CTkLabel(self.parent_details_section,text="Father's occupation",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=150)
        self.father_occupation_entry = CTkEntry(self.parent_details_section,placeholder_text="Enter occupation",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.father_occupation_entry.place(x=180,y=145)
        self.father_occupation_entry.bind("<Enter>",lambda event:self.father_occupation_entry.configure(border_color="deep sky blue"))
        self.father_occupation_entry.bind("<Leave>",lambda event:self.father_occupation_entry.configure(border_color="black"))

        CTkLabel(self.parent_details_section,text="Father's phone",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=200)
        self.father_phone_entry = CTkEntry(self.parent_details_section,placeholder_text="Enter phone number",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.father_phone_entry.place(x=180,y=195)
        self.father_phone_entry.bind("<Enter>",lambda event:self.father_phone_entry.configure(border_color="deep sky blue"))
        self.father_phone_entry.bind("<Leave>",lambda event:self.father_phone_entry.configure(border_color="black"))

        CTkLabel(self.parent_details_section,text="Mother's Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=250)
        self.mother_name_entry = CTkEntry(self.parent_details_section,placeholder_text="Enter your mother's name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.mother_name_entry.place(x=180,y=245)
        self.mother_name_entry.bind("<Enter>",lambda event:self.mother_name_entry.configure(border_color="deep sky blue"))
        self.mother_name_entry.bind("<Leave>",lambda event:self.mother_name_entry.configure(border_color="black"))

        CTkLabel(self.parent_details_section,text="Mother's occupation",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=300)
        self.mother_occupation_entry = CTkEntry(self.parent_details_section,placeholder_text="Enter occupation",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.mother_occupation_entry.place(x=180,y=295)
        self.mother_occupation_entry.bind("<Enter>",lambda event:self.mother_occupation_entry.configure(border_color="deep sky blue"))
        self.mother_occupation_entry.bind("<Leave>",lambda event:self.mother_occupation_entry.configure(border_color="black"))

        CTkLabel(self.parent_details_section,text="Mother's phone",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=350)
        self.mother_phone_entry = CTkEntry(self.parent_details_section,placeholder_text="Enter phone number",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.mother_phone_entry.place(x=180,y=345)
        self.mother_phone_entry.bind("<Enter>",lambda event:self.mother_phone_entry.configure(border_color="deep sky blue"))
        self.mother_phone_entry.bind("<Leave>",lambda event:self.mother_phone_entry.configure(border_color="black"))

        CTkButton(self.parent_details_section,text="Submit",width=300,height=40,font=CTkFont(family="times new roman",size=25),fg_color="#1f7bd1",hover_color="deep sky blue",text_color="black",corner_radius=10,command=self.submit).place(x=50,y=450)

        self.parent_details_section.place(x=710,y=10)

        self.student_registration_frame.pack(pady=25)

        # ======================================================= Admin Registration Form ========================================================
        # ======================= Label & Date time =========================
        self.tabview.tab("Admin Registration").configure(fg_color = "light blue")
        CTkLabel(self.tabview.tab("Admin Registration"),text="ADMIN  REGISTRATION  FORM",text_color="black",font=CTkFont(family="times new roman",size=50,weight="bold"),bg_color="light blue").pack()
        self.admin_date_time = CTkLabel(self.tabview.tab("Admin Registration"),text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),bg_color="light blue")
        self.admin_date_time.place(x=1180,y=0)
        self.admin_date_time_update()
        CTkButton(self.tabview.tab("Admin Registration"),image=CTkImage(light_image=Image.open("images/back.png"),dark_image=Image.open("images/back.png"),size=(40,40)),text="",width=0,bg_color="light blue",corner_radius=20,command=lambda:self.tabview.set("Login Page")).place(x=10,y=10)

        # ======================= admin registration frame =========================
        self.admin_registration_frame = CTkFrame(self.tabview.tab("Admin Registration"),height=600,width=710,border_color="deep sky blue",border_width=3,bg_color="light blue",fg_color="white",corner_radius=20)

        # === Image section ====
        self.admin_image_frame = CTkFrame(self.admin_registration_frame,height=580,width=270,border_color="deep sky blue",border_width=3,bg_color="white",fg_color="white",corner_radius=20)
        self.admin_photo_frame = CTkFrame(self.admin_image_frame,height=250,width=190,border_color="black",border_width=3,bg_color="white",fg_color="black",corner_radius=10)
        self.admin_image = CTkImage(light_image=Image.open("images/upload image.png"),dark_image=Image.open("images/upload image.png"),size=(180,240))
        self.admin_photo_frame_img = CTkLabel(self.admin_photo_frame,text="",image=self.admin_image,width=180,height=240)
        self.admin_photo_frame_img.place(x=5,y=5)
        self.admin_photo_frame.place(x=40,y=40)
        CTkButton(self.admin_image_frame,text="upload image",width=190,height=40,fg_color="#1f7bd1",hover_color="deep sky blue",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),command=self.upload_image).place(x=40,y=350)
        self.admin_image_frame.place(x=10,y=10)

        # === admin Details section ===
        self.admin_details_section = CTkFrame(self.admin_registration_frame,height=580,width=400,border_color="deep sky blue",border_width=3,bg_color="white",fg_color="white",corner_radius=20)
        CTkLabel(self.admin_details_section,text="Admin Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=100,y=25)

        CTkLabel(self.admin_details_section,text="Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=100)
        self.admin_name_entry = CTkEntry(self.admin_details_section,placeholder_text="Enter your name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.admin_name_entry.place(x=130,y=95)
        self.admin_name_entry.bind("<Enter>",lambda event:self.admin_name_entry.configure(border_color="deep sky blue"))
        self.admin_name_entry.bind("<Leave>",lambda event:self.admin_name_entry.configure(border_color="black"))

        CTkLabel(self.admin_details_section,text="D.O.B*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=150)
        self.admin_dob_entry = CTkEntry(self.admin_details_section,placeholder_text="DD/MM/YYYY",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10,state="readonly")
        self.admin_dob_entry.place(x=130,y=145)
        CTkButton(self.admin_details_section,text="get",height=40,width=10,fg_color="#1f7bd1",hover_color="deep sky blue",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),border_color="black",border_width=2,command=self.getDate).place(x=340,y=145)
        self.admin_dob_entry.bind("<Enter>",lambda event:self.admin_dob_entry.configure(border_color="deep sky blue"))
        self.admin_dob_entry.bind("<Leave>",lambda event:self.admin_dob_entry.configure(border_color="black"))

        CTkLabel(self.admin_details_section,text="Gender*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=200)
        self.admin_gender_entry = StringVar(value = "")
        CTkRadioButton(self.admin_details_section,variable=self.admin_gender_entry,text="Male",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Male").place(x=130,y=195)
        CTkRadioButton(self.admin_details_section,variable=self.admin_gender_entry,text="Female",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Female").place(x=230,y=195)
        
        CTkLabel(self.admin_details_section,text="Education*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=250)
        self.admin_education_entry = CTkEntry(self.admin_details_section,placeholder_text="Enter your education",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.admin_education_entry.place(x=130,y=245)
        self.admin_education_entry.bind("<Enter>",lambda event:self.admin_education_entry.configure(border_color="deep sky blue"))
        self.admin_education_entry.bind("<Leave>",lambda event:self.admin_education_entry.configure(border_color="black"))

        CTkLabel(self.admin_details_section,text="Field*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=300)
        self.admin_field_entry = CTkEntry(self.admin_details_section,placeholder_text="Enter your field",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.admin_field_entry.place(x=130,y=295)
        self.admin_field_entry.bind("<Enter>",lambda event:self.admin_field_entry.configure(border_color="deep sky blue"))
        self.admin_field_entry.bind("<Leave>",lambda event:self.admin_field_entry.configure(border_color="black"))

        CTkLabel(self.admin_details_section,text="Email*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=350)
        self.admin_email_entry = CTkEntry(self.admin_details_section,placeholder_text="Enter your email",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.admin_email_entry.place(x=130,y=345)
        self.admin_email_entry.bind("<Enter>",lambda event:self.admin_email_entry.configure(border_color="deep sky blue"))
        self.admin_email_entry.bind("<Leave>",lambda event:self.admin_email_entry.configure(border_color="black"))

        CTkLabel(self.admin_details_section,text="Phone*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=400)
        self.admin_phone_entry = CTkEntry(self.admin_details_section,placeholder_text="Enter your phone",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.admin_phone_entry.place(x=130,y=395)
        self.admin_phone_entry.bind("<Enter>",lambda event:self.admin_phone_entry.configure(border_color="deep sky blue"))
        self.admin_phone_entry.bind("<Leave>",lambda event:self.admin_phone_entry.configure(border_color="black"))

        CTkLabel(self.admin_details_section,text="Password*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=10,y=450)
        self.admin_password_entry = CTkEntry(self.admin_details_section,placeholder_text="Enter your password",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
        self.admin_password_entry.place(x=130,y=445)
        self.admin_password_entry.bind("<Enter>",lambda event:self.admin_password_entry.configure(border_color="deep sky blue"))
        self.admin_password_entry.bind("<Leave>",lambda event:self.admin_password_entry.configure(border_color="black"))

        CTkButton(self.admin_details_section,text="Submit",width=300,height=40,font=CTkFont(family="times new roman",size=25),fg_color="#1f7bd1",hover_color="deep sky blue",text_color="black",corner_radius=10,command=self.submit).place(x=50,y=520)

        self.admin_details_section.place(x=300,y=10)

        self.admin_registration_frame.pack(pady=25)

        # ======================================================= Student Dashboard ========================================================
        # ======================= Label & Date time =========================
        self.tabview.tab("Student Dashboard").configure(fg_color="light green")
        CTkLabel(self.tabview.tab("Student Dashboard"),text="STUDENT  DASHBOARD",text_color="black",font=CTkFont(family="times new roman",size=50,weight="bold"),bg_color="light green").pack()
        self.dashboard_date_time = CTkLabel(self.tabview.tab("Student Dashboard"),text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),bg_color="light green")
        self.dashboard_date_time.place(x=1180,y=0)
        self.dashboard_date_time_update()
        CTkButton(self.tabview.tab("Student Dashboard"),image=CTkImage(dark_image=Image.open("images/back.png"),light_image=Image.open("images/back.png"),size=(40,40)),text="",width=0,bg_color="light green",corner_radius=20,command=self.back_to_admin_panel).place(x=10,y=10)

        self.student_dashboard_functions = CTkFrame(self.tabview.tab("Student Dashboard"),width=150,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
        self.btn1 = CTkButton(self.student_dashboard_functions,text="Home",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",border_width=3,border_color="blue",hover=False,command=self.dashboard_home)
        self.btn1.place(x=5,y=20)
        self.btn1.bind("<Enter>",lambda event:self.btn1.configure(text_color="green2"))
        self.btn1.bind("<Leave>",lambda event:self.btn1.configure(text_color="black"))
        self.btn1.bind("<Button-1>",lambda event:self.outline_btn(self.btn1))
        self.btn2 = CTkButton(self.student_dashboard_functions,text="ID Card",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.generate_id_card)
        self.btn2.place(x=5,y=80)
        self.btn2.bind("<Enter>",lambda event:self.btn2.configure(text_color="green2"))
        self.btn2.bind("<Leave>",lambda event:self.btn2.configure(text_color="black"))
        self.btn2.bind("<Button-1>",lambda event:self.outline_btn(self.btn2))
        self.btn3 = CTkButton(self.student_dashboard_functions,text="Password",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.edit_password)
        self.btn3.place(x=5,y=140)
        self.btn3.bind("<Enter>",lambda event:self.btn3.configure(text_color="green2"))
        self.btn3.bind("<Leave>",lambda event:self.btn3.configure(text_color="black"))
        self.btn3.bind("<Button-1>",lambda event:self.outline_btn(self.btn3))
        self.btn4 = CTkButton(self.student_dashboard_functions,text="Edit",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.edit_profile)
        self.btn4.place(x=5,y=200)
        self.btn4.bind("<Enter>",lambda event:self.btn4.configure(text_color="green2"))
        self.btn4.bind("<Leave>",lambda event:self.btn4.configure(text_color="black"))
        self.btn4.bind("<Button-1>",lambda event:self.outline_btn(self.btn4))
        self.btn5 = CTkButton(self.student_dashboard_functions,text="Chat AI",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.chat_ai)
        self.btn5.place(x=5,y=260)
        self.btn5.bind("<Enter>",lambda event:self.btn5.configure(text_color="green2"))
        self.btn5.bind("<Leave>",lambda event:self.btn5.configure(text_color="black"))
        self.btn5.bind("<Button-1>",lambda event:self.outline_btn(self.btn5))
        self.btn6 = CTkButton(self.student_dashboard_functions,text="Delete",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.delete_account)
        self.btn6.place(x=5,y=320)
        self.btn6.bind("<Enter>",lambda event:self.btn6.configure(text_color="red"))
        self.btn6.bind("<Leave>",lambda event:self.btn6.configure(text_color="black"))
        self.btn7 = CTkButton(self.student_dashboard_functions,text="Logout",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.dashboard_logout)
        self.btn7.place(x=5,y=380)
        self.btn7.bind("<Enter>",lambda event:self.btn7.configure(text_color="red"))
        self.btn7.bind("<Leave>",lambda event:self.btn7.configure(text_color="black"))
        self.student_dashboard_functions.pack(pady=25,padx=45,side=LEFT)

        self.student_dashboard_functions_show = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
        self.student_dashboard_functions_show.pack(pady=25,side=LEFT)
        self.student_dashboard_home, self.id_card_outer_frame, self.edit_password_frame,self.edit_profile_frame,self.chat_ai_frame = None,None,None,None,None

        # ======================================================= Admin Dashboard ========================================================
        # ======================= Label & Date time =========================
        self.tabview.tab("Admin Dashboard").configure(fg_color="light green")
        CTkLabel(self.tabview.tab("Admin Dashboard"),text="ADMIN  DASHBOARD",text_color="black",font=CTkFont(family="times new roman",size=50,weight="bold"),bg_color="light green").pack()
        self.admin_dashboard_date_time = CTkLabel(self.tabview.tab("Admin Dashboard"),text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),bg_color="light green")
        self.admin_dashboard_date_time.place(x=1180,y=0)
        self.admin_dashboard_date_time_update()
        CTkButton(self.tabview.tab("Admin Dashboard"),image=CTkImage(dark_image=Image.open("images/college_web_btn.png"),light_image=Image.open("images/college_web_btn.png"),size=(80,80)),text="",width=0,height=0,fg_color="transparent",hover=False,corner_radius=50,command=lambda:webbrowser.open("https://www.sdcetmzn.org/")).place(x=70,y=1)

        self.admin_dashboard_functions = CTkFrame(self.tabview.tab("Admin Dashboard"),width=150,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
        self.btn10 = CTkButton(self.admin_dashboard_functions,text="Home",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",border_width=3,border_color="blue",hover=False,command=self.admin_home)
        self.btn10.place(x=5,y=20)
        self.btn10.bind("<Enter>",lambda event:self.btn10.configure(text_color="green2"))
        self.btn10.bind("<Leave>",lambda event:self.btn10.configure(text_color="black"))
        self.btn10.bind("<Button-1>",lambda event:self.outline_btn(self.btn10))
        self.btn11 = CTkButton(self.admin_dashboard_functions,text="You",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.dashboard_home)
        self.btn11.place(x=5,y=80)
        self.btn11.bind("<Enter>",lambda event:self.btn11.configure(text_color="green2"))
        self.btn11.bind("<Leave>",lambda event:self.btn11.configure(text_color="black"))
        self.btn11.bind("<Button-1>",lambda event:self.outline_btn(self.btn11))
        self.btn12 = CTkButton(self.admin_dashboard_functions,text="ID Card",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.generate_id_card)
        self.btn12.place(x=5,y=140)
        self.btn12.bind("<Enter>",lambda event:self.btn12.configure(text_color="green2"))
        self.btn12.bind("<Leave>",lambda event:self.btn12.configure(text_color="black"))
        self.btn12.bind("<Button-1>",lambda event:self.outline_btn(self.btn12))
        self.btn13 = CTkButton(self.admin_dashboard_functions,text="Password",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.edit_password)
        self.btn13.place(x=5,y=200)
        self.btn13.bind("<Enter>",lambda event:self.btn13.configure(text_color="green2"))
        self.btn13.bind("<Leave>",lambda event:self.btn13.configure(text_color="black"))
        self.btn13.bind("<Button-1>",lambda event:self.outline_btn(self.btn13))
        self.btn14 = CTkButton(self.admin_dashboard_functions,text="Edit",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.edit_profile)
        self.btn14.place(x=5,y=260)
        self.btn14.bind("<Enter>",lambda event:self.btn14.configure(text_color="green2"))
        self.btn14.bind("<Leave>",lambda event:self.btn14.configure(text_color="black"))
        self.btn14.bind("<Button-1>",lambda event:self.outline_btn(self.btn14))
        self.btn15 = CTkButton(self.admin_dashboard_functions,text="Chat AI",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.chat_ai)
        self.btn15.place(x=5,y=320)
        self.btn15.bind("<Enter>",lambda event:self.btn15.configure(text_color="green2"))
        self.btn15.bind("<Leave>",lambda event:self.btn15.configure(text_color="black"))
        self.btn15.bind("<Button-1>",lambda event:self.outline_btn(self.btn15))
        self.btn16 = CTkButton(self.admin_dashboard_functions,text="Delete",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.delete_account)
        self.btn16.place(x=5,y=380)
        self.btn16.bind("<Enter>",lambda event:self.btn16.configure(text_color="red"))
        self.btn16.bind("<Leave>",lambda event:self.btn16.configure(text_color="black"))
        self.btn17 = CTkButton(self.admin_dashboard_functions,text="Logout",font=("times new roman",30,"bold"),text_color="black",width=0,bg_color="white",fg_color="white",hover=False,command=self.dashboard_logout)
        self.btn17.place(x=5,y=440)
        self.btn17.bind("<Enter>",lambda event:self.btn17.configure(text_color="red"))
        self.btn17.bind("<Leave>",lambda event:self.btn17.configure(text_color="black"))
        self.admin_dashboard_functions.pack(pady=25,padx=45,side=LEFT)

        self.admin_dashboard_functions_show = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
        self.admin_dashboard_functions_show.pack(pady=25,side=LEFT)
        self.admin_dashboard_home,self.admin_dashboard_you,self.admin_card_outer_frame,self.admin_edit_password_frame,self.admin_edit_profile_frame,self.admin_chat_ai_frame=None,None,None,None,None,None

        # ============================= Run time Entities ============================
        if not os.path.exists("Student Images"):os.makedirs("Student Images")
        if not os.path.exists("Admin Images"):os.makedirs("Admin Images")
        self.filename = ""
        self.student_login_name,self.student_login_password = "",""
        self.admin_login_name,self.admin_login_password = "",""

        self.mainloop()

    # ======================= Functionality part =========================
    def connect_to_db_window(self):
        self.db_window = CTkToplevel()
        self.db_window.grab_set()
        self.db_window.title("Student Registration & Management System")
        self.db_window.geometry("380x370")
        self.db_window.configure(fg_color="white")
        self.db_window.resizable(False,False)
        CTkLabel(self.db_window,text="Database Connection",font=CTkFont(family="times new roman",size=40,weight="bold",underline=True),text_color="blue").pack()
        CTkLabel(self.db_window,text="Host (op) :",font=CTkFont(family="times new roman",size=30,weight="bold"),text_color="blue").place(x=10,y=80)
        host = CTkEntry(self.db_window,placeholder_text="Enter Host (localhost)",placeholder_text_color="gray",width=200,height=40,font=CTkFont(family="times new roman",size=20),text_color="blue",fg_color="white",border_color="green",border_width=2)
        host.place(x=170,y=80)
        CTkLabel(self.db_window,text="User (op) :",font=CTkFont(family="times new roman",size=30,weight="bold"),text_color="blue").place(x=10,y=130)
        root = CTkEntry(self.db_window,placeholder_text="Enter User (root)",placeholder_text_color="gray",width=200,height=40,font=CTkFont(family="times new roman",size=20),text_color="blue",fg_color="white",border_color="green",border_width=2)
        root.place(x=170,y=130)
        CTkLabel(self.db_window,text="Password* :",font=CTkFont(family="times new roman",size=30,weight="bold"),text_color="blue").place(x=10,y=180)
        password = CTkEntry(self.db_window,placeholder_text="Enter Password",placeholder_text_color="gray",width=200,height=40,font=CTkFont(family="times new roman",size=20),text_color="blue",fg_color="white",border_color="green",border_width=2)
        password.place(x=170,y=180)
        CTkLabel(self.db_window,text="Port (op) :",font=CTkFont(family="times new roman",size=30,weight="bold"),text_color="blue").place(x=10,y=230)
        port = CTkEntry(self.db_window,placeholder_text="Enter Port (3306)",placeholder_text_color="gray",width=200,height=40,font=CTkFont(family="times new roman",size=20),text_color="blue",fg_color="white",border_color="green",border_width=2)
        port.place(x=170,y=230)
        CTkButton(self.db_window,text="Connect",width=200,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",command=lambda:self.connect_to_db(host.get(),root.get(),password.get(),port.get())).place(x=90,y=300)
        self.db_window.mainloop()

    def connect_to_db(self,host,user,password,port):
        if host == "":host = "localhost"
        if user == "":user = "root"
        if password == "":password = ""
        if port == "":port = "3306"
        try:
            try:conn = pymysql.connect(host=host,user=user,password=password,port=int(port))
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                messagebox.showinfo("Success","Database Connected Successfully !!!")
                self.db_host = host
                self.db_user = user
                self.db_password = password
                self.db_port = int(port)
                self.db_window.destroy()
                self.register_btn.configure(state=NORMAL)
                self.login_btn.configure(state=NORMAL)
                self.forgot_password.configure(state=NORMAL)
                self.db_btn.configure(image=CTkImage(light_image=Image.open("images/db_present.png"),dark_image=Image.open("images/db_present.png"),size=(42,42)),state=DISABLED)
                self.creating_db()
            finally:conn.close()
        except:pass

    def creating_db(self):
        try:
            conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port)
            cursor = conn.cursor()
            query1 = "CREATE DATABASE IF NOT EXISTS student_registration_and_management_system"
            query2 = "USE student_registration_and_management_system"
            query3 = "CREATE TABLE IF NOT EXISTS student_data(Registration_ID INT PRIMARY KEY AUTO_INCREMENT,Student_name VARCHAR(50),DOB DATE,Gender VARCHAR(10),Class VARCHAR(20),Field VARCHAR(50),Roll_number VARCHAR(20),Email VARCHAR(50),Phone_number BIGINT,Password VARCHAR(30),Father_name VARCHAR(50),Father_occupation VARCHAR(50),Father_phone BIGINT,Mother_name VARCHAR(50),Mother_occupation VARCHAR(50),Mother_phone BIGINT,Registration_Date_time DATETIME)"
            query4 = "CREATE TABLE IF NOT EXISTS admin_data(Registration_ID INT PRIMARY KEY AUTO_INCREMENT,Admin_name VARCHAR(50),DOB DATE,Gender VARCHAR(10),Education VARCHAR(50),Field VARCHAR(50),Email VARCHAR(50),Phone_number BIGINT,Password VARCHAR(30),Registration_Date_time DATETIME)"
            cursor.execute(query1)
            cursor.execute(query2)
            cursor.execute(query3)
            cursor.execute(query4)
        except Exception as e:messagebox.showerror("Error",str(e))
        finally:conn.close()

    def login(self):
        if self.login_type.get() == "Admin" or self.login_type.get() == "Student":
            if not self.user_entry.get() or not self.pass_entry.get():
                messagebox.showerror("Error","Both fields are required !!!")
                return
            conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
            cursor = conn.cursor()
            if self.login_type.get() == "Admin":
                try:
                    query = "SELECT Password FROM admin_data WHERE Admin_name = %s AND Password = %s"
                    cursor.execute(query,(self.user_entry.get(),self.pass_entry.get()))
                    result = cursor.fetchone()  # fetching only 1st occurence of username
                    if result[0] != self.pass_entry.get(): raise Exception
                except:
                    conn.close()
                    messagebox.showerror("Error","Invalid username or password !!!")
                else:
                    self.tabview.set("Admin Dashboard")
                    conn.close()
                    self.admin_login_name = self.user_entry.get()
                    self.admin_login_password = self.pass_entry.get()
                    self.generate_qr()
                    self.admin_home()
                    self.outline_btn(self.btn10)
            elif self.login_type.get() == "Student":
                try:
                    query = "SELECT Password FROM student_data WHERE Student_name = %s AND Password = %s"
                    cursor.execute(query,(self.user_entry.get(),self.pass_entry.get()))
                    result = cursor.fetchone()
                    if result[0] != self.pass_entry.get(): raise Exception
                except:
                    conn.close()
                    messagebox.showerror("Error","Invalid username or password !!!")
                else:
                    self.tabview.set("Student Dashboard")
                    conn.close()
                    self.student_login_name = self.user_entry.get()
                    self.student_login_password = self.pass_entry.get()
                    self.generate_qr()
                    self.dashboard_home()
                    self.outline_btn(self.btn1)
            # Reset details
            self.user_entry.delete(0,END)
            self.pass_entry.delete(0,END)
        else: messagebox.showerror("Error","Please select login type !!!")

    def forgot_password_email(self):
        if self.login_type.get() == "Student":
            self.mail_window = CTkToplevel()
            self.mail_window.title("Forgot Password Student")
            self.mail_window.geometry("400x200")
            self.mail_window.resizable(False,False)
            self.mail_window.grab_set()
            user_name = CTkEntry(self.mail_window,placeholder_text="Enter your username",width=300,height=40)
            user_name.pack(pady=10)
            roll_no = CTkEntry(self.mail_window,placeholder_text="Enter your roll number",width=300,height=40)
            roll_no.pack(pady=10)
            CTkButton(self.mail_window,text="Check",font=CTkFont(family="times new roman",size=20),width=300,height=40,command=lambda:self.Checking_data(type="Student",Student_name=user_name.get(),Roll_number=roll_no.get())).pack(pady=10)
            self.mail_window.mainloop()
        elif self.login_type.get() == "Admin":
            self.mail_window = CTkToplevel()
            self.mail_window.title("Forgot Password Admin")
            self.mail_window.geometry("400x200")
            self.mail_window.resizable(False,False)
            self.mail_window.grab_set()
            user_name = CTkEntry(self.mail_window,placeholder_text="Enter your username",width=300,height=40)
            user_name.pack(pady=10)
            phone_no = CTkEntry(self.mail_window,placeholder_text="Enter your phone number",width=300,height=40)
            phone_no.pack(pady=10)
            CTkButton(self.mail_window,text="Check",font=CTkFont(family="times new roman",size=20),width=300,height=40,command=lambda:self.Checking_data(type="Admin",Admin_name=user_name.get(),Admin_phone_number=phone_no.get())).pack(pady=10)
            self.mail_window.mainloop()
        else:messagebox.showerror("Error","Please select login type !!!")
    
    def Checking_data(self,type,Student_name=None,Roll_number=None,Admin_name=None,Admin_phone_number=None):
        if type == "Student":
            if not Student_name or not Roll_number:
                messagebox.showerror("Error","Both fields are required !!!")
                return
            try:
                conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                cursor = conn.cursor()
                query = "SELECT Email,Password FROM student_data WHERE Student_name = %s AND Roll_number = %s"
                cursor.execute(query,(Student_name,Roll_number))
                data = cursor.fetchone()
                if data == None: raise Exception("No data found")
                else: self.send_mail(data[0],data[1])
            except Exception as e:messagebox.showerror("Error",str(e)+" (Internet Connection Error)")
            else:
                messagebox.showinfo("Success","Your password has been sent to your email address")
                self.mail_window.destroy()
            finally:conn.close()
        elif type == "Admin":
            if not Admin_name or not Admin_phone_number:
                messagebox.showerror("Error","Both fields are required !!!")
                return
            try:
                conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                cursor = conn.cursor()
                query = "SELECT Email,Password FROM admin_data WHERE Admin_name = %s AND Phone_number = %s"
                cursor.execute(query,(Admin_name,Admin_phone_number))
                data = cursor.fetchone()
                if data == None: raise Exception("No data found")
                else: self.send_mail(data[0],data[1])
            except Exception as e:messagebox.showerror("Error",str(e)+" (Internet Connection Error)")
            else:
                messagebox.showinfo("Success","Your password has been sent to your email address")
                self.mail_window.destroy()
            finally:conn.close()
    
    def send_mail(self,receiver_email,forgot_password):
        import smtplib
        connection = smtplib.SMTP("smtp.gmail.com",587)
        connection.starttls()
        connection.login(user="pythonprogramminglanguage2024@gmail.com",password="ogwm eucx asla ight")
        connection.sendmail(from_addr="pythonprogramminglanguage2024@gmail.com",to_addrs=receiver_email,msg=f"Your password is {forgot_password}")
        connection.quit()

    def date_time_update(self):
        self.date_time.configure(text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}")
        self.date_time.after(1000,self.date_time_update)
    
    def admin_date_time_update(self):
        self.admin_date_time.configure(text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}")
        self.admin_date_time.after(1000,self.admin_date_time_update)

    def dashboard_date_time_update(self):
        self.dashboard_date_time.configure(text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}")
        self.dashboard_date_time.after(1000,self.dashboard_date_time_update)
    
    def admin_dashboard_date_time_update(self):
        self.admin_dashboard_date_time.configure(text=f"{datetime.datetime.now().strftime('%d/%m/%Y')}\n{datetime.datetime.now().strftime('%H:%M:%S')}")
        self.admin_dashboard_date_time.after(1000,self.admin_dashboard_date_time_update)

    def getDate(self):
        self.subRoot = CTkToplevel()
        self.subRoot.grab_set()
        self.subRoot.title("Calendar")
        self.subRoot.config(bg="deep sky blue")
        self.subRoot.resizable(False,False)
        self.cal = Calendar(self.subRoot,selectmode = 'day',year = 2005,month=8,day=26)
        self.cal.pack()
        CTkButton(self.subRoot,text="Get Date",font=("times new roman",18,"bold"),bg_color="deep sky blue",command=self.grab_date).pack(pady=10)
        self.subRoot.mainloop()

    def grab_date(self):
        self.date = datetime.datetime.strptime(self.cal.get_date(), '%m/%d/%y').strftime('%d/%m/%Y')
        if self.tabview.get() == "Student Registration":
            self.dob_entry.configure(state="normal")
            self.dob_entry.delete(0,END)
            self.dob_entry.insert(0,self.date)
            self.dob_entry.configure(state="readonly")
        elif self.tabview.get() == "Admin Registration":
            self.admin_dob_entry.configure(state="normal")
            self.admin_dob_entry.delete(0,END)
            self.admin_dob_entry.insert(0,self.date)
            self.admin_dob_entry.configure(state="readonly")
        elif self.tabview.get() == "Student Dashboard":
            self.dob_entry_update.configure(state="normal")
            self.dob_entry_update.delete(0,END)
            self.dob_entry_update.insert(0,self.date)
            self.dob_entry_update.configure(state="readonly")
        elif self.tabview.get() == "Admin Dashboard":
            self.admin_dob_entry_update.configure(state="normal")
            self.admin_dob_entry_update.delete(0,END)
            self.admin_dob_entry_update.insert(0,self.date)
            self.admin_dob_entry_update.configure(state="readonly")
        self.subRoot.destroy()

    def upload_image(self):
        self.filename = filedialog.askopenfilename(title="Select Image File",filetypes=(("JPG File","*.jpg"),("PNG File","*.png"),("All files","*.txt")))
        if self.tabview.get() == "Student Registration":
            self.student_image = CTkImage(dark_image=Image.open(self.filename),light_image=Image.open(self.filename),size=(180,240))
            self.photo_frame_img.configure(image=self.student_image)
        else:
            self.admin_image = CTkImage(dark_image=Image.open(self.filename),light_image=Image.open(self.filename),size=(180,240))
            self.admin_photo_frame_img.configure(image=self.admin_image)

    def submit(self):
        if self.tabview.get() == "Student Registration":
            if self.name_entry.get() != "" and self.dob_entry.get() != "" and self.gender_entry.get() != "" and self.class_entry.get() != "Select Class" and self.field_entry.get() != "" and self.roll_no_entry.get() != "" and self.phone_entry.get() != "" and self.email_entry.get() != "" and self.password_entry.get() != "" and self.father_name_entry.get() != "" and self.mother_name_entry.get() != "":
                if self.email_entry.get().endswith("@gmail.com") and self.email_entry.get().count(" ") == 0:
                    if self.phone_entry.get().isdigit() and len(self.phone_entry.get()) == 10 and ((self.father_phone_entry.get().isdigit() and len(self.father_phone_entry.get()) == 10) or self.father_phone_entry.get() == "") and ((self.mother_phone_entry.get().isdigit() and len(self.mother_phone_entry.get()) == 10) or self.mother_phone_entry.get() == ""):
                        if self.filename == "":
                            messagebox.showerror("Error","Please select an image !!!")
                            return
                        # Database connectivity for student registration
                        conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                        cursor = conn.cursor()
                        try:
                            query = "INSERT INTO student_data(Student_name,DOB,Gender,Class,Field,Roll_number,Email,Phone_number,Password,Father_name,Father_occupation,Father_phone,Mother_name,Mother_occupation,Mother_phone,Registration_Date_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            cursor.execute(query,(self.name_entry.get(),datetime.datetime.strptime(self.dob_entry.get(), '%d/%m/%Y').strftime('%Y-%m-%d'),self.gender_entry.get(),self.class_entry.get(),self.field_entry.get(),self.roll_no_entry.get(),self.email_entry.get(),self.phone_entry.get(),self.password_entry.get(),self.father_name_entry.get(),self.father_occupation_entry.get() if self.father_occupation_entry.get() != "" else None,self.father_phone_entry.get() if self.father_phone_entry.get() != "" else None,self.mother_name_entry.get(),self.mother_occupation_entry.get() if self.mother_occupation_entry.get() != "" else None,self.mother_phone_entry.get() if self.mother_phone_entry.get() != "" else None,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            conn.commit()
                        except Exception as e:messagebox.showerror("Error",str(e))
                        else:
                            self.save_image()
                            messagebox.showinfo("Success","Registration Successful !!!")
                            # Reset the form
                            self.name_entry.delete(0,END)
                            self.dob_entry.delete(0,END)
                            self.gender_entry.set("")
                            self.class_entry.set("Select Class")
                            self.field_entry.delete(0,END)
                            self.roll_no_entry.delete(0,END)
                            self.phone_entry.delete(0,END)
                            self.email_entry.delete(0,END)
                            self.password_entry.delete(0,END)
                            self.father_name_entry.delete(0,END)
                            self.father_occupation_entry.delete(0,END)
                            self.father_phone_entry.delete(0,END)
                            self.mother_name_entry.delete(0,END)
                            self.mother_occupation_entry.delete(0,END)
                            self.mother_phone_entry.delete(0,END)
                            self.student_image = CTkImage(light_image=Image.open("images/upload image.png"),dark_image=Image.open("images/upload image.png"),size=(180,240))
                            self.photo_frame_img.configure(image=self.student_image)
                        finally:conn.close()
                    else:messagebox.showerror("Error","Please enter a valid phone number !!!")
                else:messagebox.showerror("Error","Please enter a valid email address !!!")
            else:messagebox.showerror("Error","All fields are required !!!")
        elif self.tabview.get() == "Admin Registration":
            if self.admin_name_entry.get() != "" and self.admin_dob_entry.get() != "" and self.admin_gender_entry.get() != "" and self.admin_education_entry.get() != "" and self.admin_field_entry.get() != "" and self.admin_phone_entry.get() != "" and self.admin_email_entry.get() != "" and self.admin_password_entry.get() != "":
                if self.admin_email_entry.get().endswith("@gmail.com") and self.admin_email_entry.get().count(" ") == 0:
                    if self.admin_phone_entry.get().isdigit() and len(self.admin_phone_entry.get()) == 10:
                        if self.filename == "":
                            messagebox.showerror("Error","Please upload your image !!!")
                            return
                        # Database Connectivity for admin registration
                        conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                        cursor = conn.cursor()
                        try:
                            query = "INSERT INTO admin_data(Admin_name,DOB,Gender,Education,Field,Email,Phone_number,Password,Registration_Date_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            value = (self.admin_name_entry.get(),datetime.datetime.strptime(self.admin_dob_entry.get(),"%d/%m/%Y").strftime("%Y-%m-%d"),self.admin_gender_entry.get(),self.admin_education_entry.get(),self.admin_field_entry.get(),self.admin_email_entry.get(),self.admin_phone_entry.get(),self.admin_password_entry.get(),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            cursor.execute(query,value)
                            conn.commit()
                        except Exception as e:messagebox.showerror("Error",str(e))
                        else:
                            self.save_image()
                            messagebox.showinfo("Success","Registration Successful !!!")
                            # Reset the form
                            self.admin_name_entry.delete(0,END)
                            self.admin_dob_entry.delete(0,END)
                            self.admin_gender_entry.set("")
                            self.admin_education_entry.delete(0,END)
                            self.admin_field_entry.delete(0,END)
                            self.admin_phone_entry.delete(0,END)
                            self.admin_email_entry.delete(0,END)
                            self.admin_password_entry.delete(0,END)
                            self.admin_image = CTkImage(light_image=Image.open("images/upload image.png"),dark_image=Image.open("images/upload image.png"),size=(180,240))
                            self.admin_photo_frame_img.configure(image=self.admin_image)
                        finally:conn.close()
                    else:messagebox.showerror("Error","Please enter a valid phone number !!!")
                else:messagebox.showerror("Error","Please enter a valid email address !!!")
            else:messagebox.showerror("Error","All fields are required !!!")

    def save_image(self):
        if self.filename != "":
            img = Image.open(self.filename)
            img = img.resize((180,240))
            img.save(f"Student Images/{self.name_entry.get()}{self.roll_no_entry.get()}.jpg") if self.tabview.get() == "Student Registration" else img.save(f"Admin Images/{self.admin_name_entry.get()}{self.admin_phone_entry.get()}.jpg")
            img.close()
            self.filename = ""
        
    def generate_qr(self):
        conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
        cursor = conn.cursor()
        if self.tabview.get() == "Student Dashboard":
            try:
                query = "SELECT * FROM student_data WHERE Student_name = %s AND Password = %s"
                cursor.execute(query,(self.student_login_name,self.student_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                qr_data = f"=====Student details=====\nName: {data[1]}\nD.O.B.:{data[2]}\nGender: {data[3]}\nClass: {data[4]}\nField: {data[5]}\nRoll no.: {data[6]}\nEmail: {data[7]}\nPhone: {data[8]}\n\n=====Parent's Details=====\nFather's Name: {data[10]}\nFather's occupation: {data[11]}\nFather's phone: {data[12]}\nMother's Name: {data[13]}\nMother's occupation: {data[14]}\nMother's phone: {data[15]}"
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=1)
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img = img.resize((230,230))
                img.save("temp_qr.png")
            finally:conn.close()
        else:
            try:
                query = "SELECT * FROM admin_data WHERE Admin_name = %s AND Password = %s"
                cursor.execute(query,(self.admin_login_name,self.admin_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                qr_data = f"===== Admin Details =====\nName: {data[1]}\nD.O.B.:{data[2]}\nGender: {data[3]}\nEducatoin: {data[4]}\nField: {data[5]}\nEmail: {data[6]}\nPhone: {data[7]}"
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=1)
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img = img.resize((230,230))
                img.save("temp_qr.png")
            finally:conn.close()

    def outline_btn(self,bt_c):
        if self.tabview.get() == "Student Dashboard":
            for btn in (self.btn1,self.btn2, self.btn3, self.btn4, self.btn5):
                if btn == bt_c:
                    btn.configure(border_width=3,border_color="blue")
                else:
                    btn.configure(border_width=0, border_color="white")
        elif self.tabview.get() == "Admin Dashboard":
            for btn in (self.btn10,self.btn11, self.btn12, self.btn13,self.btn14,self.btn15):
                if btn == bt_c:
                    btn.configure(border_width=3,border_color="blue")
                else:
                    btn.configure(border_width=0, border_color="white")

    def dashboard_home(self):
        if self.student_login_name == "" and self.admin_login_name == "":
            messagebox.showerror("Error","Please login first !!!")
            return
        conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
        cursor = conn.cursor()
        if self.tabview.get() == "Student Dashboard":
            try:
                query = "SELECT * FROM student_data WHERE Student_name = %s AND Password = %s"
                cursor.execute(query,(self.student_login_name,self.student_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:   
                self.delete_previous_functions()
                self.student_dashboard_home = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                student_image = Image.open(f"Student Images/{data[1]}{data[6]}.jpg")
                CTkLabel(self.student_dashboard_home,text="",image=CTkImage(dark_image=student_image,light_image=student_image,size=(180,240))).place(x=50,y=25)
                student_image.close()
                qr_image = Image.open("temp_qr.png")
                CTkLabel(self.student_dashboard_home,text="",image=CTkImage(dark_image=qr_image,light_image=qr_image,size=(230,230))).place(x=25,y=280)
                qr_image.close()
                CTkButton(self.student_dashboard_home,text="Save",width=0,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.save_qr).place(x=30,y=520)
                CTkButton(self.student_dashboard_home,text="WhatsApp",width=0,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=lambda:self.whatsapp_qr(data[1],data[8])).place(x=120,y=520)

                CTkLabel(self.student_dashboard_home,text="Your Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=320,y=25)
                CTkLabel(self.student_dashboard_home,text=f"Name\t: {data[1]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=100)
                CTkLabel(self.student_dashboard_home,text=f"D.O.B.\t: {datetime.datetime.strptime(str(data[2]), '%Y-%m-%d').strftime('%d/%m/%Y')}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=150)
                CTkLabel(self.student_dashboard_home,text=f"Gender\t: {data[3]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=200)
                CTkLabel(self.student_dashboard_home,text=f"Class\t: {data[4]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=250)
                CTkLabel(self.student_dashboard_home,text=f"Field\t : {data[5]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=300)
                CTkLabel(self.student_dashboard_home,text=f"Roll no.\t: {data[6]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=350)
                CTkLabel(self.student_dashboard_home,text=f"Email\t: {data[7]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=400)
                CTkLabel(self.student_dashboard_home,text=f"Phone\t: {data[8]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=300,y=450)

                CTkLabel(self.student_dashboard_home,text="Parent Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=700,y=25)
                CTkLabel(self.student_dashboard_home,text=f"Father's Name\t: {data[10]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=650,y=100)
                CTkLabel(self.student_dashboard_home,text=f"Father's occupation : {data[11] if data[11] else ''}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=650,y=150)
                CTkLabel(self.student_dashboard_home,text=f"Father's phone\t: {data[12] if data[12] else ''}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=650,y=200)
                CTkLabel(self.student_dashboard_home,text=f"Mother's Name\t: {data[13]}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=650,y=250)
                CTkLabel(self.student_dashboard_home,text=f"Mother's occupation : {data[14] if data[14] else ''}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=650,y=300)
                CTkLabel(self.student_dashboard_home,text=f"Mother's phone\t: {data[15] if data[15] else ''}",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=650,y=350)
                self.student_dashboard_home.pack(pady=25,side=LEFT)
            finally:conn.close()
        else:
            try:
                query = "SELECT * FROM admin_data WHERE Admin_name = %s AND Password = %s"
                cursor.execute(query,(self.admin_login_name,self.admin_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                self.delete_previous_functions()
                self.admin_dashboard_you = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                admin_image = Image.open(f"Admin Images/{data[1]}{data[7]}.jpg")
                CTkLabel(self.admin_dashboard_you,text="",image=CTkImage(dark_image=admin_image,light_image=admin_image,size=(180,240))).place(x=50,y=25)
                admin_image.close()
                qr_image = Image.open("temp_qr.png")
                CTkLabel(self.admin_dashboard_you,text="",image=CTkImage(dark_image=qr_image,light_image=qr_image,size=(230,230))).place(x=25,y=280)
                qr_image.close()
                CTkButton(self.admin_dashboard_you,text="Save",width=0,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.save_qr).place(x=30,y=520)
                CTkButton(self.admin_dashboard_you,text="WhatsApp",width=0,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=lambda:self.whatsapp_qr(data[1],data[7])).place(x=120,y=520)

                CTkLabel(self.admin_dashboard_you,text="Your Details",text_color="black",font=CTkFont(family="times new roman",size=32,weight="bold",underline=True)).place(x=400,y=25)
                CTkLabel(self.admin_dashboard_you,text=f"Name\t: {data[1]}",text_color="black",font=CTkFont(family="times new roman",size=25,weight="bold")).place(x=350,y=100)
                CTkLabel(self.admin_dashboard_you,text=f"D.O.B.\t: {datetime.datetime.strptime(str(data[2]), '%Y-%m-%d').strftime('%d/%m/%Y')}",text_color="black",font=CTkFont(family="times new roman",size=25,weight="bold")).place(x=350,y=150)
                CTkLabel(self.admin_dashboard_you,text=f"Gender\t: {data[3]}",text_color="black",font=CTkFont(family="times new roman",size=25,weight="bold")).place(x=350,y=200)
                CTkLabel(self.admin_dashboard_you,text=f"Education : {data[4]}",text_color="black",font=CTkFont(family="times new roman",size=25,weight="bold")).place(x=350,y=250)
                CTkLabel(self.admin_dashboard_you,text=f"Field\t: {data[5]}",text_color="black",font=CTkFont(family="times new roman",size=25,weight="bold")).place(x=350,y=300)
                CTkLabel(self.admin_dashboard_you,text=f"Email\t: {data[6]}",text_color="black",font=CTkFont(family="times new roman",size=25,weight="bold")).place(x=350,y=350)
                CTkLabel(self.admin_dashboard_you,text=f"Phone\t: {data[7]}",text_color="black",font=CTkFont(family="times new roman",size=25,weight="bold")).place(x=350,y=400)
                self.admin_dashboard_you.pack(pady=25,side=LEFT)
            finally:conn.close()

    def admin_home(self):
        if self.admin_login_name == "":
            messagebox.showerror("Error","Please login first !!!")
            return
        self.delete_previous_functions()
        self.admin_dashboard_home = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
        search_type = CTkComboBox(self.admin_dashboard_home,values=["Select Search Type","Search By Name","Search By Class","Search By Roll no","Search By Field","Search By Gender"],font=CTkFont(family="times new roman",size=25),width=250,height=40,fg_color="white",text_color="black",button_hover_color="green2")
        search_type.place(x=25,y=25)
        search_type.bind("<Enter>",lambda event:search_type.configure(border_color="green2"))
        search_type.bind("<Leave>",lambda event:search_type.configure(border_color="black"))
        data_entry = CTkEntry(self.admin_dashboard_home,placeholder_text="Enter data",placeholder_text_color="gray",font=CTkFont(family="times new roman",size=25),width=250,height=40,fg_color="white",text_color="black")
        data_entry.place(x=285,y=25)
        data_entry.bind("<Enter>",lambda event:data_entry.configure(border_color="green2"))
        data_entry.bind("<Leave>",lambda event:data_entry.configure(border_color="black"))
        CTkButton(self.admin_dashboard_home,text="🔍Search",font=CTkFont(family="times new roman",size=25),width=0,height=40,fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=lambda:self.show_data(search_type.get(),data_entry.get())).place(x=545,y=25)
        CTkButton(self.admin_dashboard_home,text="📤Export data",font=CTkFont(family="times new roman",size=25),width=0,height=40,fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.export_data).place(x=810,y=25)
        CTkButton(self.admin_dashboard_home,text="🤙Connect on WhatsApp",font=CTkFont(family="times new roman",size=25),width=0,height=40,fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.connect_on_whatsapp).place(x=220,y=545)
        CTkButton(self.admin_dashboard_home,text="🔑Login into Account",font=CTkFont(family="times new roman",size=25),width=0,height=40,fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.login_into_account).place(x=570,y=545)

        records_frame = CTkFrame(self.admin_dashboard_home,width=980,height=450,border_width=2,border_color="green",fg_color="white",corner_radius=5)
        scrollBarX = CTkScrollbar(records_frame,orientation=HORIZONTAL,width=980,button_color="green",button_hover_color="green2")
        scrollBarY = CTkScrollbar(records_frame,orientation=VERTICAL,height=445,button_color="green",button_hover_color="green2")
        self.records = ttk.Treeview(records_frame,columns=("Reg. No","Name","DOB","Gender","Class","Field","Roll no","Email","Phone","Password","Father's Name","Father's Occupation","Father's Phone","Mother's Name","Mother's Occupation","Mother's Phone","Registration Date & Time"),xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)
        scrollBarX.configure(command=self.records.xview)
        scrollBarY.configure(command=self.records.yview)
        scrollBarX.pack(side=BOTTOM,fill=X)
        scrollBarY.pack(side=RIGHT,fill=Y)

        self.records.heading("Reg. No",text="Reg. No")
        self.records.heading("Name",text="Name")
        self.records.heading("DOB",text="DOB")
        self.records.heading("Gender",text="Gender")
        self.records.heading("Class",text="Class")
        self.records.heading("Field",text="Field")
        self.records.heading("Roll no",text="Roll no")
        self.records.heading("Email",text="Email")
        self.records.heading("Phone",text="Phone")
        self.records.heading("Password",text="Password")
        self.records.heading("Father's Name",text="Father's Name")
        self.records.heading("Father's Occupation",text="Father's Occupation")
        self.records.heading("Father's Phone",text="Father's Phone")
        self.records.heading("Mother's Name",text="Mother's Name")
        self.records.heading("Mother's Occupation",text="Mother's Occupation")
        self.records.heading("Mother's Phone",text="Mother's Phone")
        self.records.heading("Registration Date & Time",text="Registration Date & Time")

        self.records.column("#0",width=0,stretch=NO)
        self.records.column("Reg. No",width=100,anchor=CENTER)
        self.records.column("Name",width=200,anchor=CENTER)
        self.records.column("DOB",width=100,anchor=CENTER)
        self.records.column("Gender",width=100,anchor=CENTER)
        self.records.column("Class",width=100,anchor=CENTER)
        self.records.column("Field",width=200,anchor=CENTER)
        self.records.column("Roll no",width=200,anchor=CENTER)
        self.records.column("Email",width=200,anchor=CENTER)
        self.records.column("Phone",width=150,anchor=CENTER)
        self.records.column("Password",width=150,anchor=CENTER)
        self.records.column("Father's Name",width=200,anchor=CENTER)
        self.records.column("Father's Occupation",width=250,anchor=CENTER)
        self.records.column("Father's Phone",width=200,anchor=CENTER)
        self.records.column("Mother's Name",width=200,anchor=CENTER)
        self.records.column("Mother's Occupation",width=250,anchor=CENTER)
        self.records.column("Mother's Phone",width=200,anchor=CENTER)
        self.records.column("Registration Date & Time",width=300,anchor=CENTER)
        self.records.place(x=2,y=2,width=1210,height=560)
        records_frame.place(x=10,y=80)

        style = ttk.Style()
        style.configure("Treeview",rowheight=40,font=("arial",12,"bold"),background="white",fieldbackground="white")
        style.configure("Treeview.Heading",font=("arial",16,"bold"),foreground="black")
        self.records.configure(show="headings")
        self.admin_dashboard_home.pack(pady=25,side=LEFT)
        self.show_data(search_type="Select Search Type")

    def show_data(self,search_type = None,data_entry = None):
        if search_type == "Select Search Type":
            try:
                conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                cursor = conn.cursor()
                query = "SELECT * FROM student_data"
                cursor.execute(query)
                data = cursor.fetchall()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                self.records.delete(*self.records.get_children())
                for i in data:
                    self.records.insert("",END,values=i)
            finally:conn.close()
        elif search_type == "Search By Name":self.show_data_inner("Student_name",data_entry)
        elif search_type == "Search By Class":self.show_data_inner("Class",data_entry)
        elif search_type == "Search By Roll no":
            try:
                conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                cursor = conn.cursor()
                query = "SELECT * FROM student_data WHERE Roll_number = %s"
                cursor.execute(query,(data_entry,))
                data = cursor.fetchall()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                self.records.delete(*self.records.get_children())
                for i in data:
                    self.records.insert("",END,values=i)
            finally:conn.close()
        elif search_type == "Search By Field":self.show_data_inner("Field",data_entry)
        elif search_type == "Search By Gender":self.show_data_inner("Gender",data_entry)

    def show_data_inner(self,column,data_entry):
        try:
            conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
            cursor = conn.cursor()
            query = f"SELECT * FROM student_data WHERE {column} LIKE '{data_entry}%'"
            cursor.execute(query)
            data = cursor.fetchall()
        except Exception as e:messagebox.showerror("Error",str(e))
        else:
            self.records.delete(*self.records.get_children())
            for i in data:
                self.records.insert("",END,values=i)
        finally:conn.close()

    def export_data(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")],initialfile="student_data",title="Export Data")
        if filepath != "":
            indexing = self.records.get_children()
            # print(indexing)
            newlist = []
            for index in indexing:
                content = self.records.item(index)["values"]
                newlist.append(content)
            # print(newlist)
            table = pandas.DataFrame(newlist,columns=["Registration No","Student Name","DOB","Gender","Class","Field","Roll No","Email","Phone","Password","Father's Name","Father's Occupation","Father's Phone","Mother's Name","Mother's Occupation","Mother's Phone","Registration Date & Time"])
            table.to_csv(filepath,index=False)
            messagebox.showinfo("Success","Data is saved successfully")

    def connect_on_whatsapp(self):
        try:
            index = self.records.focus()
            phone_no = self.records.item(index)["values"][8]
            import pywhatkit
            pywhatkit.sendwhatmsg_instantly(f"+91 {phone_no}","Hi",wait_time=5)
        except IndexError:messagebox.showerror("Error","Please select any data !!!")
        except Exception as e:messagebox.showerror("Error",str(e))
        if os.path.exists("PyWhatKit_DB.txt"):os.remove("PyWhatKit_DB.txt")
        
    def login_into_account(self):
        try:
            index = self.records.focus()
            user_name,password = self.records.item(index)["values"][1],self.records.item(index)["values"][9]
            self.login_type.set("Student")
            self.user_entry.delete(0,END)
            self.user_entry.insert(0,user_name)
            self.pass_entry.delete(0,END)
            self.pass_entry.insert(0,password)
            self.login()
            self.student_account = True
        except IndexError:messagebox.showerror("Error","Please select any data !!!")
        except Exception as e:messagebox.showerror("Error",str(e))
    
    def back_to_admin_panel(self):
        try:
            if self.student_account == True:
                self.student_account = False
                self.login_type.set("Admin")
                self.user_entry.delete(0,END)
                self.user_entry.insert(0,self.admin_login_name)
                self.pass_entry.delete(0,END)
                self.pass_entry.insert(0,self.admin_login_password)
                self.login()
        except:messagebox.showwarning("Warning","This functionality for Admin only !!!")

    def save_qr(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG","*.png")],initialfile="QR",title="Save QR")
        if filepath != "":
            shutil.copy("temp_qr.png",filepath)
            messagebox.showinfo("Success","QR Saved Successfully !!!")

    def whatsapp_qr(self,name,phone):
        try:
            import pywhatkit
            pywhatkit.sendwhats_image(f"+91 {phone}","temp_qr.png",wait_time=25,caption=f"{name} QR Code")
            if os.path.exists("PyWhatKit_DB.txt"):os.remove("PyWhatKit_DB.txt")
        except Exception as e: messagebox.showerror("Error",str(e))

    def generate_id_card(self):
        if self.student_login_name == "" and self.admin_login_name == "":
            messagebox.showerror("Error","Please login first !!!")
            return
        card = Image.open("images/id_card.jpg") if self.tabview.get() == "Student Dashboard" else Image.open("images/admin_card.jpg")
        college_logo = Image.open("images/college_logo.jpg")
        card.paste(college_logo,(695,85))
        conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
        cursor = conn.cursor()
        if self.tabview.get() == "Student Dashboard":
            try:
                query = "SELECT Student_name,Father_name,Mother_name,Roll_number,DOB,Gender,Class,Phone_number,Email FROM student_data WHERE Student_name = %s and Password = %s"
                cursor.execute(query,(self.student_login_name,self.student_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                student_pic = Image.open(f"Student Images/{data[0]}{data[3]}.jpg")
                student_qr = Image.open("temp_qr.png")
                card.paste(student_pic,(10,155))
                card.paste(student_qr,(645,240))
                draw = ImageDraw.Draw(card)
                draw.text((230,170),"Name\nFather's Name\nMother's Name\nRoll number\nD.O.B\nGender\nClass\nPhone\nEmail","black",spacing=15,font=ImageFont.truetype("arial.ttf", 20))
                draw.text((380,170),f": {data[0]}\n: {data[1]}\n: {data[2]}\n: {data[3]}\n: {data[4]}\n: {data[5]}\n: {data[6]}\n: {data[7]}\n: {data[8]}","black",spacing=15,font=ImageFont.truetype("arial.ttf", 20))
                self.id_card = card
                student_pic.close()
                student_qr.close()
                # ============================== id card frame ===============================
                self.delete_previous_functions()
                self.id_card_outer_frame = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                id_card_inner_frame = CTkFrame(self.id_card_outer_frame,width=594,height=380,border_color="black",border_width=3,bg_color="white",corner_radius=5)
                CTkLabel(id_card_inner_frame,image=CTkImage(dark_image=card,light_image=card,size=(588,373)),text="").place(x=3,y=3)
                id_card_inner_frame.place(x=200,y=25)
                CTkButton(self.id_card_outer_frame,text="📩 Save",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.save_id_card).place(x=220,y=450)
                CTkButton(self.id_card_outer_frame,text="🖨 Print",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.print_id_card).place(x=420,y=450)
                CTkButton(self.id_card_outer_frame,text="📱 WhatsApp",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=lambda:self.whatsapp_id_card(data[0],data[7])).place(x=620,y=450)
                self.id_card_outer_frame.pack(pady=25,side=LEFT)
            finally:conn.close()
        elif self.tabview.get() == "Admin Dashboard":
            try:
                query = "SELECT Admin_name,DOB,Gender,Education,Phone_number,Email FROM admin_data WHERE Admin_name = %s and Password = %s"
                cursor.execute(query,(self.admin_login_name,self.admin_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                admin_pic = Image.open(f"Admin Images/{data[0]}{data[4]}.jpg")
                admin_qr = Image.open("temp_qr.png")
                card.paste(admin_pic,(10,155))
                card.paste(admin_qr,(645,240))
                draw = ImageDraw.Draw(card)
                draw.text((230,170),"Name\nD.O.B\nGender\nEducation\nPhone number\nEmail","black",spacing=15,font=ImageFont.truetype("arial.ttf", 20))
                draw.text((380,170),f": {data[0]}\n: {data[1]}\n: {data[2]}\n: {data[3]}\n: {data[4]}\n: {data[5]}","black",spacing=15,font=ImageFont.truetype("arial.ttf", 20))
                self.id_card = card
                admin_pic.close()
                admin_qr.close()
                # ============================== id card frame ===============================
                self.delete_previous_functions()
                self.admin_card_outer_frame = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                id_card_inner_frame = CTkFrame(self.admin_card_outer_frame,width=594,height=380,border_color="black",border_width=3,bg_color="white",corner_radius=5)
                CTkLabel(id_card_inner_frame,image=CTkImage(dark_image=card,light_image=card,size=(588,373)),text="").place(x=3,y=3)
                id_card_inner_frame.place(x=200,y=25)
                CTkButton(self.admin_card_outer_frame,text="📩 Save",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.save_id_card).place(x=220,y=450)
                CTkButton(self.admin_card_outer_frame,text="🖨 Print",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.print_id_card).place(x=420,y=450)
                CTkButton(self.admin_card_outer_frame,text="📱 WhatsApp",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=lambda:self.whatsapp_id_card(data[0],data[4])).place(x=620,y=450)
                self.admin_card_outer_frame.pack(pady=25,side=LEFT)
            finally:conn.close()

    def save_id_card(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".jpg",filetypes=[("JPG","*.jpg")],initialfile="ID_card",title="Save ID Card")
        if filepath != "":
            self.id_card.save(filepath)
            messagebox.showinfo("Success","ID Card Saved Successfully !!!")

    def print_id_card(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            self.id_card.save(f.name)
        os.startfile(f.name, "print")

    def whatsapp_id_card(self,name,phone_number):
        self.id_card.save("temp.jpg")
        try:
            import pywhatkit
            pywhatkit.sendwhats_image(f"+91 {phone_number}","temp.jpg",wait_time=25,caption=f"{name} ID Card")
        except Exception as e:messagebox.showerror("Error",str(e))
        os.remove("temp.jpg")
        if os.path.exists("PyWhatKit_DB.txt"):os.remove("PyWhatKit_DB.txt")

    def edit_password(self):
        if self.student_login_name == "" and self.admin_login_name == "":
            messagebox.showerror("Error","Login first !!!")
            return
        if self.tabview.get() == "Student Dashboard":
            self.delete_previous_functions()
            self.edit_password_frame = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
            CTkLabel(self.edit_password_frame,text=f"Current Password : {self.student_login_password}",font=CTkFont(family="times new roman",size=40,weight="bold"),text_color="black").place(x=180,y=30)
            CTkLabel(self.edit_password_frame,text="Set New Password",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True),text_color="black").place(x=30,y=120)
            CTkLabel(self.edit_password_frame,text="Enter New Password : ",font=CTkFont(family="times new roman",size=25,weight="bold"),text_color="black").place(x=120,y=180)
            enter_new_password = CTkEntry(self.edit_password_frame,placeholder_text="Enter New Password",placeholder_text_color="gray",text_color="black",width=300,height=40,font=CTkFont(family="times new roman",size=20),corner_radius=10,border_color="green",border_width=2,fg_color="white")
            enter_new_password.place(x=400,y=175)
            CTkLabel(self.edit_password_frame,text="Re-Enter New Password : ",font=CTkFont(family="times new roman",size=25,weight="bold"),text_color="black").place(x=120,y=240)
            re_enter_new_password = CTkEntry(self.edit_password_frame,placeholder_text="Re-Enter Your Password",placeholder_text_color="gray",text_color="black",width=300,height=40,font=CTkFont(family="times new roman",size=20),show="*",corner_radius=10,border_color="green",border_width=2,fg_color="white")
            re_enter_new_password.place(x=400,y=235)
            CTkButton(self.edit_password_frame,text="Save",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=lambda:self.edit_password_inner(enter_new_password.get(),re_enter_new_password.get())).place(x=350,y=320)
            self.edit_password_frame.pack(pady=25,side=LEFT)
        else:
            self.delete_previous_functions()
            self.admin_edit_password_frame = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
            CTkLabel(self.admin_edit_password_frame,text=f"Current Password : {self.admin_login_password}",font=CTkFont(family="times new roman",size=40,weight="bold"),text_color="black").place(x=180,y=30)
            CTkLabel(self.admin_edit_password_frame,text="Set New Password",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True),text_color="black").place(x=30,y=120)
            CTkLabel(self.admin_edit_password_frame,text="Enter New Password : ",font=CTkFont(family="times new roman",size=25,weight="bold"),text_color="black").place(x=120,y=180)
            enter_new_password = CTkEntry(self.admin_edit_password_frame,placeholder_text="Enter New Password",placeholder_text_color="gray",text_color="black",width=300,height=40,font=CTkFont(family="times new roman",size=20),corner_radius=10,border_color="green",border_width=2,fg_color="white")
            enter_new_password.place(x=400,y=175)
            CTkLabel(self.admin_edit_password_frame,text="Re-Enter New Password : ",font=CTkFont(family="times new roman",size=25,weight="bold"),text_color="black").place(x=120,y=240)
            re_enter_new_password = CTkEntry(self.admin_edit_password_frame,placeholder_text="Re-Enter Your Password",placeholder_text_color="gray",text_color="black",width=300,height=40,font=CTkFont(family="times new roman",size=20),show="*",corner_radius=10,border_color="green",border_width=2,fg_color="white")
            re_enter_new_password.place(x=400,y=235)
            CTkButton(self.admin_edit_password_frame,text="Save",width=150,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=lambda:self.edit_password_inner(enter_new_password.get(),re_enter_new_password.get())).place(x=350,y=320)
            self.admin_edit_password_frame.pack(pady=25,side=LEFT)
        
    def edit_password_inner(self,new_password,re_enter_new_password):
        if new_password == re_enter_new_password and new_password != "":
            conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
            cursor = conn.cursor()
            if self.tabview.get() == "Student Dashboard":
                try:
                    query = "UPDATE student_data SET Password = %s WHERE Student_name = %s AND Password = %s"
                    cursor.execute(query,(new_password,self.student_login_name,self.student_login_password))
                    conn.commit()
                except Exception as e:messagebox.showerror("Error",str(e))
                else:
                    messagebox.showinfo("Success","Password changed successfully !!!")
                    self.student_login_password = new_password
                    self.edit_password()
                finally:conn.close()
            else:
                try:
                    query = "UPDATE admin_data SET Password = %s WHERE Admin_name = %s AND Password = %s"
                    cursor.execute(query,(new_password,self.admin_login_name,self.admin_login_password))
                    conn.commit()
                except Exception as e:messagebox.showerror("Error",str(e))
                else:
                    messagebox.showinfo("Success","Password changed successfully !!!")
                    self.admin_login_password = new_password
                    self.admin_edit_password_frame.destroy()
                    self.edit_password()
                finally:conn.close()
        else:messagebox.showerror("Error","Password doesn't match !!!")
        
    def edit_profile(self):
        if self.student_login_name == "" and self.admin_login_name == "":
            messagebox.showerror("Error","Login first !!!")
            return
        if self.tabview.get() == "Student Dashboard":
            self.delete_previous_functions()
            self.edit_profile_frame = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)

            # === Student Update Details section ===
            CTkLabel(self.edit_profile_frame,text="Student Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=140,y=25)

            CTkLabel(self.edit_profile_frame,text="Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=100)
            self.name_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter your name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.name_entry_update.place(x=170,y=95)
            self.name_entry_update.bind("<Enter>",lambda event:self.name_entry_update.configure(border_color="green2"))
            self.name_entry_update.bind("<Leave>",lambda event:self.name_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="D.O.B*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=150)
            self.dob_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="DD/MM/YYYY",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10,state="readonly")
            self.dob_entry_update.place(x=170,y=145)
            CTkButton(self.edit_profile_frame,text="get",height=40,width=10,fg_color="green",hover_color="green2",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),border_color="black",border_width=2,command=self.getDate).place(x=380,y=145)
            self.dob_entry_update.bind("<Enter>",lambda event:self.dob_entry_update.configure(border_color="green2"))
            self.dob_entry_update.bind("<Leave>",lambda event:self.dob_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Gender*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=200)
            self.gender_entry_update = StringVar(value = "")
            CTkRadioButton(self.edit_profile_frame,variable=self.gender_entry_update,text="Male",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Male",hover_color="green2").place(x=170,y=195)
            CTkRadioButton(self.edit_profile_frame,variable=self.gender_entry_update,text="Female",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Female",hover_color="green2").place(x=270,y=195)
            
            CTkLabel(self.edit_profile_frame,text="Class*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=250)
            self.class_entry_update = CTkComboBox(self.edit_profile_frame,values=["Select Class","B.Tech - I", "B.Tech - II", "B.Tech - III", "B.Tech - IV","M.Tech - I", "M.Tech - II"],font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10,state="readonly")
            self.class_entry_update.place(x=170,y=245)
            self.class_entry_update.set("Select Class")
            self.class_entry_update.bind("<Enter>",lambda event:self.class_entry_update.configure(border_color="green2"))
            self.class_entry_update.bind("<Leave>",lambda event:self.class_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Field*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=300)
            self.field_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter your field",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.field_entry_update.place(x=170,y=295)
            self.field_entry_update.bind("<Enter>",lambda event:self.field_entry_update.configure(border_color="green2"))
            self.field_entry_update.bind("<Leave>",lambda event:self.field_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Roll no.*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=350)
            self.roll_no_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter your Roll no",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.roll_no_entry_update.place(x=170,y=345)
            self.roll_no_entry_update.bind("<Enter>",lambda event:self.roll_no_entry_update.configure(border_color="green2"))
            self.roll_no_entry_update.bind("<Leave>",lambda event:self.roll_no_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Email*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=400)
            self.email_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter your email",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.email_entry_update.place(x=170,y=395)
            self.email_entry_update.bind("<Enter>",lambda event:self.email_entry_update.configure(border_color="green2"))
            self.email_entry_update.bind("<Leave>",lambda event:self.email_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Phone*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=70,y=450)
            self.phone_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter your phone",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.phone_entry_update.place(x=170,y=445)
            self.phone_entry_update.bind("<Enter>",lambda event:self.phone_entry_update.configure(border_color="green2"))
            self.phone_entry_update.bind("<Leave>",lambda event:self.phone_entry_update.configure(border_color="black"))

            # === Parent Update details section ===
            CTkLabel(self.edit_profile_frame,text="Parent Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=590,y=25)

            CTkLabel(self.edit_profile_frame,text="Father's Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=500,y=100)
            self.father_name_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter your father's name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.father_name_entry_update.place(x=675,y=95)
            self.father_name_entry_update.bind("<Enter>",lambda event:self.father_name_entry_update.configure(border_color="green2"))
            self.father_name_entry_update.bind("<Leave>",lambda event:self.father_name_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Father's occupation",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=500,y=150)
            self.father_occupation_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter occupation",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.father_occupation_entry_update.place(x=675,y=145)
            self.father_occupation_entry_update.bind("<Enter>",lambda event:self.father_occupation_entry_update.configure(border_color="green2"))
            self.father_occupation_entry_update.bind("<Leave>",lambda event:self.father_occupation_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Father's phone",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=500,y=200)
            self.father_phone_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter phone number",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.father_phone_entry_update.place(x=675,y=195)
            self.father_phone_entry_update.bind("<Enter>",lambda event:self.father_phone_entry_update.configure(border_color="green2"))
            self.father_phone_entry_update.bind("<Leave>",lambda event:self.father_phone_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Mother's Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=500,y=250)
            self.mother_name_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter your mother's name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.mother_name_entry_update.place(x=675,y=245)
            self.mother_name_entry_update.bind("<Enter>",lambda event:self.mother_name_entry_update.configure(border_color="green2"))
            self.mother_name_entry_update.bind("<Leave>",lambda event:self.mother_name_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Mother's occupation",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=500,y=300)
            self.mother_occupation_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter occupation",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.mother_occupation_entry_update.place(x=675,y=295)
            self.mother_occupation_entry_update.bind("<Enter>",lambda event:self.mother_occupation_entry_update.configure(border_color="green2"))
            self.mother_occupation_entry_update.bind("<Leave>",lambda event:self.mother_occupation_entry_update.configure(border_color="black"))

            CTkLabel(self.edit_profile_frame,text="Mother's phone",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=500,y=350)
            self.mother_phone_entry_update = CTkEntry(self.edit_profile_frame,placeholder_text="Enter phone number",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=210,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.mother_phone_entry_update.place(x=675,y=345)
            self.mother_phone_entry_update.bind("<Enter>",lambda event:self.mother_phone_entry_update.configure(border_color="green2"))
            self.mother_phone_entry_update.bind("<Leave>",lambda event:self.mother_phone_entry_update.configure(border_color="black"))

            CTkButton(self.edit_profile_frame,text="Update",width=300,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.edit_profile_update_button).place(x=540,y=450)
            self.edit_profile_frame.pack(pady=25,side=LEFT)

            # Database connection & Entry filling
            try:
                conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                cursor = conn.cursor()
                query = "SELECT * FROM student_data WHERE Student_name = %s AND Password = %s"
                cursor.execute(query,(self.student_login_name,self.student_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                if data:
                    self.name_entry_update.delete(0,END)
                    self.name_entry_update.insert(0,data[1])
                    self.dob_entry_update.configure(state="normal")
                    self.dob_entry_update.delete(0,END)
                    self.dob_entry_update.insert(0,datetime.datetime.strptime(str(data[2]), '%Y-%m-%d').strftime('%d/%m/%Y'))
                    self.dob_entry_update.configure(state="readonly")
                    self.gender_entry_update.set(data[3])
                    self.class_entry_update.set(data[4])
                    self.field_entry_update.delete(0,END)
                    self.field_entry_update.insert(0,data[5])
                    self.roll_no_entry_update.delete(0,END)
                    self.roll_no_entry_update.insert(0,data[6])
                    self.email_entry_update.delete(0,END)
                    self.email_entry_update.insert(0,data[7])
                    self.phone_entry_update.delete(0,END)
                    self.phone_entry_update.insert(0,data[8])
                    self.father_name_entry_update.delete(0,END)
                    self.father_name_entry_update.insert(0,data[10])
                    self.father_occupation_entry_update.delete(0,END)
                    self.father_occupation_entry_update.insert(0,data[11] if data[11] != None else "")
                    self.father_phone_entry_update.delete(0,END)
                    self.father_phone_entry_update.insert(0,data[12] if data[12] != None else "")
                    self.mother_name_entry_update.delete(0,END)
                    self.mother_name_entry_update.insert(0,data[13])
                    self.mother_occupation_entry_update.delete(0,END)
                    self.mother_occupation_entry_update.insert(0,data[14] if data[14] != None else "")
                    self.mother_phone_entry_update.delete(0,END)
                    self.mother_phone_entry_update.insert(0,data[15] if data[15] != None else "")
            finally:conn.close()
        else:
            self.delete_previous_functions()
            self.admin_edit_profile_frame = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
            # === admin Details section ===
            CTkLabel(self.admin_edit_profile_frame,text="Admin Details",text_color="black",font=CTkFont(family="times new roman",size=30,weight="bold",underline=True)).place(x=400,y=25)

            CTkLabel(self.admin_edit_profile_frame,text="Name*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=310,y=100)
            self.admin_name_entry_update = CTkEntry(self.admin_edit_profile_frame,placeholder_text="Enter your name",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.admin_name_entry_update.place(x=430,y=95)
            self.admin_name_entry_update.bind("<Enter>",lambda event:self.admin_name_entry_update.configure(border_color="green2"))
            self.admin_name_entry_update.bind("<Leave>",lambda event:self.admin_name_entry_update.configure(border_color="black"))

            CTkLabel(self.admin_edit_profile_frame,text="D.O.B*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=310,y=150)
            self.admin_dob_entry_update = CTkEntry(self.admin_edit_profile_frame,placeholder_text="DD/MM/YYYY",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10,state="readonly")
            self.admin_dob_entry_update.place(x=430,y=145)
            CTkButton(self.admin_edit_profile_frame,text="get",height=40,width=10,fg_color="green",hover_color="green2",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold"),border_color="black",border_width=2,command=self.getDate).place(x=640,y=145)
            self.admin_dob_entry_update.bind("<Enter>",lambda event:self.admin_dob_entry_update.configure(border_color="green2"))
            self.admin_dob_entry_update.bind("<Leave>",lambda event:self.admin_dob_entry_update.configure(border_color="black"))

            CTkLabel(self.admin_edit_profile_frame,text="Gender*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=310,y=200)
            self.admin_gender_entry_update = StringVar(value = "")
            CTkRadioButton(self.admin_edit_profile_frame,variable=self.admin_gender_entry_update,text="Male",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Male",hover_color="green2").place(x=430,y=195)
            CTkRadioButton(self.admin_edit_profile_frame,variable=self.admin_gender_entry_update,text="Female",text_color="black",font=CTkFont(family="times new roman",size=18),width=100,height=40,value="Female",hover_color="green2").place(x=530,y=195)
            
            CTkLabel(self.admin_edit_profile_frame,text="Education*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=310,y=250)
            self.admin_education_entry_update = CTkEntry(self.admin_edit_profile_frame,placeholder_text="Enter your education",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.admin_education_entry_update.place(x=430,y=245)
            self.admin_education_entry_update.bind("<Enter>",lambda event:self.admin_education_entry_update.configure(border_color="green2"))
            self.admin_education_entry_update.bind("<Leave>",lambda event:self.admin_education_entry_update.configure(border_color="black"))

            CTkLabel(self.admin_edit_profile_frame,text="Field*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=310,y=300)
            self.admin_field_entry_update = CTkEntry(self.admin_edit_profile_frame,placeholder_text="Enter your field",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.admin_field_entry_update.place(x=430,y=295)
            self.admin_field_entry_update.bind("<Enter>",lambda event:self.admin_field_entry_update.configure(border_color="green2"))
            self.admin_field_entry_update.bind("<Leave>",lambda event:self.admin_field_entry_update.configure(border_color="black"))

            CTkLabel(self.admin_edit_profile_frame,text="Email*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=310,y=350)
            self.admin_email_entry_update = CTkEntry(self.admin_edit_profile_frame,placeholder_text="Enter your email",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.admin_email_entry_update.place(x=430,y=345)
            self.admin_email_entry_update.bind("<Enter>",lambda event:self.admin_email_entry_update.configure(border_color="green2"))
            self.admin_email_entry_update.bind("<Leave>",lambda event:self.admin_email_entry_update.configure(border_color="black"))

            CTkLabel(self.admin_edit_profile_frame,text="Phone*",text_color="black",font=CTkFont(family="times new roman",size=20,weight="bold")).place(x=310,y=400)
            self.admin_phone_entry_update = CTkEntry(self.admin_edit_profile_frame,placeholder_text="Enter your phone",placeholder_text_color="black",font=CTkFont(family="times new roman",size=18),width=250,height=40,fg_color="white",text_color="blue",border_color="black",corner_radius=10)
            self.admin_phone_entry_update.place(x=430,y=395)
            self.admin_phone_entry_update.bind("<Enter>",lambda event:self.admin_phone_entry_update.configure(border_color="green2"))
            self.admin_phone_entry_update.bind("<Leave>",lambda event:self.admin_phone_entry_update.configure(border_color="black"))

            CTkButton(self.admin_edit_profile_frame,text="Update",width=300,height=40,font=CTkFont(family="times new roman",size=25),fg_color="green",hover_color="green2",text_color="black",corner_radius=10,command=self.edit_profile_update_button).place(x=350,y=520)
            self.admin_edit_profile_frame.pack(pady=25,side=LEFT)

            # Database connection & Entry filling
            try:
                conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                cursor = conn.cursor()
                query = "SELECT * FROM admin_data WHERE Admin_name = %s and Password = %s"
                cursor.execute(query,(self.admin_login_name,self.admin_login_password))
                data = cursor.fetchone()
            except Exception as e:messagebox.showerror("Error",str(e))
            else:
                if data:
                    self.admin_name_entry_update.delete(0,END)
                    self.admin_name_entry_update.insert(0,data[1])
                    self.admin_dob_entry_update.configure(state="normal")
                    self.admin_dob_entry_update.delete(0,END)
                    self.admin_dob_entry_update.insert(0,datetime.datetime.strptime(str(data[2]), '%Y-%m-%d').strftime('%d/%m/%Y'))
                    self.admin_dob_entry_update.configure(state="readonly")
                    self.admin_gender_entry_update.set(data[3])
                    self.admin_education_entry_update.delete(0,END)
                    self.admin_education_entry_update.insert(0,data[4])
                    self.admin_field_entry_update.delete(0,END)
                    self.admin_field_entry_update.insert(0,data[5])
                    self.admin_email_entry_update.delete(0,END)
                    self.admin_email_entry_update.insert(0,data[6])
                    self.admin_phone_entry_update.delete(0,END)
                    self.admin_phone_entry_update.insert(0,data[7])
            finally:conn.close()

    def edit_profile_update_button(self):
        if self.tabview.get() == "Student Dashboard":
            if self.name_entry_update.get() != "" and self.dob_entry_update.get() != "" and self.gender_entry_update.get() != "" and self.class_entry_update.get() != "Select Class" and self.field_entry_update.get() != "" and self.roll_no_entry_update.get() != "" and self.phone_entry_update.get() != "" and self.email_entry_update.get() != "" and self.father_name_entry_update.get() != "" and self.mother_name_entry_update.get() != "":
                if self.email_entry_update.get().endswith("@gmail.com") and self.email_entry_update.get().count(" ") == 0:
                    if self.phone_entry_update.get().isdigit() and len(self.phone_entry_update.get()) == 10 and ((self.father_phone_entry_update.get().isdigit() and len(self.father_phone_entry_update.get()) == 10) or self.father_phone_entry_update.get() == "") and ((self.mother_phone_entry_update.get().isdigit() and len(self.mother_phone_entry_update.get()) == 10) or self.mother_phone_entry_update.get() == ""):
                        # Database connectivity for student data updation
                        conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                        cursor = conn.cursor()
                        try:
                            query = "UPDATE student_data SET Student_name = %s, DOB = %s, Gender = %s, Class = %s, Field = %s, Roll_number = %s, Email = %s, Phone_number = %s, Father_name = %s, Father_occupation = %s, Father_phone = %s, Mother_name = %s, Mother_occupation = %s, Mother_phone = %s WHERE Student_name = %s AND Password = %s"
                            cursor.execute(query,(self.name_entry_update.get(),datetime.datetime.strptime(self.dob_entry_update.get(), '%d/%m/%Y').strftime('%Y-%m-%d'),self.gender_entry_update.get(),self.class_entry_update.get(),self.field_entry_update.get(),self.roll_no_entry_update.get(),self.email_entry_update.get(),self.phone_entry_update.get(),self.father_name_entry_update.get(),self.father_occupation_entry_update.get() if self.father_occupation_entry_update.get() != "" else None,self.father_phone_entry_update.get() if self.father_phone_entry_update.get() != "" else None,self.mother_name_entry_update.get(),self.mother_occupation_entry_update.get() if self.mother_occupation_entry_update.get() != "" else None,self.mother_phone_entry_update.get() if self.mother_phone_entry_update.get() != "" else None,self.student_login_name,self.student_login_password))
                            conn.commit()
                        except Exception as e:messagebox.showerror("Error",str(e))
                        else:
                            self.student_login_name = self.name_entry_update.get()
                            messagebox.showinfo("Success","Updation Successful !!!")
                            self.edit_profile()
                        finally:conn.close()
                    else:messagebox.showerror("Error","Please enter a valid phone number !!!")
                else:messagebox.showerror("Error","Please enter a valid email address !!!")
            else:messagebox.showerror("Error","All fields are required !!!")
        elif self.tabview.get() == "Admin Dashboard":
            if self.admin_name_entry_update.get() != "" and self.admin_dob_entry_update.get() != "" and self.admin_gender_entry_update.get() != "" and self.admin_education_entry_update.get() != "" and self.admin_field_entry_update.get() != "" and self.admin_phone_entry_update.get() != "" and self.admin_email_entry_update.get() != "":
                if self.admin_email_entry_update.get().endswith("@gmail.com") and self.admin_email_entry_update.get().count(" ") == 0:
                    if self.admin_phone_entry_update.get().isdigit() and len(self.admin_phone_entry_update.get()) == 10:
                        # Database Connectivity for admin data updation
                        conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
                        cursor = conn.cursor()
                        try:
                            query = "UPDATE admin_data SET Admin_name = %s, DOB = %s, Gender = %s, Education = %s, Field = %s, Email = %s, Phone_number = %s WHERE Admin_name = %s AND Password = %s"
                            cursor.execute(query,(self.admin_name_entry_update.get(),datetime.datetime.strptime(self.admin_dob_entry_update.get(),"%d/%m/%Y").strftime("%Y-%m-%d"),self.admin_gender_entry_update.get(),self.admin_education_entry_update.get(),self.admin_field_entry_update.get(),self.admin_email_entry_update.get(),self.admin_phone_entry_update.get(),self.admin_login_name,self.admin_login_password))
                            conn.commit()
                        except Exception as e:messagebox.showerror("Error",str(e))
                        else:
                            self.admin_login_name = self.admin_name_entry_update.get()
                            messagebox.showinfo("Success","Updation Successful !!!")
                            self.edit_profile()
                        finally:conn.close()
                    else:messagebox.showerror("Error","Please enter a valid phone number !!!")
                else:messagebox.showerror("Error","Please enter a valid email address !!!")
            else:messagebox.showerror("Error","All fields are required !!!")

    def chat_ai(self):
        if self.student_login_name == "" and self.admin_login_name == "":
            messagebox.showerror("Error","Please login first !!!")
            return
        try:
            import pywhatkit
        except Exception as e:messagebox.showerror("Error",str(e))
        else:
            if self.tabview.get() == "Student Dashboard":
                self.delete_previous_functions()
                self.chat_ai_frame = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                self.chat_frame = CTkTextbox(self.chat_ai_frame,width=960,height=490,font=CTkFont(family="times new roman",size=20),text_color="black",border_width=2,border_color="green",fg_color="white",corner_radius=10,scrollbar_button_color="green",scrollbar_button_hover_color="green2")
                self.chat_frame.place(x=20,y=20)
                self.chat_frame.configure(state="disabled")
                self.chat_frame.bind("<Enter>",lambda event:self.chat_frame.configure(border_color="green2"))
                self.chat_frame.bind("<Leave>",lambda event:self.chat_frame.configure(border_color="green"))
                self.user_msg = CTkEntry(self.chat_ai_frame,width=880,height=40,placeholder_text="Hello, How can I help you ?",placeholder_text_color="gray",text_color="black",font=CTkFont(family="times new roman",size=25),border_color="green",border_width=2,fg_color="white",corner_radius=20)
                self.user_msg.place(x=20,y=530)
                self.user_msg.bind("<Enter>",lambda event:self.user_msg.configure(border_color="green2"))
                self.user_msg.bind("<Leave>",lambda event:self.user_msg.configure(border_color="green"))
                CTkButton(self.chat_ai_frame,text="⬆",width=0,height=40,font=CTkFont(family="times new roman",size=25,weight="bold"),text_color="black",border_color="green",border_width=2,fg_color="white",corner_radius=30,hover_color="green2",command=self.send_to_gemini).place(x=920,y=530)
                self.chat_ai_frame.pack(pady=25,side=LEFT)
                self.user_msg.bind("<Return>",lambda event:self.send_to_gemini())
            elif self.tabview.get() == "Admin Dashboard":
                self.delete_previous_functions()
                self.admin_chat_ai_frame = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                self.admin_chat_frame = CTkTextbox(self.admin_chat_ai_frame,width=960,height=490,font=CTkFont(family="times new roman",size=20),text_color="black",border_width=2,border_color="green",fg_color="white",corner_radius=10,scrollbar_button_color="green",scrollbar_button_hover_color="green2")
                self.admin_chat_frame.place(x=20,y=20)
                self.admin_chat_frame.configure(state="disabled")
                self.admin_chat_frame.bind("<Enter>",lambda event:self.admin_chat_frame.configure(border_color="green2"))
                self.admin_chat_frame.bind("<Leave>",lambda event:self.admin_chat_frame.configure(border_color="green"))
                self.admin_msg = CTkEntry(self.admin_chat_ai_frame,width=880,height=40,placeholder_text="Hello, How can I help you ?",placeholder_text_color="gray",text_color="black",font=CTkFont(family="times new roman",size=25),border_color="green",border_width=2,fg_color="white",corner_radius=20)
                self.admin_msg.place(x=20,y=530)
                self.admin_msg.bind("<Enter>",lambda event:self.admin_msg.configure(border_color="green2"))
                self.admin_msg.bind("<Leave>",lambda event:self.admin_msg.configure(border_color="green"))
                CTkButton(self.admin_chat_ai_frame,text="⬆",width=0,height=40,font=CTkFont(family="times new roman",size=25,weight="bold"),text_color="black",border_color="green",border_width=2,fg_color="white",corner_radius=30,hover_color="green2",command=self.send_to_gemini).place(x=920,y=530)
                self.admin_chat_ai_frame.pack(pady=25,side=LEFT)
                self.admin_msg.bind("<Return>",lambda event:self.send_to_gemini())
    
    def send_to_gemini(self):
        if self.tabview.get() == "Student Dashboard":
            if self.user_msg.get() == "":
                messagebox.showerror("Error","Please enter a prompt !!!")
                return
            self.chat_frame.configure(state="normal")
            self.chat_frame.insert("end","User: "+self.user_msg.get())
            self.chat_frame.insert("end","\nChatbot: "+chat.send_message(self.chat_frame.get("1.0","end")).text.replace("\n\n","\n").replace("**","")+"\n")
            self.chat_frame.configure(state="disabled")
            self.chat_frame.see("end")
            self.user_msg.delete(0,"end")
        elif self.tabview.get() == "Admin Dashboard":
            if self.admin_msg.get() == "":
                messagebox.showerror("Error","Please enter a prompt !!!")
                return
            self.admin_chat_frame.configure(state="normal")
            self.admin_chat_frame.insert("end","User: "+self.admin_msg.get())
            self.admin_chat_frame.insert("end","\nChatbot: "+chat.send_message(self.admin_chat_frame.get("1.0","end")).text.replace("\n\n","\n").replace("**","")+"\n")
            self.admin_chat_frame.configure(state="disabled")
            self.admin_chat_frame.see("end")
            self.admin_msg.delete(0,"end")

    def delete_account(self):
        if self.student_login_name == "" and self.admin_login_name == "":
            messagebox.showerror("Error","Login first !!!")
            return
        ask = messagebox.askyesno("Delete","Are you sure you want to delete your account?")
        if ask == True:
            self.tabview.set("Login Page")
            # Delete from database
            conn = pymysql.connect(host=self.db_host,user=self.db_user,password=self.db_password,port=self.db_port,database="student_registration_and_management_system")
            cursor = conn.cursor()
            if self.login_type.get() == "Student":
                try:
                    query1 = "SELECT Student_name,Roll_number FROM student_data WHERE Student_name = %s AND Password = %s"
                    cursor.execute(query1,(self.student_login_name,self.student_login_password))
                    data = cursor.fetchone()
                    query2 = "DELETE FROM student_data WHERE Student_name = %s AND Password = %s"
                    cursor.execute(query2,(self.student_login_name,self.student_login_password))
                    conn.commit()
                except Exception as e:messagebox.showerror("Error",str(e))
                else:
                    if os.path.exists(f"Student Images/{data[0]}{data[1]}.jpg"):os.remove(f"Student Images/{data[0]}{data[1]}.jpg")
                    if os.path.exists("temp_qr.png"):os.remove("temp_qr.png")
                    messagebox.showinfo("Success","Account deleted successfully !!!")
                    self.student_login_name,self.student_login_password = "",""
                    self.delete_previous_functions()
                    self.student_dashboard_functions_show = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                    self.student_dashboard_functions_show.pack(pady=25,side=LEFT)
                finally:conn.close()
            else:
                try:
                    query1 = "SELECT Admin_name,Phone_number FROM admin_data WHERE Admin_name = %s AND Password = %s"
                    cursor.execute(query1,(self.admin_login_name,self.admin_login_password))
                    data = cursor.fetchone()
                    query2 = "DELETE FROM admin_data WHERE Admin_name = %s AND Password = %s"
                    cursor.execute(query2,(self.admin_login_name,self.admin_login_password))
                    conn.commit()
                except Exception as e:messagebox.showerror("Error",str(e))
                else:
                    if os.path.exists(f"Admin Images/{data[0]}{data[1]}.jpg"):os.remove(f"Admin Images/{data[0]}{data[1]}.jpg")
                    if os.path.exists("temp_qr.png"):os.remove("temp_qr.png")
                    messagebox.showinfo("Success","Account deleted successfully !!!")
                    self.admin_login_name,self.admin_login_password = "",""
                    self.delete_previous_functions()
                    self.admin_dashboard_functions_show = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                    self.admin_dashboard_functions_show.pack(pady=25,side=LEFT)
                finally:conn.close()

    def dashboard_logout(self):
        if self.student_login_name == "" and self.admin_login_name == "":
            messagebox.showerror("Error","Login first !!!")
            return
        ask = messagebox.askyesno("Logout","Are you sure you want to logout?")
        if ask == True:
            if self.tabview.get() == "Student Dashboard":
                self.student_login_name,self.student_login_password = "",""
                self.delete_previous_functions()
                self.student_dashboard_functions_show = CTkFrame(self.tabview.tab("Student Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                self.student_dashboard_functions_show.pack(pady=25,side=LEFT)
            elif self.tabview.get() == "Admin Dashboard":
                self.admin_login_name,self.admin_login_password = "",""
                self.delete_previous_functions()
                self.admin_dashboard_functions_show = CTkFrame(self.tabview.tab("Admin Dashboard"),width=1000,height=600,border_width=3,border_color="green",fg_color="white",corner_radius=20)
                self.admin_dashboard_functions_show.pack(pady=25,side=LEFT)
            self.tabview.set("Login Page")
            if os.path.exists("temp_qr.png"):os.remove("temp_qr.png")
    
    def delete_previous_functions(self):
        if self.tabview.get() == "Student Dashboard":
            for widget in (self.student_dashboard_functions_show,self.student_dashboard_home, self.id_card_outer_frame, self.edit_password_frame,self.edit_profile_frame,self.chat_ai_frame):
                if widget:
                    widget.destroy()
        elif self.tabview.get() == "Admin Dashboard":
            for widget in (self.admin_dashboard_functions_show,self.admin_dashboard_home,self.admin_dashboard_you,self.admin_card_outer_frame,self.admin_edit_password_frame,self.admin_edit_profile_frame,self.admin_chat_ai_frame):
                if widget:
                    widget.destroy()

if __name__ == "__main__":
    System()