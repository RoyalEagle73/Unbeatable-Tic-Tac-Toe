from tkinter import *
from PIL import Image
from PIL import ImageTk
from time import sleep
import random
from ailib import movePredictor

# Root window declaration
root = Tk()

# Logos and Images
cross = PhotoImage(file="crossLogo.png").subsample(2)
zero = PhotoImage(file="zeroLogo.png").subsample(2)
hvhImage = PhotoImage(file="hvh.png")
hvrImage = PhotoImage(file="hvr.png")
nextButtonImage = PhotoImage(file="nextButton.png").subsample(5)
versusIcon = PhotoImage(file="vsIcon.png").subsample(2)
placeHolderImage = PhotoImage(file="white.png").subsample(2)

# Player and Computer Icons
computerIcon = cross
playerIcon = zero
playerName = ""
computerName = "Shakti(AI)"

# GameMode, 0 if Human vs Human, 1 if Human vs Robot
mode = 0

# Turn, 0 for first player, 1 for second player
turn = 0

#Miscellaneoud Variables
padButtons = []
gameState = [] #-1 means empty, 0 means occupied by first player, 1 means occupied by 2nd player
for i in range(3):
    gameState.append([])
    padButtons.append([])
    for j in range(3):
        padButtons[i].append(Button())
        gameState[i].append(-1)

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
# Game screen
def matchStateCheck():
    global gameState
    predictor = movePredictor(gameState)
    if(predictor.wins(gameState,0)==True):
        print("Player 1 wins")
    elif(predictor.wins(gameState,1)==True):
        print("Player 2 wins")
    if len(predictor.empty_cells(gameState))==0 and predictor.game_over(gameState)==False:
        print("Match Draw")
    else:
        print("Match Still in action...")

def moveAI():
    global gameState
    global computerIcon
    global padButtons
    predictor = movePredictor(gameState)
    data = predictor.predictMove()
    aiX = data[0]
    aiY = data[1]
    gameState[aiX][aiY] = 1
    padButtons[aiX][aiY].configure(image=computerIcon)
    padButtons[aiX][aiY].unbind('<Button-1>')
    print(data)

def performAction(button,label,i,j):
    global turn
    global playerIcon
    global computerIcon
    global gameState
    global mode
    global root
    gameState[i][j] = turn
    root.update()
    if mode==1:
        print("Called from " + str(i) + "," + str(j))
        if turn==0:
            button["image"] = playerIcon 
            moveAI()
        else:
            moveAI()
    else:
        if turn==1:
            button["image"] = computerIcon
            turn = 0
            label["text"] = "It's " + playerName + "'s turn..."
            root.update()
        else:
            button["image"] = playerIcon 
            turn = 1
            label["text"] = "It's " + computerName + "'s turn..."
            root.update()
    button.unbind('<Button-1>')
    matchStateCheck()
    
def gameScreen(root):
    global playerName
    global computerName
    global padButtons
    global placeHolderImage
    global playerIcon
    global computerIcon
    global turn
    global playerName
    global computerName
    turnPlayerString = ""
    if turn==0:
        turnPlayerString = "It's " + playerName + "'s turn..."
    else:
        turnPlayerString = "It's " + computerName + "'s turn..."
    playerIcon = playerIcon.subsample(2)
    computerIcon = computerIcon.subsample(2)
    frame = Frame(root,height=600,width=600,bg="white")
    gameBoard = Frame(frame,bd=0,highlightthickness=0,height=400,width=400,bg="black")
    gameLabel = Label(frame,bg="white", fg="orange", text=turnPlayerString,font = "Helvetica 16 bold italic")
    coordinates = [0,140,280]
    for i in range(3):
        for j in range(3):
            padButtons[i][j] = Button(gameBoard,bd=0,highlightthickness=0,width=120,height=120,bg="white",image=placeHolderImage)
            padButtons[i][j].place(x=coordinates[j],y=coordinates[i])
            padButtons[i][j].bind('<Button-1>',lambda event,a=i,b=j,button=padButtons[i][j],label=gameLabel:performAction(button,label,a,b))
    gameBoard.place(x=100,y=50)
    gameLabel.place(x=50,y=500)
    frame.place(x=0,y=0)
    if(mode==1 and turn==1):
        moveAI()
        turn =0
    return frame

# Turn Selection screen
def setTurn(turnValue,frame):
    global turn
    turn = turnValue
    destroyWindow(root,frame)
    newFrame = gameScreen(root)
    switchWindow(root,newFrame,frame)

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
    global playerIcon
    global computerIcon
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
    
width = 600
height = 600
root.title("Tic Tac Toe - Player vs AI")
root.geometry( str(width) + "x" + str(height))
root.configure(bg="white")

# Main Call
# chooseMode(root)
gameScreen(root)
root.mainloop()