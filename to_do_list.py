from tkinter import *
from tkinter import messagebox

task_list = []


def newTask():
    task = my_entry.get()
    my_entry.delete(0, "end")
    if task != "":
        with open('task_list', 'a') as taskfile:
            taskfile.write(f'/n{task}')
        task_list.append(task)
        lb.insert(END, task)

    else:
        messagebox.showwarning("warning", "Please enter some task.")


def openTaskFile():
    try:
        global task_list
        with open('task_list', 'a') as taskfile:
            taskfile.readlines()
        for task in task_list:
            if task != '/n':
                task_list.append(task)
                lb.insert(END, task)
    except:
        file = open('task_list', 'w')
        file.close()


def searchTask():
    text = search_entry.get()
    lb.delete(0, END)

    for task in task_list:
        if text in task:
            lb.insert(END, task)


def deleteTask():
    lb.delete(ANCHOR)


ws = Tk()
ws.geometry('800x600+500+120')
ws.title('TO DO LIST')
ws.config(bg='#008000')
ws.resizable(width=True, height=True)
image = PhotoImage(file="screenshot.png")
ws.iconphoto(False, image)
# pc = ws.resizable(width=True, height=True)
search_frame = Frame(ws)
search_frame.pack(pady=20)

search_entry = Entry(
    search_frame,
    font=('times', 24)
)
search_entry.pack(pady=20)

serTask_btn = Button(
    search_frame,
    text='Search task',
    font=('times 14'),
    bg='#ff8b61',
    padx=20,
    pady=10,
    command=searchTask
)
serTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

frame = Frame(ws)
frame.pack(pady=10)


lb = Listbox(
    frame,
    width=34,
    height=8,
    font=('Times', 18),
    bd=0,
    fg='#464646',
    highlightthickness=0,
    selectbackground='#a6a6a6',
    activestyle="none",

)

lb.pack(side=LEFT, fill=BOTH)

for item in task_list:
    lb.insert(END, item)

sb = Scrollbar(frame)
sb.pack(side=RIGHT, fill=BOTH)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)

my_entry = Entry(
    ws,
    font=('times', 24)
)


my_entry.pack(pady=20)


button_frame = Frame(ws)
button_frame.pack(pady=20)

addTask_btn = Button(
    button_frame,
    text='Add Task',
    font=('times 14'),
    bg='#c5f776',
    padx=20,
    pady=10,
    command=newTask
)
addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

delTask_btn = Button(
    button_frame,
    text='Delete Task',
    font=('times 14'),
    bg='#ff8b61',
    padx=20,
    pady=10,
    command=deleteTask
)
delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)


# def save_to_do_list(tasks, filename):
#     with open(filename, 'w') as file:
#         for task in tasks:
#             file.write(task + '\n')


ws.mainloop()
