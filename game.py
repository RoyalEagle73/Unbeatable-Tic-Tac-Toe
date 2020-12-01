from tkinter import *
from PIL import Image
from PIL import ImageTk

# Root window declaration
root = Tk()

# Logos and Images
cross = PhotoImage(file="crossLogo.png").subsample(2)
zero = PhotoImage(file="zeroLogo.png").subsample(2)
hvhImage = PhotoImage(file="hvh.png")
hvrImage = PhotoImage(file="hvr.png")
    
# Player and Computer Icons
computerIcon = ""
playerIcon = ""
playerName = ""
computerName = "Shakti"

# GameMode, 0 if Human vs Human, 1 if Human vs Robot
mode = 1

# Methods that will be used in later stages
# Game Mode Selection Screen Methods
def finalChooseMode(modeValue):
    global mode
    mode = modeValue
    print(mode)

def chooseMode(root):
    global hvhImage
    global hvrImage
    welcomeLabel = Label(root, bg = "white", fg="orange", text="Welcome, choose game mode...", justify="center",font = "Helvetica 16 bold italic")
    hvhButton = Button(root,bd=0,highlightthickness=0,bg="white", height=250, width=300,image=hvhImage,command= lambda: finalChooseMode(0))
    hvrButton = Button(root,bd=0, highlightthickness=0,bg="white",height=250, width=300, image=hvrImage, command= lambda: finalChooseMode(1))
    welcomeLabel.place(x=140,y=50)
    hvhButton.place(x=0,y=175)
    hvrButton.place(x=300,y=175)

# Icon selection screen methods    
def changeIcon(choice):
    global cross
    global zero
    if choice==0:
        playerIcon = cross
        computerIcon = zero
    else:
        playerIcon = zero
        computerIcon = cross
    print(choice)

def selectIcons(root):
    global cross
    global zero
    global computerIcon
    global playerIcon
    chooseLabel = Label(root, bg = "white", fg="orange", text="Welcome, choose Your player icon...", justify="center",font = "Helvetica 16 bold italic")
    crossButton = Button(root,bd=0,highlightthickness=0,bg="white", height=250, width=300,image=cross,command= lambda: changeIcon(0))
    zeroButton = Button(root,bd=0, highlightthickness=0,bg="white",height=250, width=300, image=zero, command= lambda: changeIcon(1))
    chooseLabel.place(x=100,y=50)
    crossButton.place(x=0,y=175)
    zeroButton.place(x=300,y=175)

# Choose whom to play first screen
def firstPlaySelection(root):
    chooseLabel = Label(root, bg = "white", fg="orange", text="Welcome, choose Your player icon...", justify="center",font = "Helvetica 16 bold italic")
    crossButton = Button(root,bd=0,highlightthickness=0,bg="white", height=250, width=300,image=cross,command= lambda: changeIcon(0))
    zeroButton = Button(root,bd=0, highlightthickness=0,bg="white",height=250, width=300, image=zero, command= lambda: changeIcon(1))
    chooseLabel.place(x=100,y=50)
    crossButton.place(x=0,y=175)
    zeroButton.place(x=300,y=175)

# Asking name for players
width = 600
height = 600
root.title("Tic Tac Toe - Player vs AI")
root.geometry( str(width) + "x" + str(height))
root.configure(bg="white")

# Player Name
playerName = ""
computerName = "AI"

# Main Call
# selectIcons(root)
chooseMode(root)
root.mainloop()