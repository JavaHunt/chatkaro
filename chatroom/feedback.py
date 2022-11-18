from tkinter import *
import tkinter.messagebox as mymessagebox

is_on = True

def run():
    root = Tk()
    root.geometry("650x700") # w x h

    # Title
    Label(root, text="Feedback form", justify=CENTER, font=('bold', 20)).place(x=200, y=15)
    nameLabel = Label(root, text="Name : ", font=(11))
    performanceLabel = Label(root, text="Performance : ", font=(11))
    smoothnessLabel = Label(root, text="Smoothness : ", font=(11))
    are_you_aware_Label = Label(root, text="How much you are aware of this app : ", font=(11))
    useLabel = Label(root, text="Do you know how to use this app?", font=(11))  # Yes or no type
    problems_faced_Label = Label(root, text="Did you face any problems using this app? Let us know", font=(11)) # Text field
    new_features_Label = Label(root, text="Do you need any new features? Mention here", font=(11)) # text field
    overall_rating_Label = Label(root, text="Overall Rating of this app : ", font=(11))  # Slice type


    performanceVar  = IntVar()
    smoothnessVar = IntVar()
    overall_rating_Var = IntVar()
    are_you_aware_Var = IntVar()

    name = Entry(root)
    performance = Scale(root, variable=performanceVar, from_= 1, to=5, orient=HORIZONTAL)
    smoothness = Scale(root, variable=smoothnessVar, from_= 1, to=5, orient=HORIZONTAL)
    overall_rating = Scale(root, variable=overall_rating_Var, from_= 1, to=5, orient=HORIZONTAL)
    are_you_aware = Scale(root, variable=are_you_aware_Var, from_= 1, to=5, orient=HORIZONTAL)
    problems_faced = Text(root, width=50, height=3, fg="black", bg="white")
    new_features = Text(root, width=50, height=3, fg="black", bg="white")

    problems_faced.focus()

    def submit():
        if name.get().strip() != '' and problems_faced.get().strip() != '' and new_features.get().strip() != '':
            sender = 'techtreat6@gmail.com'
            app_password = 'vpdvocjtlfcavdsu'
            receiver = ['pardhu9100@gmail.com', 'korlapuyamini@gmail.com']
            message =f'''Greetings,
                            You got a feedback from {name.get().strip()}
                            ----------------------------------------------

                            Performance : {performanceVar.get()}
                            Smoothness : {smoothnessVar.get()}
                            Do you know how to use? : {is_on}
                            Are you aware of this app? : {are_you_aware_Var.get()}
                            Problems faced:
                                {problems_faced.get('1.0', END).strip()}
                            New Features Required:
                                {new_features.get('1.0', END).strip()}
                            overall rating : {overall_rating_Var.get()}


                Regards,
                ChatKaro team'''

            subject = f'Feedback from {name.get().strip()}'
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
                server.sendmail(from_addr= sender,to_addrs= receiver[0],msg= msg1)
                server.sendmail(from_addr= sender,to_addrs= receiver[1],msg= msg1)
                server.close()
                print("Mail sent successfully")
        else:
            mymessagebox.showerror('Empty Fields', 'All Fields are mandatory')
    # Define our switch function
    def switch():
        global is_on
        
        # Determine is on or off
        if is_on:
            useLabelbtn.config(image = off)
            is_on = False
        else:
        
            useLabelbtn.config(image = on)
            is_on = True

    # Define Our Images
    on = PhotoImage(file = "utilities/media/on.png")
    off = PhotoImage(file = "utilities/media/off.png")

    # Create A Button
    useLabelbtn= Button(root, image = off, bd = 0, command = switch)

    submit_btn = Button(root, text="Submit", command=submit, width=15, bg='blue', fg='white')

    # placing widgets
    nameLabel.place(x=20, y=60)
    name.place(x=180, y=60)
    performanceLabel.place(x=20, y=100)
    performance.place(x=180, y=90)
    smoothnessLabel.place(x=20, y=150)
    smoothness.place(x=180, y=140)
    useLabel.place(x=20, y=220)
    useLabelbtn.place(x=390, y=210)
    are_you_aware_Label.place(x=20, y=280)
    are_you_aware.place(x=400, y=280)
    problems_faced_Label.place(x=20, y=350)
    problems_faced.place(x=120, y=380)
    new_features_Label.place(x=20, y=450)
    new_features.place(x=120, y=490)
    overall_rating_Label.place(x=20, y=570)
    overall_rating.place(x=310, y=560)
    submit_btn.place(x=280, y=630)

    root.mainloop()

