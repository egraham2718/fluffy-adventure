import tkinter as tk
from g27_3_gui_tkinter import SalesFrame

def main():
    root = tk.Tk()
    root.title("Edit Sales Amount")
    SalesFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()