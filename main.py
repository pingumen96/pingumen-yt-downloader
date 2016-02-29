# TODO list:
#  - download playlist
#  - gestione errori di connessione
#  - barra di progresso del download con velocità e tempo rimanente (ttk.Progressbar)
#       troppo difficile per ora, serve fare multithreading per non bloccare la GUI
#  - salvataggio della cartella di download (si suppone in file esterno)
# documentazione pafy: http://pythonhosted.org/pafy/
# link per provare: https://www.youtube.com/watch?v=WKn6javQIqY
# https://www.youtube.com/watch?v=0gCWPvRZcsI

import ssl #utile per gestione errori di connessione (?)
import pafy
from hurry.filesize import size
import tkinter
from tkinter.filedialog import askdirectory
from tkinter import ttk

root = tkinter.Tk()
global save_folder
save_folder = tkinter.StringVar()


def save_folder_set(): #forse non necessaria, da controllare
    save_folder.set(askdirectory())


def download_gui():
    # prende il testo dalla casella di testo
    video_url = yt_video_link_entry.get()
    #yt_video = YouTube(yt_video_link)
    video = pafy.new(video_url)
    video_info = video.allstreams  # prende i vari formati del video
    download_window = tkinter.Toplevel()
    download_window.title = 'Download video'
    video_format = []  # lista che conterrà i formati video, sostituita da yt_video.streams
    video_download_button = []  # lista che conterrà i bottoni
    video_title_label = tkinter.Label(
        download_window,
        text=video.title,
        relief=tkinter.SUNKEN,
        padx=6,
        pady=3)
    video_title_label.grid(row=0, columnspan=6)
    tkinter.Label(download_window, text='Media').grid(row=1, column=0)
    tkinter.Label(download_window, text='Estensione').grid(row=1, column=1)
    tkinter.Label(download_window, text='Risoluzione').grid(row=1, column=2)
    tkinter.Label(download_window, text='Bitrate').grid(row=1, column=3)
    tkinter.Label(download_window, text='Dimensione').grid(row=1, column=4)
    y = 0  # tiene il conto dei cicli effettuati per generare correttamente layout
    for x in range(0, len(video_info)):
        if video_info[x].mediatype != 'video':
            tkinter.Label(download_window, text=video_info[
                          x].mediatype).grid(row=y + 2, column=0)
            tkinter.Label(download_window, text=video_info[
                          x].extension).grid(row=y + 2, column=1)
            tkinter.Label(download_window, text=video_info[
                          x].resolution).grid(row=y + 2, column=2)
            if video_info[x].mediatype == 'audio':
                tkinter.Label(download_window, text=video_info[
                              x].bitrate).grid(row=y + 2, column=3)
            else:
                tkinter.Label(download_window,
                              text='-').grid(row=y + 2, column=3)
            tkinter.Label(download_window, text=size(
                video_info[x].get_filesize())).grid(row=y + 2, column=4)
            video_download_button.append(tkinter.Button(download_window, text='Download', command=lambda z=x: video.allstreams[
                                         z].download(filepath=save_folder.get())))
            video_download_button[y].grid(row=y + 2, column=5)
            print(video_info[x])  # prova per vedere output
            # print(yt_video.filename) #mostra titolo del video
            # vedere la struttura delle informazioni sul video
            y += 1
    # gestione cartella di salvataggio
    save_folder_entry = tkinter.Entry(
        download_window, textvariable=save_folder)
    save_folder_entry.grid(row=y + 3, columnspan=4)
    # far sì che si cancelli contenuto quando si sceglie cartella
    choose_directory = tkinter.Button(
        download_window, text='Sfoglia...', command=lambda: save_folder_set())
    choose_directory.grid(row=y + 3, column=5)


def main_gui():
    global yt_video_link_entry
    yt_video_link_entry = tkinter.Entry(width=60)
    yt_video_link_entry.grid(row=0, column=0)
    download_button = tkinter.Button(
        text='Download!',
        command=lambda: download_gui())
    download_button.grid(row=0, column=1)

main_gui()
root.resizable(width=tkinter.FALSE, height=tkinter.FALSE)
root.title('YouTube Video Downloader by Pingumen96')
root.mainloop()
