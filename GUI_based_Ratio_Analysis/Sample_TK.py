import tkinter as tk
from tkinter import messagebox

def on_button_click():
    if check_var.get():
        messagebox.showinfo("Check Status", "Checkbox is checked!")
    else:
        messagebox.showinfo("Check Status", "Checkbox is not checked!")

# Create the main window
root = tk.Tk()
root.title("Tkinter Checkbox Example")
root.geometry("300x200")

# Create a checkbox
check_var = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Check me!", variable=check_var)
checkbox.pack(pady=20)

# Create a button to check the status
check_button = tk.Button(root, text="Check Status", command=on_button_click)
check_button.pack(pady=10)

# Run the application
if __name__ == "__main__":
    # Start the Tkinter event loop
    root.mainloop()