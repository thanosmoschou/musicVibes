"""
Author: Thanos Moschou
Date: 08/2023
Description: Let's have some fun with a simple music player made with Python.
This is a GUI app that uses mixer module of pygame.
"""

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import pygame.mixer as mixer
import os

TIME_UNTIL_CHECK = 5000 #time in ms


def startup():
    global thumbnail, thumbnailLabel

    thumbnail = ImageTk.PhotoImage(Image.open('widgets/thumbnail.jpg'))
    thumbnailLabel = Label(image = thumbnail, bg = "black")
    thumbnailLabel.grid(row = 0, column = 0, columnspan = 3)


def showButtons():
    global buttonFrame, previousImage, previousButton, nextImage, nextButton, pauseImage, pauseButton

    buttonFrame = LabelFrame(root, padx = 10, pady = 10, bg = "black", bd = 0.1)
    buttonFrame.grid(row = 2, column = 0, padx = 30, pady = 30, columnspan = 3)

    previousImage = ImageTk.PhotoImage(Image.open('widgets/previousButton.jpg').resize((50,50)))
    previousButton = Button(buttonFrame, image = previousImage, bg = "black", bd = 0.1, command = previous, activebackground = "black")
    previousButton.grid(row = 0, column = 0)

    pauseImage = ImageTk.PhotoImage(Image.open('widgets/pauseButton.jpg').resize((50,50)))
    pauseButton = Button(buttonFrame, image = pauseImage, bg = "black", bd = 0.1, command = pauseMusic, activebackground = "black")
    pauseButton.grid(row = 0, column = 1)

    nextImage = ImageTk.PhotoImage(Image.open('widgets/nextButton.jpg').resize((50,50)))
    nextButton = Button(buttonFrame, image = nextImage, bg = "black", bd = 0.1, command = next, activebackground = "black")
    nextButton.grid(row = 0, column = 2)


def selectFolder():
    global folderName, musicFiles

    folderName = filedialog.askdirectory(title = "Please select a folder with some music files")
    musicFiles = os.listdir(folderName)
    musicFiles = [folderName + "/" + file for file in musicFiles if file.endswith(".wav") or file.endswith(".mp3")] #concatenate the folder path with the filename itself in order to play songs which are not in the same folder with the script

    if(len(musicFiles) == 0):
        if messagebox.askretrycancel("No music files in this folder.", message = "Press Cancel to close the app or press Retry to select another folder.") ==  True:
            selectFolder()
        else:
            return False
    else:
        return True
    

#get the full path of a file as a string, split the string at /, pass the splitted content to a list 
#and return the last element of the list because this is the filename
def trimSongName(fullPathFileName):
    elements = fullPathFileName.split('/')
    return elements[-1]


def nowIsPlaying(songName):
    global nowIsPlayingLabel

    nowIsPlaying = Label(root, text = f'Now playing: {songName}', bg = "black", fg = "white")
    nowIsPlaying.grid(row = 1, column = 0, columnspan = 3, sticky = W + E, pady = 20)


def playSong(songName):
    mixer.music.load(songName)
    mixer.music.play()
    nowIsPlaying(trimSongName(songName))


def pauseMusic():
    global unpauseImage, unpauseButton

    unpauseImage = ImageTk.PhotoImage(Image.open('widgets/unpauseButton.jpg').resize((50,50)))
    unpauseButton = Button(buttonFrame, image = unpauseImage, bg = "black", bd = 0.1, command = unpauseMusic, activebackground = "black")
    unpauseButton.grid(row = 0, column = 1)

    mixer.music.pause()


def unpauseMusic():
    global pauseImage, pauseButton

    pauseImage = ImageTk.PhotoImage(Image.open('widgets/pauseButton.jpg').resize((50,50)))
    pauseButton = Button(buttonFrame, image = pauseImage, bg = "black", bd = 0.1, command = pauseMusic, activebackground = "black")
    pauseButton.grid(row = 0, column = 1)

    mixer.music.unpause()


def next():
    global songPointer, musicFiles

    if songPointer == len(musicFiles) - 1: #if it is the last song it starts from the beginning
        songPointer = 0
    else:
        songPointer += 1
    
    playSong(musicFiles[songPointer])


def previous():
    global songPointer, musicFiles

    if songPointer == 0: #if it is the first song it goes to the last one of the list
        songPointer = len(musicFiles) - 1
    else:
        songPointer -= 1

    playSong(musicFiles[songPointer])
    

def isEnded():
    global root

    if mixer.music.get_pos() == -1:
        next()
    #I call isEnded function inside the root.mainloop() every 5 seconds in order to check if the song is over. If it is, the next song will be played
    root.after(TIME_UNTIL_CHECK, isEnded)


def main():
    global root, songPointer

    root = Tk()
    root.title("Music Vibes")
    root.geometry('1000x710')
    root.configure(bg = "black")
    root.resizable(False, False)

    startup()
    showButtons()

    if selectFolder() == False:
        messagebox.showinfo(message = "Thanks for listening!")
        root.destroy()
    else:
        songPointer = 0

        mixer.init()
        playSong(musicFiles[songPointer])

    isEnded()    
    root.mainloop()


if __name__ == "__main__":
    main()