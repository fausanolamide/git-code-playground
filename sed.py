import tkinter as tk

root = tk.Tk()
root.title("Vertical Layout Example")

# Create three labels with some text
label1 = tk.Label(root, text="Label 1", padx=10, pady=10, bg="lightblue")
label2 = tk.Label(root, text="Label 2", padx=10, pady=10, bg="lightgreen")
label3 = tk.Label(root, text="Label 3", padx=10, pady=10, bg="lightcoral")

# Use the grid geometry manager to arrange labels in a single column
label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=2, column=0)

root.mainloop()
