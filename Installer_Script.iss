[Setup]
AppName=YouTube Downloader
AppVersion=1.0
DefaultDirName={pf}\YouTubeDownloader
DefaultGroupName=YouTube Downloader
OutputDir=Output
OutputBaseFilename=YouTubeDownloader
AppPublisher=Polaris Software
AppCopyright=Copyright (C) 2023 Polaris Software.
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\Jacob\PycharmProjects\YouTubeDownloader\build\exe.win-amd64-3.10\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{commondesktop}\YouTube Downloader"; Filename: "{app}\Main.exe"; WorkingDir: "{app}"; IconFilename: "{app}\logo.ico"
Name: "{commonprograms}\YouTube Downloader"; Filename: "{app}\Main.exe"; IconFilename: "{app}\logo.ico"
Name: "{commonstartup}\YouTube Downloader"; Filename: "{app}\Main.exe"; IconFilename: "{app}\logo.ico"
