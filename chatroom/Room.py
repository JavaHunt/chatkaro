# Creating a class to create an unique room

import mysql.connector as mysqlconnector
from tkinter import *
import tkinter.messagebox as mymessagebox
from smtplib import SMTP
from plyer import notification

room_name1 = ''
mydb = mysqlconnector.connect(host="192.168.56.1", user="root", password="root", database="chatroom", port=3030, autocommit=True)
mycursor = mydb.cursor(buffered=True, dictionary=True)

class createroom:
    def __init__(self, room_code, room_name, username) -> None:
        self.root = Tk()
        #self.root.withdraw()
        self.root.title("Chat Room")
        self.root.geometry('800x700')
        #Make the window jump above all
        #self.root.attributes('-topmost',True)
        self.room_code = room_code
        self.room_name = room_name
        self.username = username
        global room_name1
        room_name1 = room_name


        # Create message table with the room code
        self.query = f'''create table {self.room_code}CK(sender varchar(20) not null, msg varchar(300), msgtime varchar(30));'''
        mycursor.execute(self.query)

        # add the room code in the chat_rooms table
        self.query = f'''insert into chat_rooms values({self.room_code}, '{self.username}', '{self.username}')'''
        mycursor.execute(self.query)

        #self.room_code_label = Label(self.root, text="code: "+str(self.room_code), font=('bold', 20))
        #self.room_code_label.place(x=300, y=6)

        # Call the joinroom class object to join the creater in the room
        joinroom(self.root, room_code, username, 1)

        self.root.mainloop()
    

class joinroom:

    # if it is called by creater then no need to display message because there will be no messages for a new chatroom
    # then joined_by_creater = 1
    # if it is called by user then we need to display all the previous messages of the chat, then joined_by_creater = 0
    def __init__(self, root, room_code, username, joined_by_creater=0) -> None:
        self.room_code = room_code
        self.root = root
        self.username = username
        self.joined_by_creator = joined_by_creater

        if self.joined_by_creator == 0:
            self.room_name_label = Label(self.root, text="ChatKaro", font=('bold', 20))
        else:
            self.room_name_label = Label(self.root, text=room_name1, font=('bold', 20))
        self.room_name_label.place(x=10, y=6)

        self.room_code_label = Label(self.root, text="code: "+str(room_code), font=('bold'))
        self.room_code_label.place(x=200, y=6)

        self.share_code_btn = Button(self.root, text="Share",font="Helvetica 10 bold", width=10,bg="#ABB2B9", relief=FLAT,
                                    command=self.share_code)
        self.share_code_btn.place(x=500, y=6)

        self.exit_btn = Button(self.root, text="Exit",font="Helvetica 10 bold", width=10,bg="#ABB2B9", relief=FLAT,
                                    command=self.exit_room)
        self.exit_btn.place(x=600, y=6)

        # setting a end meeting button for the admin
        if joined_by_creater == 1:
            self.exit_btn = Button(self.root, text="End room",font="Helvetica 10 bold", width=10,bg="#ABB2B9", relief=FLAT,
                                    command=self.end_room)
            self.exit_btn.place(x=700, y=6)

        # fetching users into the chat_rooms members
        query = f'''SELECT room_mates from chat_rooms where room_code = {self.room_code}'''
        mycursor.execute(query)
        myres = mycursor.fetchone() # List of dictionary will be returned
        print(myres)
        print(type(myres))
        temp_members = myres.get('room_mates')
        #temp_members = 'pardhu'
        # updating the room members column
        temp_members = temp_members + ':' + self.username

        # Insert updates of chat room into database
        if self.joined_by_creator == 0:
            query = f'''update chat_rooms set room_mates =  '{temp_members}' where room_code = {self.room_code}'''
            mycursor.execute(query)
        self.layout()

    def layout(self):
		# to show chat window

        self.line = Label(self.root, width=450, bg="#ABB2B9")

        self.line.place(relwidth=1,rely=0.07, relheight=0.012)

        self.textCons = Text(self.root, width=20, height=2, bg="#c6f4f4", fg="#000000",font="Helvetica 14",padx=5,pady=5)

        self.textCons.place(relheight=0.745,relwidth=1, rely=0.08)

        self.labelBottom = Label(self.root,bg="#ABB2B9", height=80)

        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(self.labelBottom,bg="#90fed9",fg="#000000", font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,relheight=0.06,rely=0.008, relx=0.011)
        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,text="Send",font="Helvetica 10 bold", width=20,bg="#ABB2B9",
                            command=lambda: self.sendButton(self.entryMsg.get().strip()))

        self.buttonMsg.place(relx=0.77,rely=0.008,relheight=0.06, relwidth=0.22)

        # Roomates List
        self.roomatesbtn = Button(self.labelBottom, text="view roomates", command=self.show_roomates)
        self.roomatesbtn.place(relx=0.77,rely=0.002,relheight=0.03, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1, relx=0.974)

        scrollbar.config(command=self.textCons.yview)


        if self.joined_by_creator == 0:
            self.display_chat()
        self.display_chat()
        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        if msg != '':
            self.textCons.config(state=DISABLED)
            self.msg = msg
            self.entryMsg.delete(0, END)

            # Present time
            from datetime import datetime
            self.dt = str(datetime.now())
            self.time = self.dt[11:19]

            # store the messages in database
            self.query = f'''insert into {self.room_code}CK values('{self.username}', '{self.msg}', '{self.time}');'''
            mycursor.execute(self.query)
            mydb.commit()

            # send a notification to the user
            query = f"SELECT sender from {self.room_code}CK where msgtime = '{self.time}'"
            mycursor.execute(query)
            res = mycursor.fetchone()
            if self.username != res['sender']:
                notification.notify(
                    title = 'Message',
                    message = self.entryMsg.get(),
                    app_name = 'ChatKaro',
                    app_icon = "utilities/media/bell.ico",
                    timeout = 7
                )


        # calling the display_chat method to refresh the Text
        self.display_chat()

    def display_chat(self):
        # display msg in Text
        # Clear the Text
        self.textCons.config(state=NORMAL)
        self.textCons.delete('1.0', END)

        self.query = f'''SELECT * from {self.room_code}CK;'''
        mycursor.execute(self.query)
        # Result will be list of dictionaries(rows)
        self.myres = mycursor.fetchall()
        self.textCons.config(state=NORMAL)
        for i in self.myres:
            text_to_insert = f"{i['sender']} : {i['msg']}"
            time_to_insert = f"{i['msgtime']}"
            self.textCons.insert(END, text_to_insert+"\n"+time_to_insert+"\n\n")

        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        self.root.after(4000, self.display_chat)
    

    def show_roomates(self):
        query = f'''SELECT room_mates from chat_rooms where room_code = {self.room_code}'''
        mycursor.execute(query)
        myres = mycursor.fetchone() #  dictionary will be returned
        self.room_members = myres.get('room_mates')
        self.room_members = self.room_members.split(':')
        mymessagebox.showinfo('roomates', self.room_members)


    # This will send a mail to the users asking them to join in the room
    def share_code(self):
        self.room = Tk()
        self.room.geometry('400x400')
        self.room.title('Share code')
        
        # Display users on the screen
        query = 'Select username, email from users'
        mycursor.execute(query)
        res = mycursor.fetchall()
        self.users_list = {}
        self.search_bar = Entry(self.room, relief=FLAT)
        def search():
            mymessagebox.showinfo('Maintenance', 'This feature is under maintenance')
        self.search_btn = Button(self.room, text='search', command=search, bg='green')

        #self.search_bar.place(x=20, y=20)
        #self.search_btn.place(x=80, y=20)
        for i in range(len(res)):
            def send_code(email=res[i]['email']):
                sender = 'techtreat6@gmail.com'
                app_password = 'vpdvocjtlfcavdsu'
                receiver = email
                message =f'''Greetings,
                                You are invited to Join a chatroom from your friend {self.username}
                                Use the below code to join in the chatroom

                                {self.room_code}

                    Regards,
                    ChatKaro team'''

                subject = f'Invitation from {self.username}'
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
                    mymessagebox.showinfo('mail sent', 'Mail sent successfully')
                    server.close()
            self.users_list[res[i]['username']] = Button(self.room, text=res[i]['username'], command=send_code, width=20, relief=FLAT)
            self.users_list[res[i]['username']].pack()

        self.room.mainloop()
    

    # Save the room chat in media folder
    def save_chat(self):
        query = f"SELECT * from {self.room_code}ck;"
        mycursor.execute(query)
        myres = mycursor.fetchall()
        fname = f"media/{self.room_code}ck"
        f = open(fname, 'w')
        for row in myres:
            f.write(row['sender'] + ' : ' + row['msg'] + '\n')
            f.write(row['msgtime'] + '\n')
        f.close()
        mymessagebox.showinfo('Saved', "Your chat is saved in 'media' folder of current directory")

    
    # This will exit the meeting (available for all users)
    def exit_room(self):
        if mymessagebox.askyesno('Exit Room', 'Do you want to exit room?'):
            if mymessagebox.askyesno("Save chat", "Do you want to save this room chat?"):
                self.save_chat()
            self.root.destroy()
            mymessagebox.showinfo('Exited', 'You exited Successfully')


    # This will end the meeting (only for admin)
    def end_room(self):
        if mymessagebox.askyesno('End Room', 'Do you want to end room permanently? '):
            if mymessagebox.askyesno("Save chat", "Do you want to save this room chat?"):
                self.save_chat()
            mycursor.execute(f"drop table {self.room_code}ck")
            mycursor.execute(f"DELETE FROM chat_rooms where room_code = {self.room_code}")
            self.root.destroy()
            mymessagebox.showinfo('Ended', 'Room ended successfully')
