from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image
import backend, threading, sys, os

PADX = 5
PADY = 5
RESOURCE_PATH = sys._MEIPASS
FAVICON = os.path.join(RESOURCE_PATH, "favicon.ico")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        backend.add_key(sys.argv[1])
        sys.exit()
    else:
        # Create an instance of tkinter frame or window
        win=Tk()   

        win.resizable(0, 0)
        win.title("LocalLink")
        win.iconbitmap(FAVICON)
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
            image=Image.open(FAVICON)
            menu=(item('Quit', quit_window), item('Show', show_window))
            icon=pystray.Icon("name", image, "LocalLink client", menu)
            icon.run()

        def open_popup(msg):
            top = Toplevel(win)
            top.resizable(0, 0)
            top.iconbitmap(FAVICON)
            top.geometry("600x50")
            top.title("An error has occured")
            text = Label(top, text= msg)
            text.pack()

        def foreground(func, args):
            try: 
                func(*args)
            except Exception as error:
                open_popup("The following error was returned: {error}".format(error = error))

        def background(func, args):
            th = threading.Thread(target=func, args=args, daemon=False)
            th.start()
            
        def format_keys(keys):
            formatted_keys = []
            for key,value in keys.items():
                formatted_keys.append("Key = {key}, File = {file}\n".format(key = key, file = value))
            return formatted_keys

        def update_keys_box(keys_box):
            keys = format_keys(backend.get_keys())
            keys_box.delete(0,END)
            for index, key in enumerate(keys):
                keys_box.insert(index,key)

        def add_components():
            win.rowconfigure(0,weight=3)

            #Add ShareLink button
            add_menu_share_label = Label(win, text="Add Right-Click LocalLink option on files.")
            add_menu_share = Button(win,text='Enable LocalLink', command = lambda : foreground(backend.add_menu_option, ()))
            add_menu_share_label.grid(row=0, column=0, sticky=W, padx=PADX, pady=PADY)#
            add_menu_share.grid(row=0, column=1, sticky=W, padx=PADX, pady=PADY,)

            #Remove ShareLink button
            add_menu_share_label = Label(win, text="Remove Right-Click LocalLink option on files.")
            add_menu_share = Button(win,text='Disable LocalLink', command = lambda : foreground(backend.remove_menu_option, ()))
            add_menu_share_label.grid(row=1, column=0, sticky=W, padx=PADX, pady=PADY)
            add_menu_share.grid(row=1, column=1, sticky=W, padx=PADX, pady=PADY,)

            #Add file entry and button
            new_key = StringVar()
            add_key_entry = Entry(win, textvariable=new_key, width = 80)
            add_key_button = Button(win,text='Add Key', command = lambda : background(backend.add_key, (new_key.get(),)))
            add_key_entry.grid(row=2, column=0, sticky=W, columnspan=1, padx=PADX, pady=PADY)
            add_key_button.grid(row=2, column=1, sticky=W, padx=PADX, pady=PADY)

            #Refresh keys list button
            refresh_keys_button = Button(win,text='Refresh Keys', command = lambda : background(update_keys_box, (keys_box_area,)))
            refresh_keys_button.grid(row=2, column=2, sticky=W, padx=PADX, pady=PADY)

            #Keys list box
            keys = format_keys(backend.get_keys())
            keys_box_area = Listbox(win, width = 100, height = 10)
            update_keys_box(keys_box_area)
            keys_box_area.grid(row=3, column=0, columnspan=3, padx=PADX, pady=PADY)  

        add_components()
        background(backend.start_flask, ())

        win.protocol('WM_DELETE_WINDOW', hide_window)

        win.mainloop()