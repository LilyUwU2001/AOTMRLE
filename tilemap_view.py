# import the TKInter library
import tkinter as tk
from tkinter import Canvas, Scale, Toplevel, Listbox, Menu
from PIL import Image, ImageTk

# import other classes
from object_list import ObjectListWindow
from level_settings import LevelSettingsWindow

# Tilemap Viewer class
class TilemapViewer(tk.Tk):
    def __init__(self, tilemap, tile_size, stage_bg, stage_bgm, view_width, view_height):
        # Set up the window
        super().__init__()
        self.title("AOTMRLE - Attack of the Martians Remastered Level Editor")
        self.resizable(False, False) 
        
        # Set up window icon
        ico = Image.open('graphics/editoricon.png')
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)
        
        self.object_list_opened = False
        self.level_settings_opened = False
        
        self.tilemap = tilemap
        self.tile_size = tile_size
        self.rows = len(tilemap)
        self.cols = len(tilemap[0])
        
        self.view_width = view_width
        self.view_height = view_height
        self.start_row = 0
        self.start_col = 0
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=False)
        
        # Zmienne przechowujące wartość liczników
        global horizontal_counter_var, vertical_counter_var
        horizontal_counter_var = tk.IntVar()
        vertical_counter_var = tk.IntVar()

        # Ustawienie początkowej wartości liczników na 0
        horizontal_counter_var.set(0)
        vertical_counter_var.set(0)

        self.add_scrollbars()
        
        self.canvas = Canvas(self.container, width=self.view_width * tile_size, height=self.view_height * tile_size)
        self.canvas.pack(side="left", fill="both", expand=False)  # Ustawienie expand na False

        self.stage_bg_color = stage_bg
        self.stage_bgm = stage_bgm

        self.load_tile_images()
        
        self.redraw_tilemap()
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.add_menu()

    def draw_background(self):
        self.canvas.create_rectangle(0, 0, self.view_width * self.tile_size, self.view_height * self.tile_size,
                                     fill=self.stage_bg_color, outline="")

    def load_tile_images(self):
        self.tile_images = {}
        for row in self.tilemap:
            for tile_id in row:
                if tile_id not in self.tile_images:
                    image_path = f"graphics/tile{tile_id}.png"  # Adjust the file naming convention
                    tile_image = Image.open(image_path)
                    self.tile_images[tile_id] = ImageTk.PhotoImage(tile_image)

    def draw_tilemap(self):
        for row_index in range(self.start_row-10, self.start_row + self.view_height):
            for col_index in range(self.start_col-10, self.start_col + self.view_width):
                if 0 <= row_index < self.rows and 0 <= col_index < self.cols:
                    x = (col_index - self.start_col) * self.tile_size
                    y = (row_index - self.start_row) * self.tile_size
                    tile_id = self.tilemap[row_index][col_index]
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.tile_images[tile_id])
        
    def add_scrollbars(self):
        global v_scrollbar, h_scrollbar  # Globalne zmienne, aby móc odwoływać się do nich w innych miejscach kodu
        v_scrollbar = Scale(self.container, from_=0, to=max(self.rows-15,0), showvalue=0, orient="vertical", command=self.update_vertical_counter)
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = Scale(self.container, from_=0, to=max(self.cols-20,0), showvalue=0, orient="horizontal", command=self.update_horizontal_counter)
        h_scrollbar.pack(side="bottom", fill="x")
        
    def set_vertical_scrollbar_max(self, value):
        v_scrollbar.config(to=value)

    def set_horizontal_scrollbar_max(self, value):
        h_scrollbar.config(to=value)
        
    def add_menu(self):
        # Add the menu bar
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        window_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Window", menu=window_menu)
        window_menu.add_command(label="Object List", command=self.open_object_list)
        window_menu.add_command(label="Level Settings", command=self.open_level_settings)
        
    def scroll_y(self, value):
        self.start_row = int(value)
        self.redraw_tilemap()

    def scroll_x(self, value):
        self.start_col = int(value)
        self.redraw_tilemap()
        
    def update_horizontal_counter(self, *args):
        # Aktualizuje wartość licznika na podstawie wartości poziomego scrollbara
        new_value = int(h_scrollbar.get())
        horizontal_counter_var.set(new_value)
        self.scroll_x(new_value)

    def update_vertical_counter(self, *args):
        # Aktualizuje wartość licznika na podstawie wartości pionowego scrollbara
        new_value = int(v_scrollbar.get())
        vertical_counter_var.set(new_value)
        self.scroll_y(new_value)

    def redraw_tilemap(self):
        self.canvas.delete("all")
        self.draw_background()
        self.draw_tilemap()

    def on_canvas_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def open_object_list(self):
        if not self.object_list_opened:
            self.object_list_opened = True
            ObjectListWindow(self)
            
    def open_level_settings(self):
        if not self.level_settings_opened:
            self.level_settings_opened = True
            LevelSettingsWindow(self)