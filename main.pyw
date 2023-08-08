import customtkinter as ctk
import requests
import os, io
import win32clipboard as clip
import win32con as con
from PIL import Image
from pytube import YouTube

def extractVideoCode(link: str):
    replaceList = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/", "https://youtube.com/playlist?list="]
    _ = "" 
    for i in replaceList:
        link = link.replace(i, "")
    
    for i in link:
        if i != "?" and i != "&":
            _ += i
        else:
            break
    return _

def getThumbnail(link: str):
    videocode = extractVideoCode(link)
    thumbnail_link = f"https://i.ytimg.com/vi/{videocode}/maxresdefault.jpg"
    temp = os.getenv('temp')
    with open(fr'{temp}\\{videocode}.png', 'ab') as f:
        f.write(requests.get(thumbnail_link).content)
        f.close()
    return f'{temp}\\{videocode}.png'

def gui():
    app = ctk.CTk()
    ctk.set_default_color_theme('green')
    app.geometry("800x600")
    app.resizable(False, False)
    app.title("Wertolebus Video Downloader")

    ctk.CTkLabel(app, text="Version 1.0", text_color="#383838").place(anchor='se', relx=0.99, rely=1)
    searchEntry = ctk.CTkEntry(app, placeholder_text="Youtube video URL", width=512)
    thumbnail_label = ctk.CTkLabel(app, image=None, text="")

    def downloadVideo(resolution:str):
        link = globalLink
        yt = YouTube(link)
        yt.streams.filter(resolution=resolution).first().download(".\\", f"{yt.title}_{resolution}.mp4")
    
    def downloadAudio():
        link = globalLink
        yt = YouTube(link)
        yt.streams.get_audio_only().download(".\\", f"{yt.title}.mp3")

    def onCopyButton():
        thumbnail = Image.open(getThumbnail(searchEntry.get().strip()))
        buf = io.BytesIO()
        thumbnail.convert("RGB").save(buf, "BMP")
        data = buf.getvalue()[14:]
        buf.close()

        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardData(con.CF_DIB, data)
        clip.CloseClipboard()
        
    def onDownloadButton():
        thumbnail = Image.open(getThumbnail(searchEntry.get().strip()))
        thumbnail.save(f"{extractVideoCode(searchEntry.get().strip())}.png")

    def onClickSearch():
        global globalLink
        if searchEntry.get().strip() != "":
            thumbnail = Image.open(getThumbnail(searchEntry.get().strip()))
            size = (round(thumbnail.size[0]//2.5), round(thumbnail.size[1]//2.5))
            _thumbnail = ctk.CTkImage(thumbnail, size=(size))
            globalLink = searchEntry.get().strip()

            download480p = ctk.CTkButton(app, text="Download 480p", width=110, height=40, command=lambda: downloadVideo("480p"))
            download720p = ctk.CTkButton(app, text="Download 720p", width=110, height=40, command=lambda: downloadVideo("720p"))
            download1080p = ctk.CTkButton(app, text="Download 1080p", width=110, height=40, command=lambda: downloadVideo("1080p"))
            downloadMP3 = ctk.CTkButton(app, text="Download MP3", width=110, height=40, command=lambda: downloadAudio())
            copyButton = ctk.CTkButton(app, text="Copy to clipboard", width=110, height=40, command=lambda:onCopyButton())
            downloadButton = ctk.CTkButton(app, text="Download", width=110, height=40, command=lambda:onDownloadButton())
            
            download480p.place(anchor='center', relx=.3, rely=.625)
            download720p.place(anchor='center', relx=.3, rely=.725)
            download1080p.place(anchor='center', relx=.3, rely=.825)
            downloadMP3.place(anchor='center', relx=.3, rely=.925)
            downloadButton.place(anchor='center', relx=0.7, rely=0.65)
            copyButton.place(anchor='center', relx=0.7, rely=0.75)
            searchButton.place_configure(relx=0.5, rely=0.7)
            thumbnail_label.configure(image=_thumbnail)

    searchButton = ctk.CTkButton(app, text="Search", width=140, height=40, command=lambda: onClickSearch())
    searchEntry.place(anchor='center', relx=0.5, rely=0.55)
    thumbnail_label.place(anchor='center', relx=0.5, rely=0.27)
    searchButton.place(anchor='center', relx=0.5, rely=0.7)

    app.mainloop()

gui()