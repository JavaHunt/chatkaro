from tkinter import *
import tkinter.messagebox as mymessagebox
#import mysql.connector as mysqlconnector



def run():
    root = Tk()
    root.title("Report")
    root.geometry('400x400')

    #MYSQL ConnectionString
    #mydb = mysqlconnector.connect(host="192.168.56.1", user="root", password="root", database="chatroom", port=3030, autocommit=True)
    #mycursor = mydb.cursor(buffered=True, dictionary=True)
    
    Label(root, text="Report").place(x=100, y=20)
    nameLabel = Label(root, text="Name : ")
    emailLabel = Label(root, text="Email : ")
    report_titleLabel = Label(root, text="Report Subject : ")
    reportlabel = Label(root, text="Describe your problem")
    
    name = Entry(root, width=27, relief="flat")
    email =  Entry(root, width=27, relief="flat")
    report_title =  Entry(root, width=27, relief="flat")
    report =  Entry(root, width=27, relief="flat")

    def send_report():
        if email.get().strip() != '' and name.get().strip() != '' and report_title.get().strip() != '' and report.get().strip() != '':

            sender = 'techtreat6@gmail.com'
            app_password = 'vpdvocjtlfcavdsu'
            receiver = email.get().strip()
            message =f'''Hello,
                            Here is a report from the ChatKaro users
                            name : {name.get().strip()}
                            email : {email.get().strip()}
                            Subject : {report_title.get().strip()}
                            Description : {report.get().strip()}

                    By,
                    ChatKaro team'''

            subject = 'ChatKaro report'
            msg1 = 'Subject: %s\n\n%s' % (subject, message) 
            import smtplib 
            server = smtplib.SMTP("smtp.gmail.com",587)
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
                mymessagebox.showinfo("Report Sent", "Report Successfully sent to the ChatKaro team")
                server.close()
        else:
            mymessagebox.showerror('Empty field', 'All fields are mandatory')
    
    # go back to home
    def go_back_to_home():
        root.destroy()
        import home
        home.run()


    submitbtn = Button(root, text="Submit", command = send_report, relief="groove", fg='blue', width=10, height=2)
    homebtn = Button(root, text="Home", command = go_back_to_home, relief="groove", fg='blue', width=10, height=2)

    # placing Widgets

    nameLabel.place(x=20, y=70)
    name.place(x=180, y=70)
    emailLabel.place(x=20, y=120)
    email.place(x=180, y=120)
    report_titleLabel.place(x=20, y=170)
    report_title.place(x=180, y=170)
    reportlabel.place(x=20, y=220)
    report.place(x=180, y=220)
    submitbtn.place(x=250, y=300)
    homebtn.place(x=50, y=300)

