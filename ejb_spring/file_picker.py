import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

file_path = filedialog.askopenfilename()  # Open the file picker dialog

print(file_path)  # Output the selected file path (you can adjust this to return the path as needed)
