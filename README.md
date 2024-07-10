# YouTube Downloader

<!-- ![logo](https://raw.githubusercontent.com/RadoslavBukov/YouTube-Downloader/main/static_files/logo.jpg) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/RadoslavBukov/YouTube-Downloader/main/static_files/logo.jpg" alt="logo">
</div>

Welcome to the YouTube Downloader! This application allows you to download YouTube videos and audio easily. This guide will help you understand the features and functionalities of the application. Below, you'll find sections detailing each part of the interface.

## Main Features
- **Customizable Appearance**: Change the appearance mode and UI scaling to suit your preferences.
- **Search by Name or URL**: Find YouTube videos using the artist and title or directly input the YouTube URL.
- **Download Options**: Choose from various audio and video formats and select the desired quality.
- **Trimming**: Specify start and end times to trim the downloaded media.
- **Download Media**: Download video and audio files in a specific folder.

## Graphical User interface
<div align="center">
  <img src="hhttps://raw.githubusercontent.com/RadoslavBukov/YouTube-Downloader/main/github_img/GYI_fetched.jpg" alt="gui">
</div>
The main window of the application is divided into several sections:

- **Sidebar**: Contains the logo, appearance settings, and scaling options.
- **Search Section**: Allows searching for videos by name or URL.
- **Options Frame**: Select format and quality, and specify trimming options.
- **Visualization Frame**: Displays video thumbnails and allows video preview.
- **Download Frame**: Specify the download location and initiate downloads.

## Code Overview
### static_files Folder
Includes a couple of static images for visualization and a `setup.json` file, which contains settings about the app.

- **setup.json**: Contains configuration settings for the application.

### `backend.py`
This script allows users to download video and audio from YouTube with specific requirements for format, quality, and length. It supports operations via a console application interface, making it easy to download content based on various criteria.
#### Block diagram
<div align="center">
  <img src="hhttps://raw.githubusercontent.com/RadoslavBukov/YouTube-Downloader/main/github_img/backend_blockdiagram.png" alt="block_diagram">
</div>

### `gui.py`
The `App` class is a graphical user interface (GUI) application built using `customtkinter` and `tkinter`. This application allows users to search, preview, and download YouTube videos and playlists in various formats and qualities. The app also includes audio playback functionalities.

## Instalation
Clone the repository to your local machine, use the following command in your terminal or command prompt:
```bash
git clone https://github.com/RadoslavBukov/YouTube-Downloader.git
```

Install all needed dependencies stored I requirements.txt file:
 ```bash
pip install -r requirements.txt
```

Run application:
```bash
python gyi.py
```

## Summary
The provided source code is for a YouTube Downloader application built using the `customtkinter` library for the GUI and various other libraries like `pytube` for downloading YouTube content, `PIL` for image processing, and `pygame` for audio playback. The application allows users to search for YouTube videos by name or URL, preview the video thumbnail, and download videos or audio in various formats and qualities. The application also includes features for customizing the appearance and scaling of the UI.

### Features
- **Search and Download by Name or URL**: Users can search for videos by name or directly input a YouTube URL. The application handles both individual video URLs and playlist URLs.
- **Format and Quality Selection**: Users can select the desired audio or video format and choose from available quality options.
- **Thumbnail Preview**: The application displays a thumbnail of the video and allows users to play and pause the downloaded audio.
- **Trim Options**: Users can specify start and end times to trim the downloaded media.
- **Customizable UI**: The application supports different appearance modes (Light, Dark, System) and UI scaling options.

### Conclusion
The YouTube Downloader application is a versatile and user-friendly tool for downloading and previewing YouTube content. It provides a robust set of features that cater to various user needs, from basic video downloads to customized audio trimming. The use of modern libraries like `customtkinter` and `pytube` ensures that the application is both visually appealing and functionally rich.

### Future Updates
- **Error Handling Improvements**: Enhance error handling to provide more specific and user-friendly error messages.
- **Progress Feedback**: Implement a progress bar to give users real-time feedback during the download process.
- **Batch Download**: Add functionality to support batch downloading of multiple videos at once.

### Users Note
If you encounter the following error while using this application:
 ```bash
pytube.exceptions.RegexMatchError: get_throttling_function_name: could not find match for multiple
 ```

This error is typically caused by changes in YouTube's backend, which affect how the Pytube library fetches video metadata. To resolve this issue, you can take the following steps:

1. *Update Pytube*: Ensure you have the latest version installed using the following command:
```bash
pip install --upgrade pytube
```
2. *Check YouTube Service Status*: Verify if there are any ongoing issues or downtime affecting video downloads on YouTube's Status Dashboard.
3. *Report the Issue*: If the problem persists after updating Pytube, please report it to the Pytube developers on GitHub Issues. Provide detailed information about the error to help diagnose and fix the issue.

**Thank you for your understanding and patience.**
