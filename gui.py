# Import the required libraries
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import download, threading
import tkinter.scrolledtext as st

# Create an instance of tkinter frame or window
win=Tk()

win.title("Local Cloud")
# Set the size of the window
win.geometry("700x350")

# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
   win.destroy()

# Define a function to show the window again
def show_window(icon, item):
   icon.stop()
   win.after(0,win.deiconify())

# Hide the window and show on the system taskbar
def hide_window():
   win.withdraw()
   image=Image.open("favicon.ico")
   menu=(item('Quit', quit_window), item('Show', show_window))
   icon=pystray.Icon("name", image, "Local Cloud client", menu)
   icon.run()

def background(func, args):
    print("args = ", args)
    th = threading.Thread(target=func, args=args, daemon=True)
    th.start()
    
def format_keys(keys):
    formatted = ""
    for key,value in keys.items():
        formatted += "Key = {key}, File = {file}\n".format(key = key, file = value)
    return formatted

def add_components():
    start_flask_button = Button(win,text='Start Flask',command = lambda : background(download.start_flask, ()))  #args must be a tuple even if it is only one
    start_flask_button.pack() 

    new_key = StringVar()
    add_key_entry = Entry(win, textvariable=new_key)
    add_key_entry.pack(fill='x', expand=True)
    add_key_button = Button(win,text='Add Key',command = lambda : background(download.add_key, (new_key.get(),)))  #args must be a tuple even if it is only one
    add_key_button.pack()

    keys_box_area = st.ScrolledText(win,width = 300, height = 30, font = ("Times New Roman",15))
    keys_box_area.pack()
    keys_box_area.insert(INSERT,format_keys(download.get_keys()))
    keys_box_area.configure(state ='disabled')

    
    

add_components()

win.protocol('WM_DELETE_WINDOW', hide_window)

win.mainloop()