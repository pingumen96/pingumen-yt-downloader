# TODO list:
#  - download playlist
#  - gestione errori di connessione
# documentazione pafy: http://pythonhosted.org/pafy/
# link per provare: https://www.youtube.com/watch?v=WKn6javQIqY
# https://www.youtube.com/watch?v=0gCWPvRZcsI

import ssl  # utile per gestione errori di connessione (?)
import pafy
from hurry.filesize import size
import tkinter
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror
from tkinter import ttk

root = tkinter.Tk()
global save_folder
save_folder = tkinter.StringVar()
global folder_file
try:
    open('download_folder.txt', 'r+')
except FileNotFoundError:
    folder_file = open('download_folder.txt', 'w+')


def save_folder_set():  # forse non necessaria, da controllare
    folder_file = open('download_folder.txt', 'w+')
    save_folder.set(askdirectory())
    folder_file.write(save_folder.get())
    folder_file.close()

#funzioni per download di video e playlist

#parte riguardante i video singoli
def download_video():
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
    tkinter.Label(download_window, text='Risoluzione').grid(
        row=1, column=2)
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
    folder_file = open('download_folder.txt', 'r+') #dovrebbe farlo all'apertura del programma
    save_folder.set(folder_file.read())
    folder_file.close()
    save_folder_entry = tkinter.Entry(
        download_window, textvariable=save_folder)
    save_folder_entry.grid(row=y + 3, columnspan=4)
    # far sì che si cancelli contenuto quando si sceglie cartella
    choose_directory = tkinter.Button(
        download_window, text='Sfoglia...', command=lambda: save_folder_set())
    choose_directory.grid(row=y + 3, column=5)


#parte riguardante le playlist
def download_playlist_video(streams,mediatype,extension,resolution=None,bitrate=None):
    for z in range(0,len(streams)):
        #scaricamento di tutti gli stream della lista che rispondono ai requisiti specificati nei parametri
        if streams[z].mediatype==mediatype and streams[z].extension==extension and (streams[z].resolution==resolution or streams[z].bitrate==bitrate) :
            streams[z].download(filepath=save_folder.get())
            print(streams[z].extension)

def playlist_iterator(item_list): #funzione che si occupa di iterare lungo la lista di video passata
    pass

def download_playlist():
    playlist_url = yt_video_link_entry.get()
    playlist = pafy.get_playlist(playlist_url)
    # print(playlist)
    # creazione della finestra
    download_window = tkinter.Toplevel()
    download_window.title('Download Playlist')
    #creazione frame sinistro
    left_frame=tkinter.Frame(download_window,height=600, width=400)
    left_frame.pack(side='left')
    #creazione frame destro
    right_frame=tkinter.Frame(download_window,height=600, width=400)
    right_frame.pack(side='right')

    #lista video
    playlist_video_list=[] #contiene gli oggetti video
    playlist_formats=[] #contiene solo i formati sottoforma di stringhe
    playlist_streams=[] #contiene gli oggetti stream, serve per passarla alla funzione download_playlist_video()

    # INIZIO DEBUG

    # FINE DEBUG

    #devono essere disponibili al download solo i formati comuni a tutti gli stream
    #forse funziona così, da verificare
    for x in range(0,len(playlist['items'])):
        playlist_video_list.append(playlist['items'][x])
        #print(str(playlist_video_list[x]['pafy'].streams)+'\n')
        playlist_streams.extend(playlist_video_list[x]['pafy'].streams)
        for y in range(0,len(playlist_video_list[x]['pafy'].streams)):
            #print(playlist_video_list[x]['pafy'].streams[y])
            if not str(playlist_video_list[x]['pafy'].streams[y]) in playlist_formats:
                #INIZIO DEBUG
                for z in range(x,len(playlist['items'])):
                    string_list=list(map(str, playlist['items'][z]['pafy'].streams)) #converte in stringa gli elementi di una lista
                    if str(playlist_video_list[x]['pafy'].streams[y]) in string_list:
                        flag=True
                        #print('prova')
                    else:
                        flag=False
                        break
                if flag==True:
                    #print('prova')
                    #mostrare i label
                    playlist_formats.append(str(playlist_video_list[x]['pafy'].streams[y])) #commento da togliere
                    #costruzione dei label a destra
                    tkinter.Label(right_frame,text=playlist_video_list[x]['pafy'].streams[y].mediatype).grid(row=y,column=0)
                    tkinter.Label(right_frame,text=playlist_video_list[x]['pafy'].streams[y].extension).grid(row=y,column=1)
                    if playlist_video_list[x]['pafy'].streams[y].mediatype=='audio':
                        tkinter.Label(right_frame,text=playlist_video_list[x]['pafy'].streams[y].bitrate).grid(row=y,column=2)
                        tkinter.Button(right_frame,text='Download',command=lambda i=x, j=y:download_playlist_video(playlist_streams,playlist_video_list[i]['pafy'].streams[j].mediatype,playlist_video_list[i]['pafy'].streams[j].extension,None,playlist_video_list[i]['pafy'].streams[j].bitrate)).grid(row=y,column=3)
                    else:
                        tkinter.Label(right_frame,text=playlist_video_list[x]['pafy'].streams[y].resolution).grid(row=y,column=2)
                        tkinter.Button(right_frame,text='Download',command=lambda i=x, j=y:download_playlist_video(playlist_streams,playlist_video_list[i]['pafy'].streams[j].mediatype,playlist_video_list[i]['pafy'].streams[j].extension,playlist_video_list[i]['pafy'].streams[j].resolution,None)).grid(row=y,column=3)
                #FINE DEBUG
        print(playlist_formats)
            # gestione cartella di salvataggio
        folder_file = open('download_folder.txt', 'r+') #dovrebbe farlo all'apertura del programma
        save_folder.set(folder_file.read())
        folder_file.close()
        save_folder_entry = tkinter.Entry(right_frame, textvariable=save_folder)
        save_folder_entry.grid(row=y + 1, columnspan=3)
        # far sì che si cancelli contenuto quando si sceglie cartella
        choose_directory = tkinter.Button(right_frame, text='Sfoglia...', command=lambda: save_folder_set())
        choose_directory.grid(row=y + 1, column=3)
        #lista video che sta a sinistra
        tkinter.Label(left_frame,text=playlist_video_list[x]['pafy'].title).grid(sticky=tkinter.W)

def download_wrapper():
    try:
        download_video()
    except:  # se non riesce a scaricare il video singolo non riconoscendo il link
        try:
            download_playlist()
        except ValueError:
            showerror('Errore', 'Il link inserito non è valido.')


def main_gui():
    global yt_video_link_entry
    yt_video_link_entry = tkinter.Entry(width=60)
    yt_video_link_entry.grid(row=0, column=0)
    download_button = tkinter.Button(
        text='Download!',
        command=lambda: download_wrapper())
    download_button.grid(row=0, column=1)

main_gui()
root.resizable(width=tkinter.FALSE, height=tkinter.FALSE)
root.title('YouTube Video Downloader by Pingumen96')
root.mainloop()
