# import the TKInter library
import tkinter as tk
from tkinter import Toplevel, Listbox, Scrollbar, SINGLE
from PIL import Image, ImageTk

# Object list subwindow
class ObjectListWindow:
    def __init__(self, master):
        # Prepare the subwindow
        self.master = master
        self.window = Toplevel(master)
        self.window.title("Object List")
        
        # Set up window icon
        ico = Image.open('graphics/objecticon.png')
        photo = ImageTk.PhotoImage(ico)
        self.window.wm_iconphoto(False, photo)
        
        # Set window size
        self.window.geometry("200x150")
        
        # Set window position
        main_x, main_y = self.master.winfo_x(), self.master.winfo_y()
        self.window.geometry(f"+{main_x}+{main_y}")
        
        # Disable Maximize and resizing
        self.window.resizable(False, False) 

        # Prepare the object list
        self.object_list = Listbox(self.window, selectmode=SINGLE)
        object_names = ["Grass", "Dirt", "Yellow tile / Bridge part", "Building - Yellow flat", "Building - Pink flat", "Building - Gray flat", "Building - Green flat",
                        "Billboard - No Martians", "Billboard - Mat&Pat", "Billboard - Love2D", "Billboard - Zielone Pole", "UFO - Top left", "UFO - Top mid",
                        "UFO - Top right", "UFO - Bottom left", "UFO - Bottom mid", "UFO - Bottom right", "Martian - Green", "Martian - Pink", "Martian - Blue",
                        "Martian - Red", "Martian - Green (-64px)", "Martian - Pink (-64px)", "Martian - Blue (-64px)", "Martian - Red (-64px)", "Player start",
                        "Medkit", "1UP", "Spike - top", "Spike - bottom", "Level end sign", "Toll booth", "Building - Green fire", "Building - Pink fire",
                        "Building - Gray fire", "Duplicate - Green fire", "Ashes", "Dead man", "Mars ground", "Mars dirt", "Mars base piece"]
        
        # Add all the objects in the game to the listbox
        for name in object_names:
            self.object_list.insert(tk.END, name)
            
        # Pack the object list
        self.object_list.pack(side="left", fill="both", expand=True)
        
        # Add a vertical scrollbar to the list
        scrollbar = Scrollbar(self.window, command=self.object_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.object_list.config(yscrollcommand=scrollbar.set)
        
        # Close window handler
        def on_close():
            # Set object list opened in TilemapViewer parent window class to false
            self.master.object_list_opened = False
            self.window.destroy()
            
        # Prepare the close window handler
        self.window.protocol("WM_DELETE_WINDOW", on_close)
        
        # Bind the object selection to left click
        self.object_list.bind("<ButtonRelease-1>", self.select_object_from_list)
        
    # Select object from list
    def select_object_from_list(self, event):
        selected_index = self.object_list.curselection()
        if selected_index:
            selected_object_id = self.object_list.curselection()[0]+1
            self.master.set_main_id(selected_object_id)
        
if __name__ == "__main__":
    app = tk.Tk()
    level_settings_window = ObjectListWindow(app)
    app.mainloop()