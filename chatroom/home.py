from tkinter import *
#from PIL import ImageTk,Image

def run():
    home = Tk()
    home.title('Home Page')
    home.geometry('800x800')
    home.resizable(False, False)

    def login():
        home.destroy()
        import login
        login.run()

    def register():
        home.destroy()
        import register
        register.run()

    def feedback():
        home.destroy()
        import feedback
        feedback.run()

    def report():
        home.destroy()
        import report
        report.run()

    def help():
        pass

    def about_us():
        pass

    Label(home, text="Chatkaro", width=20,font=("bold", 20), background='#54596d').place(x=5, y=20)
    loginbtn = Button(home, text ="Login", command = login, relief="groove", fg='blue', width=10, height=2)
    registerbtn = Button(home, text ="Register", command = register, relief="groove", fg='blue', width=10, height=2)
    feedbackbtn = Button(home, text ="Feedback", command = feedback, relief="groove", fg='blue', width=10, height=2)
    reportbtn = Button(home, text ="Report", command = report, relief="groove", fg='blue', width=10, height=2)
    helpbtn = Button(home, text = "Help", command = help, relief="groove", fg='blue', width=10, height=2)
    about_us_btn = Button(home, text = "About Us", command = about_us, relief="groove", fg='blue', width=10, height=2)

    on = PhotoImage(file = "utilities/media/home_image.png")
    Label(home, image=on, width=800, height=550).place(x=0, y=150)
    '''
    img = ImageTk.PhotoImage(Image.open("ball.png"))
    panel = Label(home, image = img)
    panel.place(x=20, y=130)
    '''
    # Placing widgets

    loginbtn.place(x = 20, y = 80)
    registerbtn.place(x = 140, y = 80)
    feedbackbtn.place(x = 270, y = 80) 
    reportbtn.place(x = 420, y = 80)
    helpbtn.place(x = 570, y = 80)
    about_us_btn.place(x=700, y=80)


    home.configure(background='#000000')
    home.mainloop()

if __name__ == '__main__':
    run()