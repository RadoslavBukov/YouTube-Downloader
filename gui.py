"""

"""
import os
import tkinter
import customtkinter
# from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from proglog import ProgressBarLogger
from pytube import YouTube
import logging
from tkinterweb import HtmlFrame
from backend import (find_url_by_name, download_youtube_video, download_youtube_audio, download_playlist,
                     get_video_quality_options, extract_thumbnail_from_url, get_value_from_json, get_video_name)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
# Configure MoviePy logger to capture progress messages
logger = logging.getLogger('moviepy')
logger.setLevel(logging.INFO)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # static files
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
        self.logo_path = os.path.join(script_dir, 'static_files', 'logo.jpg')
        self.youtube_frame_path = os.path.join(script_dir, 'static_files', 'empty_frame.jpg')
        self.default_img_active = True
        self.youtube_url = "www.google.com/search"
        self.url_playlist = False
        self.video_url_name = ""
        self.quality_options = []

        self.audio_format_options_dict = get_value_from_json("supported_audio_file_types")
        self.audio_format_options = list(self.audio_format_options_dict.keys())
        self.video_format_options = get_value_from_json("supported_video_file_types")

        # configure window
        self.title("YouTube Downloader")
        self.geometry(f"{1300}x{750}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

# SECTION - Sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="YouTube",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=2, pady=(20, 0))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Downloader",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=2, pady=(0, 20))
        # Load and display logo image
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(self.logo_path),
                                                 dark_image=Image.open(self.logo_path), size=(150, 150))
        self.logo_label_img = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.logo_label_img.grid(row=2, column=0, rowspan=2, padx=10, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_options = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                   values=["Light", "Dark", "System"],
                                                                   command=self.change_appearance_mode_event)
        self.appearance_mode_options.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_options = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                           values=["80%", "90%", "100%", "110%", "120%"],
                                                           command=self.change_scaling_event)
        self.scaling_options.grid(row=8, column=0, padx=20, pady=(10, 20))

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
                                                          border_width=1, text_color=("gray10", "#DCE4EE"),
                                                          command=self.loading_find_url_by_artist_name)
        self.search_button_name.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.loading_1 = customtkinter.CTkLabel(self.tabview.tab("by Name"), text="Loading...",
                                                font=("Helvetica", 16, "bold"), text_color="#2fa572")
        self.loading_1.grid(row=2, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

        # Tab by URL
        self.url_input = customtkinter.CTkEntry(self.tabview.tab("by URL"), placeholder_text="YouTube URL")
        self.url_input.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.search_button_url = customtkinter.CTkButton(self.tabview.tab("by URL"), text="Search:",
                                                         border_width=1, text_color=("gray10", "#DCE4EE"),
                                                         command=lambda: self.loading_update_url(self.url_input.get(),
                                                                                                 False))
        self.search_button_url.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.playlist_url_input = customtkinter.CTkEntry(self.tabview.tab("by URL"),
                                                         placeholder_text="YouTube Playlist URL")
        self.playlist_url_input.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.search_button_playlist_url = customtkinter.CTkButton(self.tabview.tab("by URL"), text="Search:",
                                                                  border_width=1, text_color=("gray10", "#DCE4EE"),
                                                                  command=lambda: self.loading_update_url
                                                                  (self.playlist_url_input.get(), True))
        self.search_button_playlist_url.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.loading_2 = customtkinter.CTkLabel(self.tabview.tab("by URL"), text="Loading...",
                                                font=("Helvetica", 16, "bold"), text_color="#2fa572")
        self.loading_2.grid(row=2, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

# SECTION - Options frame
        self.options_frame = customtkinter.CTkFrame(self)
        self.options_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # Select format
        self.label_format = customtkinter.CTkLabel(self.options_frame, text="Select format: ",
                                                   font=("Helvetica", 16, "bold"))
        self.label_format.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")

        # Audio format selection
        self.select_audio_format = customtkinter.CTkOptionMenu(self.options_frame,
                                                               # fg_color="#343638",
                                                               # button_color="#565b5e",
                                                               values=self.audio_format_options,
                                                               command=self.update_options_video)
        self.select_audio_format.grid(row=0, column=1, padx=20, sticky="s")
        # Video format selection
        self.select_video_format = customtkinter.CTkOptionMenu(self.options_frame,
                                                               # fg_color="#343638",
                                                               # button_color="#565b5e",
                                                               values=self.video_format_options,
                                                               command=self.update_options_audio)
        self.select_video_format.grid(row=0, column=2, padx=20, sticky="s")

        # Select quality
        self.quality_var = tkinter.IntVar(value=0)
        self.label_quality_group = customtkinter.CTkLabel(master=self.options_frame, text="Select quality:",
                                                          font=("Helvetica", 16, "bold"))
        self.label_quality_group.grid(row=2, column=0, padx=20, pady=(20, 60), sticky="w")

        # Select trim
        self.label_trim = customtkinter.CTkLabel(self.options_frame, text="Select trim: (min:sec)",
                                                 font=("Helvetica", 16, "bold"))
        self.label_trim.grid(row=5, column=0, columnspan=2, padx=20, pady=(40, 10), sticky="w")

        # Start time input
        self.start_input = customtkinter.CTkEntry(self.options_frame, placeholder_text="Start time (00:00)")
        self.start_input.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.end_input = customtkinter.CTkEntry(self.options_frame, placeholder_text="End time (00:00)")
        self.end_input.grid(row=6, column=1, padx=20, pady=(0, 20), sticky="nsew")

# SECTION - Visualisation frame
        self.visualisation_frame = customtkinter.CTkFrame(self)
        self.visualisation_frame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # Result
        # self.label_result = customtkinter.CTkLabel(self.visualisation_frame, text="Search result: ",
        #                                            font=("Helvetica", 16, "bold"))
        # self.label_result.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="w")

        # Load and display the default image initially
        self.default_image = Image.open(self.youtube_frame_path)
        self.default_image = self.default_image.resize((500, 300), Image.LANCZOS)
        self.default_img = ImageTk.PhotoImage(self.default_image)

        self.thumbnail_label = customtkinter.CTkLabel(self.visualisation_frame, image=self.default_img, text="")
        self.thumbnail_label.image = self.default_img
        self.thumbnail_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5))

        # URL Video Preview
        # self.youtube_frame = HtmlFrame(self.visualisation_frame)
        # self.youtube_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 5))
        # self.youtube_frame.load_website(self.youtube_url)

        self.label_video_name = customtkinter.CTkLabel(self.visualisation_frame, text=self.video_url_name,
                                                       font=("Helvetica", 16, "bold"))
        self.label_video_name.grid(row=2, column=0, padx=30, pady=5, sticky="wn")

        self.slider_preview = customtkinter.CTkSlider(self.visualisation_frame, from_=0, to=1, number_of_steps=18)
        self.slider_preview.grid(row=3, column=0, padx=20, columnspan=2, sticky="ew")
        self.play_button = customtkinter.CTkButton(self.visualisation_frame, text="Play", fg_color="transparent",
                                                   border_width=0, text_color=("gray10", "#DCE4EE"))
        self.play_button.grid(row=4, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        self.pause_button = customtkinter.CTkButton(self.visualisation_frame, text="Pause", fg_color="transparent",
                                                    border_width=0, text_color=("gray10", "#DCE4EE"))
        self.pause_button.grid(row=4, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")

# SECTION - Download frame
        self.download_frame = customtkinter.CTkFrame(self)
        self.download_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_result = customtkinter.CTkLabel(self.download_frame, text="Download to: ",
                                                   font=("Helvetica", 16, "bold"))
        self.label_result.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        # Create entry to display selected path
        self.download_path = customtkinter.CTkEntry(self.download_frame, width=250)
        self.download_path.grid(row=1, column=0, padx=(20, 5), pady=20, sticky="w")

        # Create browse button
        self.browse_button = customtkinter.CTkButton(self.download_frame, text="Browse", fg_color="transparent",
                                                     border_width=1, text_color=("gray10", "#DCE4EE"),
                                                     command=self.browse_folder)
        self.browse_button.grid(row=1, column=1, padx=(0, 20), pady=20, sticky="e")

        # Create download button
        self.download_button = customtkinter.CTkButton(self.download_frame, text="DOWNLOAD",
                                                       command=self.loading_download_media, height=50)
        self.download_button.grid(row=2, column=0, columnspan=5, rowspan=2, padx=20, pady=(20, 0), sticky="nsew")
        # self.loadingbar = customtkinter.CTkProgressBar(self.download_frame)
        # self.loadingbar.grid(row=3, column=0, columnspan=2, padx=20, pady=(20, 20), sticky="nsew")
        self.loading = customtkinter.CTkLabel(self.download_frame, text="Loading...", font=("Helvetica", 16, "bold"),
                                              text_color="#2fa572")
        self.loading.grid(row=3, column=0, columnspan=2, padx=0, pady=10, sticky="nsew")

        self.progress_label = customtkinter.CTkLabel(self.download_frame, text="Progress:")
        self.progress_label.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="w")

        self.progress_bar = customtkinter.CTkProgressBar(self.download_frame, mode='determinate')
        self.progress_bar.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="w")

# SECTION Initial states:
        self.play_button.configure(state="disabled")
        self.pause_button.configure(state="disabled")
        self.slider_preview.configure(state="disabled")
        self.download_button.configure(state="disabled")
        self.appearance_mode_options.set("Dark")
        self.scaling_options.set("100%")
        self.select_audio_format.set("Audio:")
        self.select_video_format.set("Video:")
        self.loading.grid_remove()
        self.loading_1.grid_remove()
        self.loading_2.grid_remove()
        # self.loadingbar.configure(mode="indeterminnate")
        # self.loadingbar.stop()

# SECTION - Methods
    def loading_find_url_by_artist_name(self):
        self.loading_1.grid()
        self.loading_1.after(100, lambda: self.find_url_by_artist_name())

    def find_url_by_artist_name(self):
        artist = self.name_input.get()
        title = self.title_input.get()
        self.youtube_url = find_url_by_name(artist, title)
        self.update_url(self.youtube_url, False)
        self.loading_1.grid_remove()

    def loading_update_url(self, url, playlist):
        self.loading_2.grid()
        self.loading_2.after(100, lambda: self.update_url(url, playlist))

    def update_url(self, url, playlist):
        # TODO: Check the validity of url here, and remove Loading if its not valid
        # Check if the URL is a valid YouTube URL
        try:
            yt = YouTube(url)
            # Assuming no exceptions raised, URL is valid
        except Exception as e:
            messagebox.showerror("Error", f"Invalid YouTube URL: {str(e)}")
            self.loading_2.grid_remove()
            return



        if playlist:
            self.url_playlist = True
        else:
            self.url_playlist = False

        self.youtube_url = url
        self.video_url_name = get_video_name(url)
        self.label_video_name.configure(text=self.video_url_name)
        self.update_search_result(url)
        self.update_quality_options(url)
        self.loading_2.grid_remove()

    def update_search_result(self, url):
        try:
            image = extract_thumbnail_from_url(url)
            img = ImageTk.PhotoImage(image)
            self.default_img_active = False
            self.youtube_url = url
        except Exception as e:
            messagebox.showerror("Error", f"Wrong URL: {str(e)}")
            # CTkMessagebox(master=self, title="Error", message="Error URL", icon="cancel")
            default_image = Image.open(self.youtube_frame_path)
            default_image = default_image.resize((500, 300), Image.LANCZOS)
            img = ImageTk.PhotoImage(default_image)
            self.default_img_active = True

        self.thumbnail_label.configure(image=img)
        self.thumbnail_label.image = img

        if self.default_img_active:
            self.play_button.configure(state="disabled")
            self.pause_button.configure(state="disabled")
            self.slider_preview.configure(state="disabled")
            self.download_button.configure(state="disabled")
        else:
            self.play_button.configure(state="normal")
            self.pause_button.configure(state="normal")
            self.slider_preview.configure(state="normal")
            self.download_button.configure(state="normal")

    def update_quality_options(self, url):
        self.quality_options = get_video_quality_options(url)
        # sorted_qualiti_options = sorted(self.quality_options, key=self.extract_resolution)

        # Add new radio buttons based on quality options
        for i, quality in enumerate(self.quality_options):
            row = 3 + i // 3
            col = i % 3
            radio_button = customtkinter.CTkRadioButton(master=self.options_frame,
                                                        text=f"{quality}",
                                                        variable=self.quality_var,
                                                        value=i)
            radio_button.grid(row=row, column=col, pady=5, padx=1, sticky="n")
            # self.radio_buttons.append(radio_button)

        # Ensure the grid layout adjusts accordingly
        for col in range(3):
            self.options_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        self.label_quality_group.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")

    def update_options_audio(self, value=None):
        self.select_audio_format.set("Audio:")

    def update_options_video(self, value=None):
        self.select_video_format.set("Video:")

    def loading_download_media(self):
        self.loading.grid()
        # self.loadingbar.start()
        # self.loadingbar.after(200, lambda: self.download_media())

    def download_media(self):
        selected_audio_format = self.select_audio_format.get()
        selected_video_format = self.select_video_format.get()
        selected_quality = self.quality_var.get()
        download_folder = self.download_path.get()

        if not download_folder:
            messagebox.showerror("Error", "Please select a download folder.")
            return

        if selected_audio_format == "Audio:" and selected_video_format == "Video:":
            messagebox.showerror("Error", "Please select either audio or video format.")
            return

        if selected_audio_format == "Audio:":
            audio_file = False
            file_format = selected_video_format
        else:
            audio_file = True
            file_format = selected_audio_format

        if self.url_playlist:
            download_function = download_playlist
        else:
            if audio_file:
                download_function = download_youtube_audio
            else:
                download_function = download_youtube_video

        selected_quality = self.quality_options[selected_quality]

        start_time = self.start_input.get()
        end_time = self.end_input.get()

        try:
            # Download function with progress callback
            yt = YouTube(self.youtube_url, on_progress_callback=self.update_progress_bar)

            if audio_file:
                download_function(yt, download_folder, file_format, start_time, end_time)
            else:
                download_function(yt, download_folder, file_format, selected_quality, start_time,
                                  end_time)
            messagebox.showinfo("Success", "Download completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download media: {str(e)}")

        # self.loadingbar.stop()
        self.loading.grid_remove()

    def update_progress_bar(self, stream, chunk, remaining):
        # Calculate the percentage of the file that has been downloaded
        progress = int((1 - remaining / stream.filesize) * 100)
        self.progress_bar['value'] = progress


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path.delete(0, customtkinter.END)
            self.download_path.insert(0, folder_selected)





if __name__ == "__main__":
    app = App()
    app.mainloop()
