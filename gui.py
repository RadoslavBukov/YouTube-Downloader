import os
import tkinter
import webbrowser
import customtkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pytube import YouTube
from PIL import Image, ImageTk
from io import BytesIO
import requests
from backend import find_url_by_name, download_youtube_video, download_youtube_audio, get_video_quality_options, extract_thumbnail_from_url


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # static files
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
        self.logo_path = os.path.join(script_dir, 'static_files', 'logo.jpg')
        self.youtube_frame_path = os.path.join(script_dir, 'static_files', 'empty_frame.jpg')
        default_img = True
        self.youtube_url = ""
        self.quality_options = []

        # configure window
        self.title("YouTube Downloader")
        self.geometry(f"{1200}x{650}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

# SECTION - Sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="YouTube", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=2, pady=(20, 0))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Downloader",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=2, pady=(0, 20))
        # Load and display logo image
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(self.logo_path), dark_image=Image.open(self.logo_path),
                                       size=(150, 150))
        self.logo_label_img = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.logo_label_img.grid(row=2, column=0, rowspan=2, padx=10, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

# SECTION - Search Section with TabView's
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("by Name")
        self.tabview.add("by URL")
        self.tabview.tab("by Name").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("by URL").grid_columnconfigure(0, weight=1)

        # Tab by Name
        self.name_input = customtkinter.CTkEntry(self.tabview.tab("by Name"), placeholder_text="Artist")
        self.name_input.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.title_input = customtkinter.CTkEntry(self.tabview.tab("by Name"), placeholder_text="Title")
        self.title_input.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.name = self.name_input.get()
        self.title = self.title_input.get()
        self.search_button_name = customtkinter.CTkButton(self.tabview.tab("by Name"), text="Search",
                                                     border_width=2, text_color=("gray10", "#DCE4EE"), command=self.find_url_by_artist_name)
        self.search_button_name.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Tab by URL
        self.url_input = customtkinter.CTkEntry(self.tabview.tab("by URL"), placeholder_text="YouTube URL")
        self.url_input.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.search_button_url = customtkinter.CTkButton(self.tabview.tab("by URL"), text="Search:",
                                                     border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.update_thumbnail(self.url_input.get()))
        self.search_button_url.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.playlist_url_input = customtkinter.CTkEntry(self.tabview.tab("by URL"), placeholder_text="YouTube Playlist URL")
        self.playlist_url_input.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.search_button_playlist_url = customtkinter.CTkButton(self.tabview.tab("by URL"), text="Search:",
                                                         border_width=2, text_color=("gray10", "#DCE4EE"), command=lambda: self.update_thumbnail(self.url_input.get()))
        self.search_button_playlist_url.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

# SECTION - Options frame
        self.options_frame = customtkinter.CTkFrame(self)
        self.options_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # Select format
        self.label_format = customtkinter.CTkLabel(self.options_frame, text="Select format: ", font=("Helvetica", 16, "bold"))
        self.label_format.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        self.options_audio = customtkinter.CTkComboBox(self.options_frame,
                                                          values=[".mp3", ".was", ".aac", ".ogg", ".flac"])
        self.options_audio.grid(row=0, column=1, padx=20, sticky="s")
        self.options_video = customtkinter.CTkComboBox(self.options_frame,
                                                          values=[".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"])
        self.options_video.grid(row=0, column=2, padx=20, sticky="s")
            # Select quality
        self.radio_var = tkinter.IntVar(value=0)
        self.label_quality_group = customtkinter.CTkLabel(master=self.options_frame, text="Select quality:", font=("Helvetica", 16, "bold"))
        self.label_quality_group.grid(row=2, column=0, padx=20, pady=(20, 60), sticky="w")


            # Select trim
        self.label_trim = customtkinter.CTkLabel(self.options_frame, text="Select trim: (min:sec)", font=("Helvetica", 16, "bold"))
        self.label_trim.grid(row=5, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="w")

        # Start time input
        self.start_input = customtkinter.CTkEntry(self.options_frame, width=10, placeholder_text="Start time (00:00)")
        self.start_input.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.end_input = customtkinter.CTkEntry(self.options_frame, width=10, placeholder_text="End time (00:00)")
        self.end_input.grid(row=6, column=1, padx=20, pady=(0, 20), sticky="nsew")

# SECTION - Visualisation frame
        self.visualisation_frame = customtkinter.CTkFrame(self)
        self.visualisation_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
            # Result
        self.label_result = customtkinter.CTkLabel(self.visualisation_frame, text="Search result: ", font=("Helvetica", 16, "bold"))
        self.label_result.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="w")

        # Load and display the default image initially
        default_image = Image.open(self.youtube_frame_path)
        default_image = default_image.resize((500, 300), Image.LANCZOS)
        default_img = ImageTk.PhotoImage(default_image)

        self.thumbnail_label = customtkinter.CTkLabel(self.visualisation_frame, image=default_img, text="")
        self.thumbnail_label.image = default_img
        self.thumbnail_label.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        self.slider_preview = customtkinter.CTkSlider(self.visualisation_frame, from_=0, to=1, number_of_steps=18)
        self.slider_preview.grid(row=2, column=0, padx=20, columnspan=2, sticky="ew")
        self.play_button = customtkinter.CTkButton(self.visualisation_frame, text="Play", fg_color="transparent",
                                                     border_width=0, text_color=("gray10", "#DCE4EE"))
        self.play_button.grid(row=3, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.pause_button = customtkinter.CTkButton(self.visualisation_frame, text="Pause", fg_color="transparent",
                                                     border_width=0, text_color=("gray10", "#DCE4EE"))
        self.pause_button.grid(row=3, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")

# SECTION - Download frame
        self.download_frame = customtkinter.CTkFrame(self)
        self.download_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_result = customtkinter.CTkLabel(self.download_frame, text="Download to: ", font=("Helvetica", 16, "bold"))
        self.label_result.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        # Create entry to display selected path
        self.download_path = customtkinter.CTkEntry(self.download_frame, width=200)
        self.download_path.grid(row=1, column=0, padx=(20, 5), pady=20, sticky="w")

        # Create browse button
        self.browse_button = customtkinter.CTkButton(self.download_frame, text="Browse", fg_color="transparent",
                                                     border_width=1, text_color=("gray10", "#DCE4EE"), command=self.browse_folder)
        self.browse_button.grid(row=1, column=1, padx=(0, 20), pady=20, sticky="e")
        # Create browse button
        self.browse_button = customtkinter.CTkButton(self.download_frame, text="DOWNLOAD", command=self.browse_folder, width=100, height=50)
        self.browse_button.grid(row=3, column=0, columnspan=2, rowspan=2, padx=20, pady=(50, 20), sticky="nsew")

        # Initial states:
        self.play_button.configure(state="disabled")
        self.pause_button.configure(state="disabled")
        self.slider_preview.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.options_audio.set("Audio:")
        self.options_video.set("Video:")

# SECTION - Methods
    def find_url_by_artist_name(self):
        artist = self.name_input.get()
        title = self.title_input.get()
        self.youtube_url = find_url_by_name(artist, title)
        self.update_thumbnail(self.youtube_url)

    def update_thumbnail(self, url):
        try:
            image = extract_thumbnail_from_url(url)
            img = ImageTk.PhotoImage(image)
            self.default_img = False
            self.youtube_url = url
            self.update_quality_options(url) #Todo: not right place
        except Exception as e:
            messagebox.showerror("Error", "Wrong URL.")
            default_image = Image.open(self.youtube_frame_path)
            default_image = default_image.resize((500, 300), Image.LANCZOS)
            img = ImageTk.PhotoImage(default_image)
            self.default_img = True

        self.thumbnail_label.configure(image=img)
        self.thumbnail_label.image = img

        if self.default_img:
            self.play_button.configure(state="disabled")
            self.pause_button.configure(state="disabled")
            self.slider_preview.configure(state="disabled")
        else:
            self.play_button.configure(state="normal")
            self.pause_button.configure(state="normal")
            self.slider_preview.configure(state="normal")


    def update_quality_options(self, url):
        self.quality_options = get_video_quality_options(url)
        # Clear existing radio buttons
        # for radio_button in self.radio_buttons:
        #     radio_button.grid_forget()
        # self.radio_buttons.clear()

        # Add new radio buttons based on quality options
        for i, quality in enumerate(self.quality_options):
            row = 3 + i // 3
            col = i % 3
            radio_button = customtkinter.CTkRadioButton(master=self.options_frame,
                                                        text=f"{quality}p",
                                                        variable=self.radio_var,
                                                        value=i)
            radio_button.grid(row=row, column=col, pady=5, padx=1, sticky="n")
            # self.radio_buttons.append(radio_button)

        # Ensure the grid layout adjusts accordingly
        for col in range(3):
            self.options_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        self.label_quality_group.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path.delete(0, customtkinter.END)
            self.download_path.insert(0, folder_selected)

if __name__ == "__main__":
    app = App()
    app.mainloop()