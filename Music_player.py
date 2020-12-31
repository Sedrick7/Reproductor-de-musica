# Libraries needed #
from tkinter import *
from tkinter import filedialog
import pygame 
import time
from mutagen.mp3 import MP3 
import tkinter.ttk as ttk

# Function to add songs to the playlist#
def add_songs():
    songs = filedialog.askopenfilenames(initialdir='music/', title='Escoge una cancion', filetypes=(('Archivos mp3', '*.mp3'), ('Archivos wav', '*.wav')))

    for song in songs:
        song = song.replace('C:/Users/javie/Desktop/Python/Music Player/music/', '')
        song = song.replace('.mp3', '')

        song_box.insert(END, song)


# Delete songs from the playlist #
def del_songs():
    # delete slected song #
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


# Delete the entire playlist #
def del_all():
     # delete all songs #
     song_box.delete(0, END)
     pygame.mixer.music.stop()



# Back Function #
def prv_sng():
    prv_song = song_box.curselection()
    prv_song = prv_song[0]-1

    song = song_box.get(prv_song)
    song = f'C:/Users/javie/Desktop/Python/Music Player/music/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.select_clear(0,END)
    song_box.activate(prv_song)
    song_box.selection_set(prv_song, last=None)


# Next Function #
def nxt_sng():
    next_song = song_box.curselection()
    next_song = next_song[0]+1

    song = song_box.get(next_song)
    song = f'C:/Users/javie/Desktop/Python/Music Player/music/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    song_box.select_clear(0,END)
    song_box.activate(next_song)
    song_box.selection_set(next_song, last=None)




# Play Function #
def Play():
    song = song_box.get(ACTIVE)
    song = f'C:/Users/javie/Desktop/Python/Music Player/music/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    play_time()


# Pause Function #
global paused
global playing
paused = False

def Pause(is_paused):
    global paused

    paused = is_paused

    # Unpause #
    if paused:
        pygame.mixer.music.unpause()
        paused = False

    # Pause #
    else:
        pygame.mixer.music.pause()
        paused = True


# Stop Function #
def Stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    timeline.config(text='')


# Song timeline #
def play_time():
    current_time = pygame.mixer.music.get_pos()/1000
    
    # time in minutes#
    min_time = time.strftime('%M:%S', time.gmtime(current_time))
    
    # Song currently playing #
    #current_song = song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f'C:/Users/javie/Desktop/Python/Music Player/music/{song}.mp3'
    
    # song lenght #
    song_mut = MP3(song)
    song_lenght = song_mut.info.length
    # convert time #
    converted_song_lenght = time.strftime('%M:%S', time.gmtime(song_lenght))

    timeline.config(text = f'Tiempo transcurrido: {min_time} de {converted_song_lenght}   ')

    timeline.after(1000, play_time)




# Creation of the window #
root = Tk()
root.title('Music Player')
root.iconbitmap('Music.ico')
root.geometry('500x350')
root.configure(bg='gray')

pygame.mixer.init()

# Play list box #
song_box = Listbox(root)
song_box.configure(bd=0, bg='silver', fg='black', width=1000, selectbackground='dimgray', selectforeground='white')
song_box.pack(pady=20)

# Buttons icons #
back_btn_img = PhotoImage(file='buttons/Back.png')
fwd_btn_img = PhotoImage(file='buttons/Forward.png')
play_btn_img = PhotoImage(file='buttons/Play.png')
pause_btn_img = PhotoImage(file='buttons/Pause.png')
stop_btn_img = PhotoImage(file='buttons/Stop.png')

ctrls_frame = Frame(root)
ctrls_frame.configure(bg='gray')
ctrls_frame.pack()

# Control Buttons #
back_btn = Button(ctrls_frame, image=back_btn_img, borderwidth=0, bg='gray', command=prv_sng)
fwd_btn = Button(ctrls_frame, image=fwd_btn_img, borderwidth=0, bg='gray', command=nxt_sng)
play_btn = Button(ctrls_frame, image=play_btn_img, borderwidth=0, bg='gray', command=Play)
pause_btn = Button(ctrls_frame, image=pause_btn_img, borderwidth=0, bg='gray', command=lambda: Pause(paused))
stop_btn = Button(ctrls_frame, image=stop_btn_img, borderwidth=0, bg='gray', command=Stop)

# Buttons Positions #
back_btn.grid(row=0,column=0, padx=10)   
pause_btn.grid(row=0,column=1, padx=10)
play_btn.grid(row=0,column=2, padx=10) 
stop_btn.grid(row=0,column=3, padx=10)
fwd_btn.grid(row=0,column=4, padx=10)


# Menu #
my_menu = Menu(root)
root.config(menu=my_menu)

# Song Menu Options #
songs_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Opciones', menu=songs_menu)
# Add songs option #
songs_menu.add_command(label='Agregar canciones a la Playlist', command=add_songs)
# Separator #
songs_menu.add_separator()
# Delete songs options #
songs_menu.add_command(label='Quitar canción seleccionada', command=del_songs)
songs_menu.add_command(label='Borrar la Playlist', command=del_all)
# Separator #
songs_menu.add_separator()
# Exit button #
songs_menu.add_command(label='Salir', command=root.destroy)

# Song Timeline #
timeline = Label(root, text='',bd=1, relief=GROOVE, anchor=E)
timeline.pack(fill=X, side=BOTTOM, ipady=2)


root.mainloop()