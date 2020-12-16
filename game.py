'''
Author: Deepak Chauhan
Github: https://github.com/RoyalEagle73/
'''
from tkinter import *
from PIL import Image
from PIL import ImageTk
from time import sleep
import random
from lib.ailib import movePredictor

# Root window declaration
root = Tk()

# Logos and Images
titleBackground = PhotoImage(file="images/titleBg.png")
turnBackground = PhotoImage(file="images/turnTitle.png")
cross = PhotoImage(file="images/crossLogo.png").subsample(2)
zero = PhotoImage(file="images/zeroLogo.png").subsample(2)
hvhImage = PhotoImage(file="images/hvh.png")
hvrImage = PhotoImage(file="images/hvr.png")
nextButtonImage = PhotoImage(file="images/nextButton.png").subsample(5)
versusIcon = PhotoImage(file="images/vsIcon.png").subsample(2)
placeHolderImage = PhotoImage(file="images/white.png").subsample(2)
retryImage = PhotoImage(file="images/retry.png")
homeImage = PhotoImage(file="images/home.png")

# Player and Computer Icons
computerIcon = cross
playerIcon = zero
playerName = ""
computerName = "Shakti(AI)"

# GameMode, 0 if Human vs Human, 1 if Human vs Robot
mode = 0

# Turn, 0 for first player, 1 for second player
turn = 0
turnBackupForNewGame = 0

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
    while initX>=-600:
        entryFrame.place(x=initX+600,y=0)
        exitFrame.place(x=initX,y=0)
        initX -= 20
        sleep(0.01)
        root.update()

def backAnimation(root,entryFrame,exitFrame):
    initX = -600
    while initX!=0:
        entryFrame.place(x=initX,y=0)
        exitFrame.place(x=initX+600,y=0)
        initX += 20
        sleep(0.01)
        root.update()

# Methods that will be used in later stages
# Game screen
def matchStateCheck():
    global gameState
    predictor = movePredictor(gameState)
    if(predictor.wins(gameState,0)==True):
        return 0
    elif(predictor.wins(gameState,1)==True):
        return 1
    if len(predictor.empty_cells(gameState))==0 and predictor.game_over(gameState)==False:
        return 2
    return -1

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

def performAction(button,label,frame,i,j):
    global turn
    global playerIcon
    global computerIcon
    global gameState
    global mode
    global root
    gameState[i][j] = turn
    root.update()
    if mode==1:
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
    matchResult = matchStateCheck()
    if matchResult!=-1:
        destroyWindow(root,frame)
        newFrame = resultScreen(root,matchResult)
        switchWindow(root,newFrame,frame)
    
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
    global turnBackupForNewGame
    global turnBackground
    turnBackupForNewGame = turn
    turnPlayerString = ""
    if turn==0:
        turnPlayerString = "It's " + playerName + "'s turn..."
    else:
        turnPlayerString = "It's " + computerName + "'s turn..."
    playerIcon = playerIcon.subsample(2)
    computerIcon = computerIcon.subsample(2)
    frame = Frame(root,height=600,width=600,bg="white")
    turnBackgroundLabel = Label(frame,bg="white",image=turnBackground, width=600, height=100)
    gameBoard = Frame(frame,bd=0,highlightthickness=0,height=400,width=400,bg="black")
    gameLabel = Label(frame,bg="#33ffff", fg="#ef3e67", text=turnPlayerString,font = "times 14 bold")
    coordinates = [0,140,280]
    for i in range(3):
        for j in range(3):
            padButtons[i][j] = Button(gameBoard,bd=0,highlightthickness=0,width=120,height=120,bg="white",image=placeHolderImage)
            padButtons[i][j].place(x=coordinates[j],y=coordinates[i])
            padButtons[i][j].bind('<Button-1>',lambda event,a=i,b=j,button=padButtons[i][j],label=gameLabel,f=frame:performAction(button,label,f,a,b))
    gameBoard.place(x=100,y=50)
    turnBackgroundLabel.place(x=0,y=490)
    gameLabel.place(x=160,y=525)
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
    global titleBackground
    frame = Frame(root,height=600,width=600,bg="white")
    titleBackgroundLabel = Label(frame,bg="white",image=titleBackground, width=600, height=100)
    welcomeLabel = Label(frame,bg="#3bc1cd", fg="#ef3e67", text="Choose player who'll charge first...",font = "times 20 bold italic")
    versusLabel = Label(frame,bg="white", image=versusIcon,width=600, height=200)
    firstNameLabel = Button(frame, bd=0,highlightthickness=0, bg="white", width=15,height=3, fg="red",text=playerName,font = "times 20 bold italic", command= lambda: setTurn(0,frame))
    secondNameLabel = Button(frame, bd=0,highlightthickness=0, bg="white",width=15,height=3, fg="blue",text=computerName,font = "times 20 bold italic", command= lambda: setTurn(1,frame))
    welcomeLabel.place(x=120,y=35)
    versusLabel.place(x=0,y=200)
    firstNameLabel.place(x=0,y=200)
    secondNameLabel.place(x=350, y=300)
    titleBackgroundLabel.place(x=0,y=0)
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
    global titleBackground
    frame = Frame(root,height=600,width=600,bg="white")
    titleBackgroundLabel = Label(frame,bg="white",image=titleBackground, width=600, height=100)
    chooseLabel = Label(frame, bg = "#3bc1cd", fg="#ef3e67", text= playerName+", choose Your player icon...",justify="center",font = "times 16 bold italic")
    crossButton = Button(frame,bd=0,highlightthickness=0,bg="white", height=250, width=300,image=cross,command= lambda: changeIcon(0,frame))
    zeroButton = Button(frame,bd=0, highlightthickness=0,bg="white",height=250, width=300, image=zero, command= lambda: changeIcon(1,frame))
    chooseLabel.place(x=140,y=35)
    crossButton.place(x=0,y=175)
    zeroButton.place(x=300,y=175)
    titleBackgroundLabel.place(x=0,y=0)
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
    global titleBackground
    playerLabelText = ""
    computerLabelText = ""
    if(mode==0):
        playerLabelText = "Enter name of first player"
        computerLabelText = "Enter Name of second player"
    else:
        playerLabelText = "Enter your name"
        computerLabelText = "Enter name for AI (Default is Shakti)"
    frame = Frame(root,height=600,width=600,bg="white")
    titleBackgroundLabel = Label(frame,bg="white",image=titleBackground, width=600, height=100)
    instructionLabel = Label(frame, bg = "#3bc1cd", fg="#ef3e67", text="Give Name to your players...", justify="center",font = "times 20 bold italic")
    playerLabel = Label(frame, bg = "white", fg="#ef3e67", text=playerLabelText, justify="center",font = "times 12 bold italic")
    computerLabel = Label(frame, bg = "white", fg="#ef3e67", text=computerLabelText, justify="center",font = "times 12 bold italic")
    playerEntry = Entry(frame,width=35,bd=3,highlightcolor="cyan",highlightbackground="#ef3e67",relief=RIDGE,bg="white",fg="blue", font=('Verdana',15))
    computerEntry = Entry(frame,width=35,bd=3,highlightcolor="cyan",highlightbackground="#ef3e67",relief=RIDGE,bg="white",fg="blue",font=('Verdana',15))
    if(mode==1):
        computerEntry.insert(0,"Shakti(AI)")
    nextButton = Button(frame, width=200, height=100, bd=0, bg="white",highlightthickness=0,image=nextButtonImage, command= lambda : setPlayerNames(root,playerEntry.get(), computerEntry.get(),frame))
    instructionLabel.place(x=160,y=35)
    playerLabel.place(x=10,y=160)
    playerEntry.place(x=10,y=210)
    computerLabel.place(x=10,y=280)
    computerEntry.place(x=10,y=330)
    nextButton.place(x=200,y=475)
    titleBackgroundLabel.place(x=0,y=0)
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
    global titleBackground
    frame = Frame(root,height=600,width=600,bg="white")
    humanVsHumanLabel = Label(frame,bg="white",fg="red",text="Human Vs Human",font="times 15 bold italic")
    humanVsAILabel = Label(frame,bg="white",fg="blue",text="Human Vs AI",font="times 15 bold italic")
    titleBackgroundLabel = Label(frame,bg="white",image=titleBackground, width=600, height=100)
    welcomeLabel = Label(frame, bg = "#3bc1cd", fg="#ef3e67", text="Welcome, choose game mode...", justify="center",font = "times 20 bold italic")
    hvhButton = Button(frame,bd=0,highlightthickness=0,bg="white", height=250, width=300,image=hvhImage,command= lambda: finalChooseMode(root,0,frame))
    hvrButton = Button(frame,bd=0, highlightthickness=0,bg="white",height=250, width=300, image=hvrImage, command= lambda: finalChooseMode(root,1,frame))
    welcomeLabel.place(x=140,y=35)
    titleBackgroundLabel.place(x=0,y=0)
    humanVsHumanLabel.place(x=50,y=450)
    humanVsAILabel.place(x=375,y=450)
    hvhButton.place(x=0,y=175)
    hvrButton.place(x=300,y=175)
    frame.place(x=0,y=0)
    return frame
    
# Result Screen
def goHome(root,frame):
    global mode
    destroyWindow(root,frame)
    newFrame = chooseMode(root)
    switchWindow(root,newFrame,frame)

def resetGameBoard():
    global gameState
    for row in gameState:
        for i in range(3):
            row[i] = -1
    
def newGame(root,currentFrame):
    global turn
    global turnBackupForNewGame
    resetGameBoard()
    turn = turnBackupForNewGame
    newFrame = gameScreen(root)
    backAnimation(root,newFrame,currentFrame)
    destroyWindow(root,currentFrame)

def resultScreen(root,winner):
    global playerName
    global computerName
    global playerIcon
    global computerIcon
    global retryImage
    global homeImage
    playerIcon = playerIcon.zoom(2)
    computerIcon = computerIcon.zoom(2)
    mainFrame = Frame(root,height=600,width=600,bg="white")
    winnerFrame = Frame(mainFrame,width=600,height=200)
    playerImageLabel = Label(winnerFrame, image=playerIcon, width=200,height=200,bg="white")
    computerImageLabel = Label(winnerFrame, image=computerIcon, width=200,height=200,bg="white")
    titleBackgroundLabel = Label(mainFrame,bg="white",image=titleBackground, width=600, height=100)
    if(winner==2):
        playerImageLabel.pack(side=LEFT)
        computerImageLabel.pack(side=RIGHT)
        winnerFrame.place(x=100,y=150)
        status = "Match Draw !!"
    else:
        if winner==1:
            computerImageLabel.pack(side=TOP)
            status = computerName + " Won !!"
        else:
            playerImageLabel.pack(side=TOP)
            status = playerName + " Won !!"
        winnerFrame.place(x=200,y=150)
    titleBackgroundLabel.place(x=0,y=0)
    matchStatusLabel = Label(mainFrame,text=status,bg="#3bc1cd",fg="#ef3e67",anchor="center",font = "times 20 bold italic")
    if status=="Match Draw !!":
        matchStatusLabel.place(x=210,y=35)
    else:
        matchStatusLabel.place(x=140,y=35)
    retryButton = Button(mainFrame,image=retryImage,width=400,height=100,bg="white",bd=0,highlightthickness=0, command= lambda : newGame(root, mainFrame))
    retryButton.place(x=100,y=370)
    homeButton = Button(mainFrame,image=homeImage,width=400,height=100,bg="white",bd=0,highlightthickness=0,command=lambda: goHome(root,mainFrame))
    homeButton.place(x=100,y=470)
    mainFrame.place(x=0,y=0)
    return mainFrame

width = 600
height = 600
root.title("Tic Tac Toe - Revamped")
root.geometry( str(width) + "x" + str(height))
root.configure(bg="white")

# Main Call
chooseMode(root)
root.mainloop()