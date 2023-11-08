from tkinter import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import subprocess
import os

root = Tk()
root.title("Blender To Do List")
root.geometry("400x630+790+50")
root.resizable(False, False)

task_list = []
db_engine = create_engine('sqlite:///task_list.db')

# Create a base class for declarative class definitions
Base = declarative_base()

# Define a Task class to map to the database table


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)


# Create the table if it doesn't exist
Base.metadata.create_all(db_engine)

# Create a session to interact with the database
Session = sessionmaker(bind=db_engine)
db_session = Session()


# Function to open Blender with a specific task file
def open_blender_with_task(task_filename):
    if not os.path.exists(task_filename):
        os.path.exists(task_filename)

    try:
        # Specify the correct path
        blender_executable = 'C:\\Program Files\\Blender Foundation\\Blender 3.5\\blender.exe'

        subprocess.run([blender_executable, task_filename], check=True)
    except Exception as e:
        print(f"Error opening Blender: {e}")

# Function to open Blender when a task is clicked


def open_blender_task(task_description, task_index):
    # Create a unique task filename based on the task's description or index
    task_folder = 'blendlists'  # Folder to save the .blend files
    # Create the folder if it doesn't exist
    os.makedirs(task_folder, exist_ok=True)
    task_filename = os.path.join(
        task_folder, f'task_{task_index}_{task_description}.blend')

    # Open Blender with the task file
    open_blender_with_task(task_filename)

# Add a task with Blender integration


def AddTask():
    task = task_entry.get()
    task_entry.delete(0, END)
    if task:
        task_list.append(task)
        listbox.insert(END, task)

        # Save the task to the database
        new_task = Task(description=task)
        db_session.add(new_task)
        db_session.commit()

        # #  create an index for the file
        # task_index = len(task_list) - 1

        # #  Call open_blender_task with the task description and index
        # open_blender_task(task, task_index)


def deleteTask():
    selected_task = listbox.curselection()
    if selected_task:
        task_index = selected_task[0]
        deleted_task = task_list.pop(task_index)
        listbox.delete(task_index)

        # Delete the task from the database
        db_session.query(Task).filter(
            Task.description == deleted_task).delete()
        db_session.commit()


def searchTask():
    keyword = task_entry.get()
    listbox.delete(0, END)  # Clear the Listbox
    found_tasks = db_session.query(Task).filter(
        Task.description.ilike(f'%{keyword}%')).all()

    if found_tasks:
        for task in found_tasks:
            listbox.insert(END, task.description)
    else:
        listbox.insert(END, "No results found")


image_top = PhotoImage(file="task.png")
root.iconphoto(True, image_top)
# top image
topImage = PhotoImage(file='topbar.png')
Label(root, image=topImage).pack()

dockImage = PhotoImage(file="dock.png")
Label(root, image=dockImage, bg="#32405b").place(x=13, y=20)

noteImage = PhotoImage(file="task.png")
Label(root, image=noteImage, bg="#32405b").place(x=300, y=20)

h1 = Label(root, text="ALL TASK ",
           font="arial 20 bold", fg="white", bg="#32405b")
h1.place(x=130, y=20)
# main
frame = Frame(root, width=400, height=50, bg="white")
frame.place(x=0, y=130)

task = StringVar()
task_entry = Entry(frame, width=20, font="arial 20", bd=0)
task_entry.place(x=10, y=7)
task_entry.focus()

button = Button(frame, text='ADD', width=6, font='arial 20 bold',
                bg='#5a95ff', fg='#fff', command=AddTask)
button.place(x=300, y=0)
# list
frame1 = Frame(root, bd=3, width=700, height=280, bg="#32405b")
frame1.pack(pady=(130, 0))

listbox = Listbox(frame1, font=("arial"), width=40,
                  height=13, bg='#32405b', fg="white", cursor="hand2", selectbackground='#5a95ff')
listbox.pack(side=LEFT, fill=BOTH, padx=2)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)

Button2 = Button(text='SEARCH', bg="yellow", command=searchTask)
Button2.pack(pady=(40, 0))

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
# openTaskFile()
# delete
delete_icon = PhotoImage(file='delete.png')
Button(root, image=delete_icon, bd=0,
       command=deleteTask).pack(side=BOTTOM, pady=8)
open_blender_button = Button(text='Open in Blender', bg="green", command=lambda: open_blender_task(
    listbox.get(listbox.curselection()), listbox.curselection()[0]))
open_blender_button.pack(pady=(5, 0))

# funtion to load data from a data base


def openTaskFile():
    tasks = db_session.query(Task).all()
    for task in tasks:
        task_list.append(task.description)
        listbox.insert(END, task.description)


# Load tasks from the database when the application starts
openTaskFile()

root.mainloop()
