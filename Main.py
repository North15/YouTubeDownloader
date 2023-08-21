import sys
import yt_dlp as youtube_dl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, \
    QFileDialog, QRadioButton, QHBoxLayout, QMessageBox, QTabWidget, QTextBrowser, QFormLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings


class YoutubeDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 400, 300)

        self.settings = QSettings("Polaris Software", "YouTubeDownloader")
        self.output_folder = self.settings.value("output_folder", None)

        self.init_ui()
        self.setWindowIcon(QIcon('logo.png'))

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_download_tab(), "Download")
        self.tab_widget.addTab(self.create_settings_tab(), "Settings")
        self.tab_widget.addTab(self.create_about_tab(), "About")

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        self.central_widget.setLayout(layout)

    def create_settings_tab(self):
        settings_tab = QWidget()

        layout = QVBoxLayout()

        self.settings_label = QLabel("Settings")
        self.settings_label.setAlignment(Qt.AlignCenter)
        self.settings_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.output_label = QLabel("Output Folder:")
        self.output_location = QLabel()
        self.output_location.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.update_output_location_label()

        self.change_output_button = QPushButton("Change Output Location")
        self.change_output_button.clicked.connect(self.show_folder_dialog)

        settings_layout = QFormLayout()
        settings_layout.addRow(self.output_label, self.output_location)
        settings_layout.addRow(self.change_output_button)

        layout.addWidget(self.settings_label)
        layout.addSpacing(10)
        layout.addLayout(settings_layout)

        settings_tab.setLayout(layout)
        return settings_tab

    def update_output_location_label(self):
        self.output_folder = self.settings.value("output_folder", None)
        if self.output_folder:
            self.output_location.setText(self.output_folder)
        else:
            self.output_location.setText("Not set")

    def create_download_tab(self):
        download_tab = QWidget()

        layout = QVBoxLayout()

        self.main_label = QLabel("YouTube Downloader")
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.download_label = QLabel("Download Status:")
        self.download_label.setAlignment(Qt.AlignCenter)
        self.download_label.setStyleSheet("font-size: 12px; font-weight: bold;")

        self.download_status = QLabel("Waiting for Input...")
        self.download_status.setAlignment(Qt.AlignCenter)
        self.download_status.setStyleSheet("font-size: 10px; font-weight: bold")

        self.url_layout = QHBoxLayout()
        self.url_label = QLabel("Enter URL:")
        self.url_input = QLineEdit()
        self.url_layout.addWidget(self.url_label)
        self.url_layout.addWidget(self.url_input)

        self.audio_radio = QRadioButton("Audio")
        self.video_radio = QRadioButton("Video")
        self.both_radio = QRadioButton("Both")
        self.audio_radio.setChecked(True)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.audio_radio)
        radio_layout.addWidget(self.video_radio)
        radio_layout.addWidget(self.both_radio)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_video)

        layout.addWidget(self.main_label)
        layout.addWidget(self.download_label)
        layout.addWidget(self.download_status)
        layout.addSpacing(10)
        layout.addLayout(self.url_layout)
        layout.addLayout(radio_layout)
        layout.addSpacing(10)
        layout.addWidget(self.download_button)

        download_tab.setLayout(layout)
        return download_tab

    def create_about_tab(self):
        about_tab = QWidget()

        layout = QVBoxLayout()

        about_label = QLabel("About YouTube Downloader")
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        about_text = QTextBrowser()
        about_text.setOpenExternalLinks(True)
        about_text.setHtml("<p>This application allows you to download YouTube videos and playlists in audio, video, or both formats.</p>"
                           "<p>Version: 1.0<br>"
                           "Author: Polaris Software<br>")

        layout.addWidget(about_label)
        layout.addWidget(about_text)

        about_tab.setLayout(layout)
        return about_tab

    def show_folder_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder", options=options)
        if folder_path:
            self.output_folder = folder_path
            self.settings.setValue("output_folder", folder_path)
            self.update_output_location_label()

    def download_video(self):
        video_url = self.url_input.text().strip()  # Remove leading/trailing spaces
        if not video_url:  # Check if the URL is empty
            self.show_error_message("Please enter a valid URL.")
            return

        self.set_in_progress()

        if self.output_folder:
            if self.audio_radio.isChecked():
                self.download_video_content(video_url, self.output_folder, "Audio")
            elif self.video_radio.isChecked():
                self.download_video_content(video_url, self.output_folder, "Video")
            elif self.both_radio.isChecked():
                self.download_video_content(video_url, self.output_folder, "Audio")
                self.download_video_content(video_url, self.output_folder, "Video")
        else:
            self.show_error_message("Please set the output location first.")

        self.set_complete()

    def download_video_content(self, video_url, output_folder, download_option):
        ydl_opts = {
            'format': 'bestaudio/best' if download_option == "Audio" else 'bestvideo/best',
            'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': 'ffmpeg\\bin',
            'yesplaylist': True,
        } if download_option == "Audio" else {
            'format': 'best',
            'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
            'ffmpeg_location': 'ffmpeg\\bin',
            'yesplaylist': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([video_url])
            except Exception as e:
                error_message = f"An error occurred: {e}"
                print(error_message)
                self.show_error_message(error_message)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setWindowIcon(QIcon('error.png'))
        msg_box.exec_()

    def set_in_progress(self):
        self.download_status.setText("Download In-Progress")
        self.download_status.setStyleSheet("font-size: 10px; font-weight: bold; color: red")

    def set_complete(self):
        self.download_status.setText("Download Complete")
        self.download_status.setStyleSheet("font-size: 10px; font-weight: bold; color: green")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = YoutubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
