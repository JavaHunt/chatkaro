from tkinter import *
import mysql.connector as mysqlconnector
from random import randint

# this page contains only join and create room

class home:
    def __init__(self, username) -> None:
        self.username = username
        self.room_code = randint(100000, 999999)
        #MYSQL ConnectionString
        self.mydb = mysqlconnector.connect(host="192.168.56.1", user="root", password="root", database="chatroom", port=3030, autocommit=True)
        self.mycursor = self.mydb.cursor(buffered=True, dictionary=True)

        self.root = Tk()
        self.root.geometry('200x200')

        self.create_btn = Button(self.root, text='Create Room', bg='blue', font=("bold", 20), command=self.create_room_gui)
        self.join_btn = Button(self.root, text='Join Room', bg='green', font=("bold", 20), command=self.join_room_gui)
        self.create_btn.pack(fill=BOTH, expand=True)
        self.join_btn.pack(fill=BOTH, expand=True)
        self.root.mainloop()
    
    def create_room(self, room_name):
        import Room
        obj = Room.createroom(self.room_code, room_name, self.username)
    
    def join_room(self, room_code):
        # Creating Tk() object to pass it to joinroom()
        self.root = Tk()
        self.root.geometry('800x700')
        self.root.title('ChatKaro')
        import Room
        obj = Room.joinroom(self.root, room_code, self.username)
    
    def create_room_gui(self):
        self.root.destroy()

        self.CreateRoom = Tk()
        self.CreateRoom.geometry('200x200')
        Label(self.CreateRoom, text='Enter Room name : ').place(x=10, y=20)
        self.name = Entry(self.CreateRoom, width=18)
        self.name.place(x=15, y=50)

        self.create_btn = Button(self.CreateRoom, width=20, text='Create', command=lambda:self.create_room(self.name.get().strip()))
        self.create_btn.place(x=20, y=100)

    def join_room_gui(self):
        self.root.destroy()

        self.JoinRoom = Tk()
        self.JoinRoom.geometry('200x200')
        Label(self.JoinRoom, text='Enter Room code : ').place(x=10, y=20)
        self.code = Entry(self.JoinRoom, width=18)
        self.code.place(x=15, y=50)

        self.join_btn = Button(self.JoinRoom, width=20, text='Join', command=lambda:self.join_room(self.code.get().strip()))
        self.join_btn.place(x=20, y=100)
        