from tkinter import filedialog
from tkinter import *
import pygame
import os
from mutagen.mp3 import MP3
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Import PIL library

root = Tk()
root.title('Music Player')
root.geometry('980x590')
root.config(bg='gray23')

pygame.mixer.init()  # Adjust buffer size as needed

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = True

# Load and display image
image_path = "image.jpg"  # Replace with your image path
image = Image.open(image_path)
image = image.resize((500, 300))  # Resize the image
photo = ImageTk.PhotoImage(image)
image_label = Label(root, image=photo)
image_label.image = photo
image_label.grid(row=0, column=1, padx=10, pady=10)  # Place the image beside the playlist box
image_label.config(borderwidth=1, highlightcolor='grey')
songlist = Listbox(root, bg="black", fg="white", width=70, height=30)
songlist.grid(row=0, column=0, padx=10, pady=10)  # Place the playlist box
songlist.config(border=0, highlightthickness=0)
def load_music():
    global current_song
    songs.clear()
    root.directory = filedialog.askdirectory()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    if songs:  # Check if songs list is not empty
        songlist.selection_set(0)
        current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song, paused
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def toggle_play_pause():
    global paused
    if paused:
        play_btn.config(image=play_bth_image)
        play_music()  # Start playing if paused
        paused = False
    else:
        play_btn.config(image=pause_bth_image)
        pause_music()  # Pause if playing
        paused = True

def next_music():
    global current_song
    try:
        index = songs.index(current_song)
        next_index = (index + 1) % len(songs)
        current_song = songs[next_index]
        songlist.selection_clear(0, END)
        songlist.selection_set(next_index)
        play_music()  # Start playing the next song
    except ValueError:  # Catch ValueError when current song is not found in the list
        pass

def prev_music():
    global current_song
    try:
        index = songs.index(current_song)
        prev_index = (index - 1) % len(songs)
        current_song = songs[prev_index]
        songlist.selection_clear(0, END)
        songlist.selection_set(prev_index)
        play_music()  # Start playing the previous song
    except ValueError:  # Catch ValueError when current song is not found in the list
        pass

# def skip_forward():
#     pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() + 10)  # Skip forward 10 seconds
#
# def skip_backward():
#     pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() - 10)  # Skip backward 10 seconds

def on_song_select(event):
    global current_song
    selected_index = songlist.curselection()
    if selected_index:
        current_song = songs[selected_index[0]]
        play_music()

def update_progress():
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000
        total_time = MP3(os.path.join(root.directory, current_song)).info.length
        progress_label.config(text=f"{format_time(current_time)} / {format_time(total_time)}")
    else:
        progress_label.config(text="00:00 / 00:00")

    root.after(100, update_progress)

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

# Function bindings
songlist.bind('<<ListboxSelect>>', on_song_select)

# Menu
organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Add Music', menu=organise_menu)

# Images
play_bth_image = PhotoImage(file='pause.png').subsample(40)
pause_bth_image = PhotoImage(file='play.png').subsample(40)
next_bth_image = PhotoImage(file='next.png').subsample(40)
prev_bth_image = PhotoImage(file='previous.png').subsample(40)

# Control frame and progress label container
control_container = Frame(root)
control_container.config(borderwidth=0, relief=GROOVE)
control_container.grid(row=1, column=0, columnspan=2)  # Grid the container below the playlist box with some padding

# Control frame
control_frame = Frame(control_container)
control_frame.pack(side=TOP)  # Pack the control frame at the top of the container

# Buttons
play_btn = Button(control_frame, image=play_bth_image, borderwidth=0, command=toggle_play_pause)
play_btn.grid(row=0, column=1, padx=20, pady=10)

next_btn = Button(control_frame, image=next_bth_image, borderwidth=0, command=next_music)
next_btn.grid(row=0, column=3, padx=20, pady=10)

prev_btn = Button(control_frame, image=prev_bth_image, borderwidth=0, command=prev_music)
prev_btn.grid(row=0, column=0, padx=20, pady=10)

# Progress label
progress_label = Label(control_container, text="00:00 / 00:00", fg="black")
progress_label.pack(side=TOP)  # Pack the progress label at the top of the container

# Start updating progress
update_progress()

# Main loop
root.mainloop()
