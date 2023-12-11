from tkinter import *
from tkinter import messagebox, simpledialog
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import subprocess
import os

root = Tk()
root.title("Blender To Do List")
root.geometry("420x630+790+50")
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


def add_task_dialog():
    task = simpledialog.askstring("Add Task", "Enter the task:")
    if task:
        task_list.append(task)
        listbox.insert(END, task)

        # Save the task to the database
        new_task = Task(description=task)
        db_session.add(new_task)
        db_session.commit()

    else:
        messagebox.showwarning("warning", "Please enter some task.")

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
        # Get the filename associated with the deleted task
        task_folder = 'blendlists'
        task_filename = os.path.join(
            task_folder, f'task_{task_index}_{deleted_task}.blend')
        try:
            os.remove(task_filename)
        except Exception as e:
            print(f"Error deleting file: {e}")

# Function to open Blender when a task is double-clicked


def double_click_handler(events):
    selected_task_index = listbox.curselection()
    if selected_task_index:
        open_blender_task(listbox.get(selected_task_index),
                          selected_task_index[0])


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


# Create a context menu
context_menu = Menu(root, tearoff=0)

# Function to handle the "Open in Blender" option


def open_blender_context_menu_handler():
    selected_task_index = listbox.curselection()
    if selected_task_index:
        open_blender_task(listbox.get(selected_task_index),
                          selected_task_index[0])

# Function to handle the "Delete" option


def delete_context_menu_handler():
    deleteTask()


def add_context_menu_handler():
    add_task_dialog()


# Add options to the context menu
context_menu.add_command(label="Open in Blender",
                         command=open_blender_context_menu_handler)
context_menu.add_command(label="Delete", command=delete_context_menu_handler)
context_menu.add_command(label="add", command=add_context_menu_handler)
# Function to display the context menu


def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)


#  IMAGE SECTION
image_top = PhotoImage(file="task.png")
root.iconphoto(True, image_top)

topImage = PhotoImage(file='topbar.png')
Label(root, image=topImage).pack()

dockImage = PhotoImage(file="dock.png")
Label(root, image=dockImage, bg="#32405b").place(x=13, y=20)

noteImage = PhotoImage(file="task.png")
Label(root, image=noteImage, bg="#32405b").place(x=300, y=20)

search_image = PhotoImage(file="search.png")
add_image = PhotoImage(file="add.png")
delete_image = PhotoImage(file='delete.png')
open_blender_image = PhotoImage(file='open blender.png')

h1 = Label(root, text="ALL TASK ",
           font="arial 20 bold", fg="white", bg="#32405b")
h1.place(x=130, y=20)
# main
frame = Frame(root, width=420, height=50, bg="white")
frame.place(x=0, y=130)

task = StringVar()
task_entry = Entry(frame, width=20, font="arial 20", bd=0)
task_entry.place(x=10, y=7)
task_entry.focus()

button = Button(frame, image=search_image, width=39, height=39,
                bg='#5a95ff', fg='#fff', command=searchTask)
button.place(x=370, y=0)
# listbox
frame1 = Frame(root, bd=3, width=700, height=280, bg="#32405b")
frame1.pack(pady=(110, 0), padx=0)  # Set padx to 0 to eliminate left margin

listbox = Listbox(frame1, font=("arial"), width=40,
                  height=13, bg='#32405b', fg="white", cursor="hand2", selectbackground='#5a95ff')
listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=0)
scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)
# bind the double click handler function to the listbox
listbox.bind("<Double-Button-1>", double_click_handler)
# bind the right click contexts menu to the list box
listbox.bind("<Button-3>", show_context_menu)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

add_icon = Button(root, image=add_image,
                  bg="#32405b", command=add_task_dialog)
add_icon.place(x=400, y=190)

Button(root, image=delete_image, bd=0,
       command=deleteTask).place(x=400, y=240)
open_blender_button = Button(image=open_blender_image, bg="green", command=lambda: open_blender_task(
    listbox.get(listbox.curselection()), listbox.curselection()[0]))
open_blender_button.place(x=400, y=210)

# funtion to load data from a data base


def openTaskFile():
    tasks = db_session.query(Task).all()
    for task in tasks:
        task_list.append(task.description)
        listbox.insert(END, task.description)


# Load tasks from the database when the application starts
openTaskFile()

root.mainloop()
