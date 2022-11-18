from tkinter import *
import mysql.connector as mysqlconnector
from re import match
import tkinter.messagebox as mymessagebox
from random import randint
from smtplib import SMTP

def run():
    otp = randint(1111, 9999)
    root = Tk()
    root.geometry('510x550')
    root.title("Registration Form")
    root.resizable(False, False)

    # otp validation
    otp_validation = False
    #Make the window jump above all
    #root.attributes('-topmost',True)

    #MYSQL ConnectionString
    mydb = mysqlconnector.connect(host="192.168.56.1", user="root", password="root", database="chatroom", port=3030, autocommit=True)
    mycursor = mydb.cursor(buffered=True, dictionary=True)


    form_title = Label(root, text="Registration form",width=20,font=("bold", 20))
    name = Label(root, text="FullName",width=20,font=("bold", 10))
    nametxt = Entry(root, relief="flat", width=30)
    email = Label(root, text="Email",width=20,font=("bold", 10))
    emailtxt = Entry(root, relief="flat", width=30)
    username = Label(root, text="Username ",width=20,font=("bold", 10))
    usernametxt = Entry(root, relief="flat", width=30)
    password1 = Label(root, text="Password",width=20,font=("bold", 10))
    password1txt = Entry(root, relief="flat", width=30, show='*')
    password2 = Label(root, text="Confirm Password",width=20,font=("bold", 10))
    password2txt = Entry(root, relief="flat", width=30, show='*')
    otp_label = Label(root, text="OTP",width=20,font=("bold", 10))
    otp_entry = Entry(root, relief="flat", width=30)

    # This will send otp to the mail
    def send_otp_to_mail():
        sender = 'techtreat6@gmail.com'
        app_password = 'vpdvocjtlfcavdsu'
        receiver = emailtxt.get().strip()
        message =f'''Greetings,
                        Use the below otp to register into Chatkaro application
                        {otp}

                By,
                ChatKaro team'''

        subject = 'Registration OTP'
        msg1 = 'Subject: %s\n\n%s' % (subject, message) 
        server = SMTP("smtp.gmail.com",587)
        server.starttls()
        try:
            server.login(user= sender,password= app_password)
        except:
            print("")
            print("""check for the following:
            1. Read prerequisite section 
            2. Check app password
            3. try again and enter details carefully
            """)
        else:
            server.sendmail(from_addr= sender,to_addrs= receiver,msg= msg1)
            mymessagebox.showinfo("OTP Sent", "OTP sent successfully to your email")
            server.close()
        
    # This will check the email is valid or not
    def validate_email():
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        query = f"Select email from users where email='{emailtxt.get().strip()}'"
        mycursor.execute(query)
        if mycursor.rowcount == 0:
            if(match(regex, emailtxt.get().strip())):
                if(emailtxt.get().strip().endswith('gmail.com') or emailtxt.get().strip().endswith('yahoo.com')
                or emailtxt.get().strip().endswith('protonmail.com') or emailtxt.get().strip().endswith('outlook.com')
                or emailtxt.get().strip().endswith('icloud.com')):
                    if otp_entry.get().strip() == str(otp):
                        return True
                    else:
                        mymessagebox.showerror('OTP', 'Incorrect OTP')
        else:
            mymessagebox.showerror('email', 'Email already registered !!!')
            return False
        return False

    def validate_password():
        if password1txt.get().strip() == password2txt.get().strip():
            return True
        else:
            return False

    # register user
    def register_user():
        if(emailtxt.get().strip() != '' and nametxt.get().strip() != '' and usernametxt.get().strip() != '' 
        and password1txt.get().strip() != '' and password2txt.get().strip() != '' and otp_entry.get().strip() != ''):
            query = f"SELECT username from users where username='{usernametxt.get().strip()}'"
            mycursor.execute(query)
            if mycursor.rowcount == 0:
                if validate_email():
                    if validate_password():
                        query = "INSERT INTO users values('"+nametxt.get().strip()+"','"+emailtxt.get().strip()+"','"+usernametxt.get().strip()+"','"+password1txt.get().strip()+"'+"'1'");"
                        #query = "INSERT INTO users values('pardhu', 'pardhu9100@gmail.com', 'pardhu', 'pardhu', 1);"
                        mydb.commit()
                        mycursor.execute(query)
                        if mymessagebox.askyesno("Login?", "You are registered successfully. Do you want to login?"):
                            root.destroy()
                            import login
                            login.run()
                        print(mycursor.rowcount)
                            
                    else:
                        mymessagebox.showerror("password not matched", "Passowrd and confirm password not matched")
                else:
                    mymessagebox.showerror("Invalid email format", "Please enter valid email for further process")
            else:
                mymessagebox.showerror('User exists', 'User already exists')
        else:
            mymessagebox.showerror("Empty field", "Enter all fields")


    # method to show the password 
    def my_show():
        if(c_v1.get()==1):
            password1txt.config(show='')
        else:
            password1txt.config(show='*')

    def go_back_to_home():
        root.destroy()
        import home
        home.run()


    # Checkbox variable to get input, default value is 0
    c_v1=IntVar(value=0)
    show_password = Checkbutton(root,text='Show Password',variable=c_v1,
        onvalue=1, offvalue=0, command=my_show)

    nametxt.focus()

    registerbtn = Button(root, text='Submit', command=register_user, width=20,bg='brown',fg='white')
    HomeBtn = Button(root, text='Home', command=go_back_to_home, width=20,bg='brown',fg='white')
    get_otp_btn = Button(root, text='get otp', command=send_otp_to_mail, width=7,bg='white',fg='blue', relief='groove')

    # Place the elements on window
    form_title.place(x=90,y=53)
    name.place(x=80,y=130)
    email.place(x=68,y=180)
    username.place(x=70,y=230)
    password1.place(x=72, y=280)
    password2.place(x=80, y=370)

    nametxt.place(x=240,y=130)
    emailtxt.place(x=240,y=180)
    usernametxt.place(x=240,y=230)
    password1txt.place(x=240, y=280)
    show_password.place(x=250, y=320)
    password2txt.place(x=240, y=370)

    otp_label.place(x=80, y=420)
    otp_entry.place(x=240, y=420)
    get_otp_btn.place(x=400, y=420)

    registerbtn.place(x=250,y=480)
    HomeBtn.place(x=50, y=480)

    root.mainloop()
