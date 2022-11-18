import mysql.connector as mysqlconnector
from tkinter import *
import tkinter.messagebox as mymessagebox
from random import randint
from smtplib import SMTP


loginLimit = 5
def run():
    otp = randint(101001, 999999)
    MyLoginForm = Tk()
    MyLoginForm.title('Login Form')
    #Set Form Size
    MyLoginForm.geometry("350x300")
    # Not resizable
    MyLoginForm.resizable(False, False)


    #MYSQL ConnectionString
    mydb = mysqlconnector.connect(host="192.168.56.1", user="root", password="root", database="chatroom", port=3030, autocommit=True)
    mycursor = mydb.cursor(buffered=True, dictionary=True)

    UserTxt = Entry(MyLoginForm,  width=27, relief="flat")
    UserTxt.place(x=120, y=60)

    #Set Focus on User Entrybox in Tkinter
    UserTxt.focus()

    PassTxt = Entry(MyLoginForm,  width=27, relief="flat", show='*')
    PassTxt.place(x=120, y=90)

    # This will send mail to the user when he failed to login
    def send_mail(email):
        sender = 'techtreat6@gmail.com'
        app_password = 'vpdvocjtlfcavdsu'
        receiver = email
        message =f'''Hello,
                        Sorry to say you....
                        You or someone else tried to login to your ChatKaro account but failed to login !!
                        You account is tempararily disabled... Reply back to this email to recover your account

                        We like to work with you...


            Regards,
            ChatKaro team'''

        subject = f'ALERT ! Failed to login'
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
            server.close()

    def ClicktoLogin():
        global loginLimit
        if UserTxt.get().strip() != '' and PassTxt.get().strip() != '':
            username = UserTxt.get().strip()
            print('u', UserTxt.get().strip(), 'p ', PassTxt.get().strip())
            mycursor.execute("SELECT * FROM users where username = '"+ username +"' and passwords = '"+ PassTxt.get().strip() +"';")
            myresult = mycursor.fetchone()
            if myresult==None:
                loginLimit -= 1
                if loginLimit == 0:
                    mymessagebox.showerror("Can't login", "You reached maximum number of trails.. You can't login")
                    LoginBtn['state'] = DISABLED
                    query = f"SELECT username, email from users where username='{username}'"
                    mycursor.execute(query)
                    myres = mycursor.fetchone()
                    if myres != None:
                        query = f"UPDATE users SET permission=0 where username = '{username}';"
                        mycursor.execute(query)
                        mymessagebox.showwarning("Can't Login", "You can't login.. Contact ChatKaro team via 'about us' tab in home page")
                        send_mail(myres['email'])
                else:
                    mymessagebox.showerror("Error", "Invalid User Name And Password \
                    you left %s trials "%(loginLimit))

            else:
                if myresult['permission'] == 1:
                    mymessagebox.showinfo("Success", "Successfully Login")
                    MyLoginForm.destroy()
                    #import user
                    #o = user.User(username)
                    import face_page
                    o = face_page.home(username)
                else:
                    mymessagebox.showinfo('No permission', "You don't have permission to login... Contact chatkaro team")
                    
            #mydb.close()
            #mycursor.close()
        else:
            mymessagebox.showerror('Empty Fields', 'All fields are mandatory')

    # method to show the password 
    def my_show():
        if(c_v1.get()==1):
            PassTxt.config(show='')
        else:
            PassTxt.config(show='*')


    # Action for Forgot password
    def forgot_password():
        ForgotForm = Tk()
        MyLoginForm.destroy()

        ForgotForm.title('forgot password')
        ForgotForm.geometry('400x350')

        Label(ForgotForm, text="Forgot Password", width=20,font=("bold", 20), background='#54596d').place(x=20, y=30)
        email = Label(ForgotForm, text="Email", width=10)
        emailtxt = Entry(ForgotForm,  width=27, relief="flat")
        otp_entry = Entry(ForgotForm, width=27, relief="flat")
        otp_entry.place(x=130, y=150)

        emailtxt.focus()

        # go back to home
        def go_back_to_home():
            ForgotForm.destroy()
            import home
            home.run()

        # This method will return the entered otp by refreshing every second
        def get_entered_otp():
            print('otp : ', otp)
            print('otp.get() : ', otp_entry.get().strip())
            if str(otp) == otp_entry.get().strip():
                # Disable get OTP button
                get_otp_btn['state'] = DISABLED
                change_password_btn['state'] = NORMAL
            else:
                get_otp_btn['state'] = NORMAL
                change_password_btn['state'] = DISABLED

            ForgotForm.after(3000, get_entered_otp)

        email.place(x=30, y=100)
        emailtxt.place(x=130, y=100)
        get_otp_btn = Button(ForgotForm, text='Get OTP', command=lambda:get_otp(emailtxt.get().lower().strip()), relief="groove", fg='blue', width=15, height=1)
        get_otp_btn.place(x=30, y=210)

        Label(ForgotForm, text="Enter your registered email to get OTP").place(x=40, y=260)

        Label(ForgotForm, text='OTP ').place(x=30, y=150)

        change_password_btn = Button(ForgotForm, text='Change Password', command=lambda:change_password(emailtxt.get().lower().strip(), ForgotForm), relief="groove", fg='blue', width=15, height=1)
        change_password_btn.place(x=180, y=210)
        change_password_btn['state'] = DISABLED
        
        homebtn = Button(ForgotForm, text="Home", command = go_back_to_home, relief="groove", fg='blue', width=15, height=1)
        homebtn.place(x=150, y=300)

        get_entered_otp()

        ForgotForm.configure(background='#54596d')

        ForgotForm.mainloop()


    def update_password(email, passwd1, passwd2):
        if passwd1 != '' and passwd2 != '':
            if passwd1 == passwd2:
                query = f"UPDATE users SET passwords='{passwd1}' where email = '{email}';"
                mycursor.execute(query)
            else:
                mymessagebox.showerror('NOT Equal Passwords', 'New Password and Confirm New Password not matched')
        else:
            mymessagebox.showerror('Empty fields', 'All fields are mandatory')

    # change Password
    def change_password(email, window):
        window.destroy()
        root = Tk()
        root.geometry('400x400')

        Label(root, text="Change Password", font=('bold', 20), width=20).place(x=30, y=30)
        new_password1 = Label(root, text="New Password", width=25)
        new_password1.place(x=30, y=80)
        new_password1txt = Entry(root, relief='flat', width=30)
        new_password1txt.place(x=100, y=110)

        new_password2 = Label(root, text='Confirm New Password', width=25)
        new_password2.place(x=30, y=150)
        new_password2txt = Entry(root, relief='flat', width=30)
        new_password2txt.place(x=100, y=180)

        change_password_btn = Button(root, text='Change Password',command=lambda: update_password(email, new_password1txt.get().strip(), new_password2txt.get().strip()), relief="groove", fg='blue', width=20, height=2)
        change_password_btn.place(x=120, y=230)

        root.mainloop()

    # Send a email with otp
    def get_otp(email):
        if email != '':
            # checking if email is registered or not
            query = "SELECT * from users where email='" + email + "';"
            mycursor.execute(query)
            res = mycursor.fetchone()
            # email exits
            if res != None:
                sender = 'techtreat6@gmail.com'
                app_password = 'vpdvocjtlfcavdsu'
                receiver = email
                message =f'''Greetings,
                                You are requested for your account password OTP.... Enter the below OTP to change your password
                                OTP : {otp}
                                Don't share your OTP with anyone...
                    Regards,
                    ChatKaro team'''

                subject = 'Forgot Password OTP'
                msg1 = 'Subject: %s\n\n%s' % (subject, message) 
                from smtplib import SMTP
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
                    mymessagebox.showinfo("OTP Sent", "OTP sent to your given email")
                    server.close()
                    
            else:
                mymessagebox.showerror("Email not valid", "Entered email is not registered      \
                                        Check if you have entered any white spaces in email")
        else:
            mymessagebox.showerror('Empty field', 'Email field is mandatory to get OTP')
    
    # go back to home
    def go_back_to_home():
        MyLoginForm.destroy()
        import home
        home.run()

    # Set Tkinter Widget Size Location and Style
    Bannerlabel = Label(MyLoginForm, text = "Login Form......", width=40, bg= 'yellow')
    Bannerlabel.place(x=20, y=20)

    UserLabel = Label(MyLoginForm, text = "User Name:", width=10)
    UserLabel.place(x=20, y=60)


    PassLabel = Label(MyLoginForm, text = "Password :", width=10)
    PassLabel.place(x=20, y=90)

    # Checkbox variable to get input, default value is 0
    c_v1=IntVar(value=0)
    show_password = Checkbutton(MyLoginForm,text='Show Password',variable=c_v1,
        onvalue=1, offvalue=0, command=my_show)

    show_password.place(x=150, y=120)

    forgot_password_btn = Button(MyLoginForm, text ="forgot password?", command = forgot_password, relief="groove", fg='blue', height=1)
    forgot_password_btn.place(x=150, y=160)

    LoginBtn = Button(MyLoginForm, text ="Login", command = ClicktoLogin, relief="groove", fg='blue', width=10, height=2)
    LoginBtn.place(x=250, y=210)

    HomeBtn = Button(MyLoginForm, text ="Home", command = go_back_to_home, relief="groove", fg='blue', width=10, height=2)
    HomeBtn.place(x=50, y=210)

    MyLoginForm.configure(background='#54596d')
    MyLoginForm.mainloop()