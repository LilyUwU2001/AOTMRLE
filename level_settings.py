# import the TKInter library
import tkinter as tk
from tkinter import Toplevel, Canvas, Scale, Label, Button, Frame, ttk
from PIL import Image, ImageTk

# Level settings subwindow
class LevelSettingsWindow:
    def __init__(self, master):
        # Prepare the subwindow
        self.master = master
        self.window = Toplevel(master)
        self.window.title("Level Settings")
        
        # Set up window icon
        ico = Image.open('graphics/settingsicon.png')
        photo = ImageTk.PhotoImage(ico)
        self.window.wm_iconphoto(False, photo)

        # Set window size
        self.window.geometry("350x315")
        
        # Set window position
        main_x, main_y = self.master.winfo_x(), self.master.winfo_y()
        self.window.geometry(f"+{main_x}+{main_y}")
        
        # Disable Maximize and resizing
        self.window.resizable(False, False) 
        
        # Prepare BG color & stage BGM variables
        self.bg_color = self.master.stage_bg_color
        self.stage_bgm = 0
        
        # Create Background Color label
        label = Label(self.window, text="Background Color", font=("MS Sans Serif", 12))
        label.pack(pady=10)
        
        # Create the color picker
        self.create_color_picker()
        
        # Create Level Metadata label
        label = Label(self.window, text="Level Metadata", font=("MS Sans Serif", 12))
        label.pack(pady=10)
        
        # Create level dimensions sliders
        self.create_width_slider(self.window)
        self.create_height_slider(self.window)
        
        # Create music picker
        self.create_music_picker(self.window)
        
        # Create empty label to pad out stuff
        label = Label(self.window, text=" ", font=("MS Sans Serif", 1))
        label.pack(pady=0)
        
        # Create apply button
        apply_button = tk.Button(self.window, width=46, text="Apply changes", command=self.apply_settings)
        apply_button.pack()
        
        # Close window handler
        def on_close():
            # Set object list opened in TilemapViewer parent window class to false
            self.master.level_settings_opened = False
            self.window.destroy()
            
        # Prepare the close window handler
        self.window.protocol("WM_DELETE_WINDOW", on_close)
        
    def create_color_slider(self, channel, target_frame):
        # Create target frame
        frame = Frame(target_frame)
        frame.pack(pady=0, side="top")

        # Create components
        label = tk.Label(frame, width=3, text=channel+":")
        label.pack(side="left")

        slider = tk.Scale(frame, length=192, from_=0, to=1, showvalue=0, resolution=0.01, orient="horizontal")
        slider.pack(side="left")

        value_label = tk.Label(frame, width=3, text="0")
        value_label.pack(side="left")

        # Set starting value
        setattr(self, f"{channel.lower()}_slider", slider)
        setattr(self, f"{channel.lower()}_value_label", value_label)

        # Set update function
        slider.config(command=lambda val, ch=channel: self.update_color_slider(ch, val))

    def update_color_slider(self, channel, value):
        # Update the label for the slider
        label = getattr(self, f"{channel.lower()}_value_label")
        label.config(text=value)
        self.value = value
        self.update_color_display()
        
    def create_color_sliders(self, target_frame):
        # Prepare frame
        frame = Frame(target_frame)
        frame.pack(pady=0, side="left")
        
        # Create sliders separately
        r_slider = self.create_color_slider("R", frame)
        g_slider = self.create_color_slider("G", frame)
        b_slider = self.create_color_slider("B", frame)
        
    def create_color_display(self, target_frame):
        # Prepare frame
        frame = Frame(target_frame)
        frame.pack(padx=16, pady=0, side="left")
        
        # Color preview canvas
        self.color_square_canvas = Canvas(frame, width=42, height=42, bg="#FFFFFF")
        self.color_square_canvas.pack(pady=0)
        
        # Hex color code label
        self.color_code_label = Label(frame, text="#FFFFFF")
        self.color_code_label.pack(pady=0)
        
    def update_color_display(self):
        # Get RGB values of the sliders
        red_value = self.r_slider.get()
        green_value = self.g_slider.get()
        blue_value = self.b_slider.get()

        # Set BG color by converting RGB to hex
        self.bg_color = self.rgb_to_hex(int(red_value*255), int(green_value*255), int(blue_value*255))
        
        # Draw canvas square with defined RGB color
        self.color_square_canvas.configure(bg=self.bg_color)

    def create_color_picker(self):
        # Prepare frame
        frame = Frame(self.window)
        frame.pack(pady=0)
        
        # RGB sliders
        self.create_color_sliders(frame)
        
        # Color display
        self.create_color_display(frame)
        
    def create_width_slider(self, target_frame):
        # Prepare frame
        frame = Frame(target_frame)
        frame.pack(pady=0, side="top")

        # Prepare components
        label = tk.Label(frame, width=8, text="Width:")
        label.pack(side="left")

        slider = tk.Scale(frame, length=250, from_=20, to=999, showvalue=0, resolution=1, orient="horizontal")
        slider.pack(side="left")

        value_label = tk.Label(frame, width=3, text="0")
        value_label.pack(side="left")

        # Set starting value
        setattr(self, f"width_slider", slider)
        setattr(self, f"width_value_label", value_label)

        # Set update function
        slider.config(command=lambda val: self.update_width_slider(val))

    def update_width_slider(self, value):
        # Update the label for the slider
        label = getattr(self, f"width_value_label")
        label.config(text=value)
        self.value = value
        
    def create_height_slider(self, target_frame):
        # Prepare frame
        frame = Frame(target_frame)
        frame.pack(pady=0, side="top")

        # Prepare components
        label = tk.Label(frame, width=8, text="Height:")
        label.pack(side="left")

        slider = tk.Scale(frame, length=250, from_=15, to=999, showvalue=0, resolution=1, orient="horizontal")
        slider.pack(side="left")

        value_label = tk.Label(frame, width=3, text="0")
        value_label.pack(side="left")

        # Set starting value
        setattr(self, f"height_slider", slider)
        setattr(self, f"height_value_label", value_label)

        # Set update function
        slider.config(command=lambda val: self.update_height_slider(val))

    def update_height_slider(self, value):
        # Update the label for the slider
        label = getattr(self, f"height_value_label")
        label.config(text=value)
        self.value = value
        
    def create_music_picker(self, target_frame):
        # Prepare music dropdown menu
        music_label = Label(self.window, text="Choose level music track:")
        music_label.pack(pady=5)

        self.music_options = ["Metallica - Seek & Destroy (music1.ogg)", "Caltron 6-in-1 - Bookyman (music2.ogg)", "Metallica - For Whom the Bell Tolls (music3.ogg)",
                              "Gustav Holst - Mars, the Bringer of War (music4.ogg)"]
        self.selected_music = tk.StringVar(self.window)
        self.selected_music.set(self.music_options[0])  # Set default value
        music_dropdown = ttk.Combobox(self.window, state="readonly", width=51, textvariable=self.selected_music, values=self.music_options)
        music_dropdown.pack(pady=0)
        
    def apply_settings(self):
        # Set BG color
        self.master.stage_bg_color = self.bg_color
        
        # Set level music
        self.stage_bgm = self.music_options.index(self.selected_music.get())
        self.master.stage_bgm = self.stage_bgm
        
        # Set level dimensions
        width_in_tiles = self.width_slider.get()
        self.master.cols = width_in_tiles
        height_in_tiles = self.height_slider.get()
        self.master.rows = height_in_tiles
        
        # Reset scrollbars
        self.master.set_vertical_scrollbar_max(max(height_in_tiles-15,0))
        self.master.set_horizontal_scrollbar_max(max(width_in_tiles-20,0))
        
        # Redraw tilemap
        self.master.redraw_tilemap()
        
    def rgb_to_hex(self, r, g, b):
        # Returns hex from provided R, G and B values
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
if __name__ == "__main__":
    app = tk.Tk()
    level_settings_window = LevelSettingsWindow(app)
    app.mainloop()