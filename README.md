# 🎥 YouTube Downloader

<!-- ![logo](https://raw.githubusercontent.com/RadoslavBukov/YouTube-Downloader/main/static_files/logo.jpg) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/RadoslavBukov/YouTube-Downloader/main/static_files/logo.jpg" alt="logo">
</div>

🎬 **Welcome to the YouTube Downloader!** This application allows you to download YouTube videos and audio easily. This guide will help you understand the features and functionalities of the application. Below, you'll find sections detailing each part of the interface.

## ⭐ Main Features
- 🎨 **Customizable Appearance**: Change the appearance mode and UI scaling to suit your preferences.
- 🔍 **Search by Name or URL**: Find YouTube videos using the artist and title or directly input the YouTube URL.
- 📥 **Download Options**: Choose from various audio and video formats and select the desired quality.
- ✂️ **Trimming**: Specify start and end times to trim the downloaded media.
- 💾 **Download Media**: Download video and audio files in a specific folder.

## 🖼️ Graphical User interface
<div align="center">
  <img src="https://github.com/RadoslavBukov/YouTube-Downloader/blob/main/github_img/GUI_fetched.jpg" alt="gui">
</div>

The main window of the application is divided into several sections:

- 🎛️ **Sidebar**: Contains the logo, appearance settings, and scaling options.
- 🔎 **Search Section**: Allows searching for videos by name or URL.
- ⚙️ **Options Frame**: Select format and quality, and specify trimming options.
- 🖼️ **Visualization Frame**: Displays video thumbnails and allows video preview.
- 📂 **Download Frame**: Specify the download location and initiate downloads.

## 💻 Code Overview

### 📁 static_files
Includes a couple of static images for visualization and a `setup.json` file, which contains settings about the app.

- **setup.json**: Contains configuration settings for the application.

### 🔧 `backend.py`
This script allows users to download video and audio from YouTube with specific requirements for format, quality, and length. It supports operations via a console application interface, making it easy to download content based on various criteria.
#### Block diagram
<div align="center">
  <img src="https://github.com/RadoslavBukov/YouTube-Downloader/blob/main/github_img/backend_blockdiagram.png" alt="block_diagram">
</div>

### 🎨 `gui.py`
The `App` class is a graphical user interface (GUI) application built using `customtkinter` and `tkinter`. This application allows users to search, preview, and download YouTube videos and playlists in various formats and qualities. The app also includes audio playback functionalities.

### 📚 External Libraries
<div align="center">

  | Library           | Usage                                                                                                                                                            |
  |-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | _googleapiclient_ | This is part of the Google API client library used to interact with YouTube's Data API v3. It's specifically used for searching videos based on author and title |
  | _pytube_          | Used for interacting with YouTube. It allows you to fetch video URLs, download video and audio streams, and handle playlists                                     |
  | _moviepy_         | A module for video editing, used here for trimming video files and merging video and audio files                                                                 |
  | _pydub_           | A library for manipulating audio files. It's used here for trimming audio files.                                                                                 |
  | _Pillow_          | Used for handling images, particularly for extracting thumbnails from YouTube video URLs.                                                                        |
  | _customtkinter_   | Used for Graphical User Interface, custom extension around Tkinter, providing additional styling options.                                                        |
  | _pygame_          | Primarily used for audio playback, to play audio files downloaded from YouTube.                                                                                   |
  | _argparse_        | A module for parsing command-line arguments. It's used to create a command-line interface (CLI) for your YouTube downloader so users can specify parameters      |
</div>

## � Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python**: Version 3.8 or higher
- **pip**: Python package manager (typically included with Python)
- **FFmpeg**: Required by moviepy for video/audio processing
  - **Windows**: Download from [FFmpeg official website](https://ffmpeg.org/download.html) or use: `choco install ffmpeg`
  - **Mac**: `brew install ffmpeg`
  - **Linux**: `sudo apt-get install ffmpeg`

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/RadoslavBukov/YouTube-Downloader.git
cd YouTube-Downloader
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python gui.py
```

### 4. Using Console (Optional)
You can also use the application as a console application:
```bash
python backend.py "<YouTube_URL_or_Artist_Name>" "<download_path>" <type> --quality <quality> --start <start_time> --end <end_time>
```

## 📥 Supported Formats

### 🎵 Audio Formats
- MP3, WAV, AAC, OGG, FLAC, M4R

### 🎬 Video Formats
- MP4, AVI, MOV, MKV, FLV, WMV

## 📝 Summary
The provided source code is for a YouTube Downloader application built using the `customtkinter` library for the GUI and various other libraries like `pytube` for downloading YouTube content, `PIL` for image processing, and `pygame` for audio playback. The application allows users to search for YouTube videos by name or URL, preview the video thumbnail, and download videos or audio in various formats and qualities. The application also includes features for customizing the appearance and scaling of the UI.

### ✨ Features
- 🎯 **Search and Download by Name or URL**: Users can search for videos by name or directly input a YouTube URL. The application handles both individual video URLs and playlist URLs.
- 🎬 **Format and Quality Selection**: Users can select the desired audio or video format and choose from available quality options.
- 🖼️ **Thumbnail Preview**: The application displays a thumbnail of the video and allows users to play and pause the downloaded audio.
- ✂️ **Trim Options**: Users can specify start and end times to trim the downloaded media.
- 🎨 **Customizable UI**: The application supports different appearance modes (Light, Dark, System) and UI scaling options.

### 🚀 Conclusion
The YouTube Downloader application is a versatile and user-friendly tool for downloading and previewing YouTube content. It provides a robust set of features that cater to various user needs, from basic video downloads to customized audio trimming. The use of modern libraries like `customtkinter` and `pytube` ensures that the application is both visually appealing and functionally rich.

### 🔮 Future Updates
- 🛡️ **Error Handling Improvements**: Enhance error handling to provide more specific and user-friendly error messages.
- 📊 **Progress Feedback**: Implement a progress bar to give users real-time feedback during the download process.
- 📦 **Batch Download**: Add functionality to support batch downloading of multiple videos at once.

### ⚠️ Troubleshooting

#### Error: `pytube.exceptions.RegexMatchError`
If you encounter the following error:
 ```bash
pytube.exceptions.RegexMatchError: get_throttling_function_name: could not find match for multiple
 ```

This error occurs when `pytube` is unable to parse YouTube's webpage structure due to changes in YouTube's backend.

**Solutions**:
1. **Update pytube to the latest version**:
   ```bash
   pip install --upgrade pytube
   ```
2. **Verify YouTube Status**: Check if there are any ongoing issues affecting video downloads on [YouTube's Status Dashboard](https://www.youtubstatus.com/)
3. **Report the Issue**: If the problem persists, check the [PyTube GitHub Issues](https://github.com/pytube/pytube/issues)

---

## 📂 Project File Structure

```
YouTube-Downloader/
├── backend.py              # Core download and processing logic
├── gui.py                  # Graphical user interface
├── requirements.txt        # Project dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── static_files/          # Static resources
│   ├── setup.json         # Configuration file with API key and format settings
│   ├── logo.jpg           # Application logo
│   └── ...                # Other static images
├── github_img/            # Images for GitHub documentation
│   ├── GUI_fetched.jpg    # GUI screenshot
│   └── backend_blockdiagram.png  # Backend architecture diagram
└── temp_mp3/              # Temporary audio files (created during runtime)
```

## ⚙️ Configuration

The application uses a `setup.json` file located in the `static_files` folder to store configuration settings:

```json
{
  "api_key": "YOUR_YOUTUBE_API_KEY",
  "supported_audio_file_types": {
    "mp3": "libmp3lame",
    "wav": "pcm_s16le",
    "aac": "aac",
    "ogg": "libvorbis",
    "flac": "flac",
    "m4r": "aac"
  },
  "supported_video_file_types": ["mp4", "avi", "mov", "mkv", "flv", "wmv"]
}
```

**Note**: The YouTube API key is already included in the setup.json for basic functionality.

## 📝 How to Use

1. **Launch the Application**: Run `python gui.py`
2. **Search for Videos**: 
   - Use the **"by Name"** tab to search by artist name
   - Use the **"by URL"** tab to paste a YouTube link
3. **Select Download Options**:
   - Choose between Audio or Video format
   - Select desired quality/resolution
4. **Optional - Trim Media**: 
   - Specify start and end times in the trimming options
5. **Choose Download Location**: Click "Browse Folder" to select where to save the file
6. **Download**: Click the "Download" button and wait for completion
7. **Preview**: Use the playback controls to preview downloaded audio

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2024 Radoslav Bukov**

## 👤 Author

**Radoslav Bukov**
- GitHub: [@RadoslavBukov](https://github.com/RadoslavBukov)
- Project Repository: [YouTube-Downloader](https://github.com/RadoslavBukov/YouTube-Downloader)

## 🤝 Contributing

Contributions are welcome! If you find any bugs or have feature suggestions, please:
1. Fork the repository
2. Create a new branch for your feature or fix
3. Make your changes and test thoroughly
4. Submit a pull request with clear description of your changes

## 💬 Support & Feedback

- 🐛 **Found a Bug?** - Report it in [GitHub Issues](https://github.com/RadoslavBukov/YouTube-Downloader/issues)
- 💡 **Have a Feature Idea?** - Create an issue with the `enhancement` label
- ❓ **Need Help?** - Check existing issues or ask in GitHub Discussions

## 📊 Project Status

🟢 **Active Development** - Regular updates and improvements are being made

---

<div align="center">
  <strong>⭐ Star this repository if you find it helpful!</strong><br>
  <strong>Happy Downloading! 🎉🎵</strong>
</div>
