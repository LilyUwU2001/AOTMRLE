# import the TKInter library
import tkinter as tk
from tkinter import Canvas, Scale, Toplevel, Listbox, Menu, Frame
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
        
        # Subwindow opened variables
        self.object_list_opened = False
        self.level_settings_opened = False
        
        # Tilemap variables
        self.tilemap = tilemap
        self.tile_size = tile_size
        self.rows = len(tilemap)
        self.cols = len(tilemap[0])
        self.tile_num = 41
        
        # View width & height
        self.view_width = view_width
        self.view_height = view_height
        self.start_row = 0
        self.start_col = 0
        
        # Prepare container
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=False)
        
        # Store scrolling counter values
        global horizontal_counter_var, vertical_counter_var
        horizontal_counter_var = tk.IntVar()
        vertical_counter_var = tk.IntVar()

        # Set scrolling counter values to 0
        horizontal_counter_var.set(0)
        vertical_counter_var.set(0)
        
        # Variable with selected object ID
        self.selected_id = 0

        # Add scrollbars
        self.add_scrollbars()
        
        # Prepare canvas
        self.canvas = Canvas(self.container, width=self.view_width * tile_size, height=self.view_height * tile_size)
        self.canvas.pack(side="left", fill="both", expand=False)  # Set expand to False

        # Default stage BG color and BGM defined by level data file
        self.stage_bg_color = stage_bg
        self.stage_bgm = stage_bgm

        # Load all tile images
        self.load_tile_images()
        
        # Redraw the tilemap
        self.redraw_tilemap()
        
        # Configure the canvas scrolling functions
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Bind events to canvas
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<Button-1>", self.place_object_left_click)
        self.canvas.bind("<Button-3>", self.place_object_right_click)
        
        # Add the top bar menu
        self.add_menu()

    def draw_background(self):
        # Draw the background in the stage BG color
        self.canvas.create_rectangle(0, 0, self.view_width * self.tile_size, self.view_height * self.tile_size,
                                     fill=self.stage_bg_color, outline="")

    def load_tile_images(self):
        # Load all tile images
        self.tile_images = {}
        for tile_id in range(0, self.tile_num):
            image_path = f"graphics/tile{tile_id}.png"
            tile_image = Image.open(image_path)
            self.tile_images[tile_id] = ImageTk.PhotoImage(tile_image)

    def draw_tilemap(self):
        # Draw the entire tilemap. Start 10 tiles earlier, to include buildings etc.
        # For each row and column, if it's valid...
        for row_index in range(self.start_row-10, self.start_row + self.view_height):
            for col_index in range(self.start_col-10, self.start_col + self.view_width):
                if 0 <= row_index < self.rows and 0 <= col_index < self.cols:
                    # Compute the place on the canvas to draw the tile, including the scrolling...
                    x = (col_index - self.start_col) * self.tile_size
                    y = (row_index - self.start_row) * self.tile_size
                    # Get the tile ID to draw...
                    tile_id = self.tilemap[row_index][col_index]
                    # And draw the tile!
                    self.canvas.create_image(x, y, anchor=tk.NW, image=self.tile_images[tile_id])
        
    def add_scrollbars(self):
        global v_scrollbar, h_scrollbar  # Global variables for scrollbars, to refer in various places in the code
        # Prepare the vertical scrollbar
        v_scrollbar = Scale(self.container, from_=0, to=max(self.rows-15,0), showvalue=0, orient="vertical", command=self.update_vertical_counter)
        v_scrollbar.pack(side="right", fill="y")
        
        # Prepare the horizontal scrollbar
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
        # Updates the horizontal scrollbar X counter
        new_value = int(h_scrollbar.get())
        horizontal_counter_var.set(new_value)
        self.scroll_x(new_value)

    def update_vertical_counter(self, *args):
        # Updates the vertical scrollbar Y counter
        new_value = int(v_scrollbar.get())
        vertical_counter_var.set(new_value)
        self.scroll_y(new_value)

    def redraw_tilemap(self):
        # Delete everything from canvas and redraw the BG and the tilemap
        self.canvas.delete("all")
        self.draw_background()
        self.draw_tilemap()
        
    def set_main_id(self, selected_object_id):
        # Setting the ID of the object as selected in tilemap_view
        self.selected_id = selected_object_id
        
    def place_object_left_click(self, event):
        # Place object (left click = selected ID)
        self.place_object(event, self.selected_id)

    def place_object_right_click(self, event):
        # Place object (right click = ID 0)
        self.place_object(event, 0)
        
    def place_object(self, event, object):
        # Determine the column and row IDs. Include the scroll
        col = event.x // self.tile_size + horizontal_counter_var.get()
        row = event.y // self.tile_size + vertical_counter_var.get()

        # Check, if the click is in map area
        if 0 <= row < self.rows and 0 <= col < self.cols:
            # Check if tile size > 0
            if self.tile_size > 0:
                # Set the object ID on the map to the defined one
                self.tilemap[row][col] = object
                # Redraw the tilemap
                self.redraw_tilemap()

    def on_canvas_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def open_object_list(self):
        # Open object list if not open
        if not self.object_list_opened:
            self.object_list_opened = True
            ObjectListWindow(self)
            
    def open_level_settings(self):
        # Open level settings if not open
        if not self.level_settings_opened:
            self.level_settings_opened = True
            LevelSettingsWindow(self)