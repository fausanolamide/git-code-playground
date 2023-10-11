import tkinter
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("To Do List")
root.geometry("400x630+400+100")
root.resizable(False, False)

task_list = []


def AddTask():
    task = task_entry.get()
    task_entry.delete(0, END)
    if task:
        with open('task_list.txt', 'a') as taskfile:
            taskfile.write(f"/n{task}")
    task_list.append(task)
    listbox.insert(END, task)


def searchTask():
    input = task_entry.get()
    listbox.delete(0, END)

    for task in task_list:
        if input in task:
            listbox.insert(END, task)

    # input = task_entry.get()
    # task_entry.delete(0, END)
    # for task in task_list:
    #     if input in task:
    #         listbox.delete(0, END)
    #         listbox.insert(0, task)


def deleteTask():
    listbox.delete(ANCHOR)


def openTaskFile():
    try:
        global task_list
        with open('task_list.txt', 'a') as taskfile:
            taskfile.readlines()
        for task in task_list:
            if task != '/n':
                task_list.append(task)
                listbox.insert(END, task)
    except:
        file = open('task_list.txt', 'w')
        file.close()


# icon
image_top = PhotoImage(file="task.png")
root.iconphoto(False, image_top)
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
       command=deleteTask).pack(side=BOTTOM, pady=13)

root.mainloop()
with open('task_list.txt', 'a') as taskfile:
    taskfile.readlines()
