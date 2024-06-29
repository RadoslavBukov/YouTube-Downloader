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
url = "https://www.youtube.com/watch?v=6Ejga4kJUts"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("YouTube Downloader")
        self.geometry(f"{1200}x{650}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="YouTube", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=2, pady=(20, 0))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Downloader",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=2, pady=(0, 20))
        # Load and display logo image
        image_path = "logo.jpg"  # Replace with your image file path
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path),
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

        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("by Name")
        self.tabview.add("by URL")
        self.tabview.tab("by Name").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("by URL").grid_columnconfigure(0, weight=1)

        # create main entry and button
        # Tab by Name
        self.entry = customtkinter.CTkEntry(self.tabview.tab("by Name"), placeholder_text="Artist")
        self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry = customtkinter.CTkEntry(self.tabview.tab("by Name"), placeholder_text="Title")
        self.entry.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(self.tabview.tab("by Name"), text="Search:",
                                                     border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Tab by URL
        self.entry = customtkinter.CTkEntry(self.tabview.tab("by URL"), placeholder_text="YouTube URL")
        self.entry.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(self.tabview.tab("by URL"), text="Search:",
                                                     border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # Option section
        self.options_frame = customtkinter.CTkFrame(self)
        self.options_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
            # Select format
        self.label_format = customtkinter.CTkLabel(self.options_frame, text="Select format: ")
        self.label_format.grid(row=0, column=0, padx=20, pady=20)

        self.optionmenu_audio = customtkinter.CTkComboBox(self.options_frame,
                                                          values=[".mp3", ".was", ".aac", ".ogg", ".flac"])
        self.optionmenu_audio.grid(row=0, column=1, padx=20)
        self.optionmenu_video = customtkinter.CTkComboBox(self.options_frame,
                                                          values=[".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"])
        self.optionmenu_video.grid(row=0, column=2, padx=20)
            # Select quality
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.options_frame, text="Select quality:")
        self.label_radio_group.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.options_frame, text="320p",
                                                           variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=3, column=0, pady=5, padx=1, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.options_frame, text="480p",
                                                           variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=3, column=1, pady=5, padx=1, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.options_frame, text="720p",
                                                           variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=5, padx=1, sticky="n")
        self.radio_button_4 = customtkinter.CTkRadioButton(master=self.options_frame, text="1080p",
                                                           variable=self.radio_var, value=3)
        self.radio_button_4.grid(row=4, column=0, pady=5, padx=1, sticky="n")
        self.radio_button_5 = customtkinter.CTkRadioButton(master=self.options_frame, text="1440p",
                                                           variable=self.radio_var, value=4)
        self.radio_button_5.grid(row=4, column=1, pady=5, padx=1, sticky="n")
        self.radio_button_6 = customtkinter.CTkRadioButton(master=self.options_frame, text="4k",
                                                           variable=self.radio_var, value=5)
        self.radio_button_6.grid(row=4, column=2, pady=5, padx=1, sticky="n")
        # Configure the columns to have equal weight
        for col in range(3):
            self.options_frame.grid_columnconfigure(col, weight=1, uniform="equal")

            # Select trim
        self.label_trim = customtkinter.CTkLabel(self.options_frame, text="Select trim: ")
        self.label_trim.grid(row=5, column=0, padx=20, pady=20)



        # create visualisation frame
        self.visualisation_frame = customtkinter.CTkFrame(self)
        self.visualisation_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
            # Result
        self.label_result = customtkinter.CTkLabel(self.visualisation_frame, text="Search result: ")
        self.label_result.grid(row=0, column=0, columnspan=2, padx=20)
            # create Visualisation
            # Load image from URL
        self.image = extract_thumbnail_from_url(url)
        img = ImageTk.PhotoImage(self.image)

        self.thumbnail_label = customtkinter.CTkLabel(self.visualisation_frame, image=img)
        self.thumbnail_label.image = img
        self.thumbnail_label.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        self.slider_1 = customtkinter.CTkSlider(self.visualisation_frame, from_=0, to=1, number_of_steps=18)
        self.slider_1.grid(row=2, column=0, padx=20, columnspan=2, sticky="ew")
        self.play_button = customtkinter.CTkButton(self.visualisation_frame, text="Play",
                                                     border_width=1, text_color=("gray10", "#DCE4EE"))
        self.play_button.grid(row=3, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.pause_button = customtkinter.CTkButton(self.visualisation_frame, text="Pause",
                                                     border_width=1, text_color=("gray10", "#DCE4EE"))
        self.pause_button.grid(row=3, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")

        # create download frame
        self.download_frame = customtkinter.CTkFrame(self)
        self.download_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_result = customtkinter.CTkLabel(self.download_frame, text="Download to: ")
        self.label_result.grid(row=0, column=0, padx=20, pady=20)
        # Create entry to display selected path
        self.download_path = customtkinter.CTkEntry(self.download_frame, width=200)
        self.download_path.grid(row=1, column=0, padx=(20, 5), pady=20, sticky="w")

        # Create browse button
        self.browse_button = customtkinter.CTkButton(self.download_frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=1, column=1, padx=(0, 20), pady=20, sticky="e")
        # Create browse button
        self.browse_button = customtkinter.CTkButton(self.download_frame, text="DOWNLOAD", command=self.browse_folder)
        self.browse_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_audio.set("Audio:")
        self.optionmenu_video.set("Video:")

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