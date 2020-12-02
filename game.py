from tkinter import *
from PIL import Image
from PIL import ImageTk
from time import sleep
import random

# Root window declaration
root = Tk()

# Logos and Images
cross = PhotoImage(file="crossLogo.png").subsample(2)
zero = PhotoImage(file="zeroLogo.png").subsample(2)
hvhImage = PhotoImage(file="hvh.png")
hvrImage = PhotoImage(file="hvr.png")
nextButtonImage = PhotoImage(file="nextButton.png").subsample(5)
versusIcon = PhotoImage(file="vsIcon.png").subsample(2)

# Player and Computer Icons
computerIcon = ""
playerIcon = ""
playerName = ""
computerName = "Shakti(AI)"

# GameMode, 0 if Human vs Human, 1 if Human vs Robot
mode = 1

# Turn, 0 for first player, 1 for second player
turn = 0

#Miscellaneoud Variables
padButtons = [[Button(),Button(),Button()]]*3

# Method to destroy current window
def destroyWindow(root,frame):
    frame.pack_forget()
    root.update()

# Entry Animation
def switchWindow(root,entryFrame,exitFrame):
    initX = 0
    while initX!=-600:
        entryFrame.place(x=initX+600,y=0)
        exitFrame.place(x=initX,y=0)
        initX -= 20
        sleep(0.01)
        root.update()

# Methods that will be used in later stages
# Turn Selection screen

def setTurn(turnValue,frame):
    global turn
    turn = turnValue
    print(turn)
    # destroyWindow(root,frame)
    # newFrame = gameScreen()
    # switchWindow(root,newFrame,frame)

def turnSelection(root):
    global versusIcon
    global playerName
    global computerName
    frame = Frame(root,height=600,width=600,bg="white")
    welcomeLabel = Label(frame,bg="white", fg="orange", text="Choose player who'll charge first...",font = "Helvetica 16 bold italic")
    versusLabel = Label(frame,bg="white", image=versusIcon,width=600, height=200)
    firstNameLabel = Button(frame, bd=0,highlightthickness=0, bg="white", width=15,height=3, fg="red",text=playerName,font = "Helvetica 20 bold italic", command= lambda: setTurn(0,frame))
    secondNameLabel = Button(frame, bd=0,highlightthickness=0, bg="white",width=15,height=3, fg="blue",text=computerName,font = "Helvetica 20 bold italic", command= lambda: setTurn(1,frame))
    welcomeLabel.place(x=10,y=50)
    versusLabel.place(x=0,y=200)
    firstNameLabel.place(x=0,y=200)
    secondNameLabel.place(x=350, y=300)
    return frame

# Icon selection screen methods    
def changeIcon(choice,frame):
    global cross
    global zero
    if choice==0:
        playerIcon = cross
        computerIcon = zero
    else:
        playerIcon = zero
        computerIcon = cross
    destroyWindow(root,frame)
    newFrame = turnSelection(root)
    switchWindow(root,newFrame,frame)

def selectIcons(root):
    global cross
    global zero
    global computerIcon
    global playerIcon
    global playerName
    frame = Frame(root,height=600,width=600,bg="white")
    chooseLabel = Label(frame, bg = "white", fg="orange", text= playerName+", choose Your player icon...",justify="center",font = "Helvetica 16 bold italic")
    crossButton = Button(frame,bd=0,highlightthickness=0,bg="white", height=250, width=300,image=cross,command= lambda: changeIcon(0,frame))
    zeroButton = Button(frame,bd=0, highlightthickness=0,bg="white",height=250, width=300, image=zero, command= lambda: changeIcon(1,frame))
    chooseLabel.place(x=10,y=50)
    crossButton.place(x=0,y=175)
    zeroButton.place(x=300,y=175)
    return frame

# Asking name for players
def setPlayerNames(root,firstName,secondName,frame):
    global playerName
    global computerName
    playerName = firstName
    computerName = secondName
    destroyWindow(root,frame)
    newFrame = selectIcons(root)
    switchWindow(root,newFrame,frame)

def getPlayerNames(root):
    global nextButtonImage
    global mode
    playerLabelText = ""
    computerLabelText = ""
    if(mode==0):
        playerLabelText = "Enter name of first player"
        computerLabelText = "Enter Name of second player"
    else:
        playerLabelText = "Enter your name"
        computerLabelText = "Enter name for AI (Default is Shakti)"
    frame = Frame(root,height=600,width=600,bg="white")
    instructionLabel = Label(frame, bg = "white", fg="orange", text="Give Name to your players...", justify="center",font = "Helvetica 16 bold italic")
    playerLabel = Label(frame, bg = "white", fg="orange", text=playerLabelText, justify="center",font = "Helvetica 12 bold italic")
    computerLabel = Label(frame, bg = "white", fg="orange", text=computerLabelText, justify="center",font = "Helvetica 12 bold italic")
    playerEntry = Entry(frame,width=35,bd=3,highlightcolor="cyan",highlightbackground="orange",relief=RIDGE,bg="white",fg="blue", font=('Verdana',15))
    computerEntry = Entry(frame,width=35,bd=3,highlightcolor="cyan",highlightbackground="orange",relief=RIDGE,bg="white",fg="blue",font=('Verdana',15))
    if(mode==1):
        computerEntry.insert(0,"Shakti(AI)")
    nextButton = Button(frame, width=200, height=100, bd=0, bg="white",highlightthickness=0,image=nextButtonImage, command= lambda : setPlayerNames(root,playerEntry.get(), computerEntry.get(),frame))
    # entryAnimation(root,instructionLabel,10,50)
    instructionLabel.place(x=10,y=50)
    playerLabel.place(x=10,y=160)
    playerEntry.place(x=10,y=210)
    computerLabel.place(x=10,y=280)
    computerEntry.place(x=10,y=330)
    nextButton.place(x=200,y=475)
    return frame
  
# Game Mode Selection Screen Methods
def finalChooseMode(root,modeValue,frame):
    global mode
    mode = modeValue
    destroyWindow(root,frame)
    newFrame = getPlayerNames(root)
    switchWindow(root,newFrame,frame)

def chooseMode(root):
    global hvhImage
    global hvrImage
    global widgetsList
    frame = Frame(root,height=600,width=600,bg="white")
    welcomeLabel = Label(frame, bg = "white", fg="orange", text="Welcome, choose game mode...", justify="center",font = "Helvetica 16 bold italic")
    hvhButton = Button(frame,bd=0,highlightthickness=0,bg="white", height=250, width=300,image=hvhImage,command= lambda: finalChooseMode(root,0,frame))
    hvrButton = Button(frame,bd=0, highlightthickness=0,bg="white",height=250, width=300, image=hvrImage, command= lambda: finalChooseMode(root,1,frame))
    welcomeLabel.place(x=140,y=50)
    hvhButton.place(x=0,y=175)
    hvrButton.place(x=300,y=175)
    frame.place(x=0,y=0)

# Game screen
def pop(i,j):
    print(str(i)+","+str(j))

def gameScreen(root,mode,turn):
    global cross
    global zero
    global playerName
    global computerName
    global padButtons
    cross = cross.subsample(2)
    zero = zero.subsample(2)
    frame = Frame(root,height=600,width=600,bg="white")
    gameBoard = Frame(frame,bd=0,highlightthickness=0,height=400,width=400,bg="black")
    coordinates = [0,140,280]
    for i in range(3):
        for j in range(3):
            padButtons[i][j] = Button(gameBoard,bd=0,highlightthickness=0,width=120,height=120,bg="white",image=cross)
            padButtons[i][j].place(x=coordinates[j],y=coordinates[i])
            padButtons[i][j].bind('<Button-1>',lambda event,a=i,b=j:pop(a,b))
    gameBoard.place(x=100,y=50)
    frame.place(x=0,y=0)

width = 600
height = 600
root.title("Tic Tac Toe - Player vs AI")
root.geometry( str(width) + "x" + str(height))
root.configure(bg="white")

# Main Call
# chooseMode(root)
gameScreen(root,1,1)
root.mainloop()