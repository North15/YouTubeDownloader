import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"  # For Windows GUI applications

executables = [Executable("Main.py", base=base)]

build_options = {
    "packages": ["yt_dlp", "PyQt5"],
    "excludes": [],
    "include_files": ["logo.png", "error.png", "logo.ico"],
}

setup(
    name="YouTubeDownloader",
    version="1.0",
    description="YouTube Downloader Application",
    options={"build_exe": build_options},
    executables=executables,
)
