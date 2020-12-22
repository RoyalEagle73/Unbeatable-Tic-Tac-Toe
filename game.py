'''
Author: Deepak Chauhan
Github: https://github.com/RoyalEagle73/
'''
from tkinter import *
from PIL import Image
from PIL import ImageTk
from time import sleep
from lib.dbHandler import databaseHandler
from lib.ailib import movePredictor

# Database object
db = databaseHandler()
data = [] #List to contain data
clearTableCode = 0 #0 for HumanVHuman Table and 1 for HumanVAI Table

# Root window declaration
root = Tk()

# Logos and Images
nitJsrLogo = PhotoImage(file="images/nitJsrLogo.png").subsample(2)
letsPlayImage = PhotoImage(file="images/letsPlay.png")
aboutUsImage = PhotoImage(file="images/aboutUs.png")
recordsImage = PhotoImage(file="images/records.png")
logo = PhotoImage(file="images/logo.png").subsample(4)
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
playerName = "Deepak"
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
def switchWindow(root,entryFrame,exitFrame,toLeft=True):
    initX = 0
    if toLeft==True:
        while initX>=-600:
            entryFrame.place(x=initX+600,y=0)
            exitFrame.place(x=initX,y=0)
            initX -= 20
            sleep(0.01)
            root.update()
    else:
        while initX<=600:
            entryFrame.place(x=initX-600,y=0)
            exitFrame.place(x=initX,y=0)
            initX += 20
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
    global computerIconplayer
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
    resetButton = Button(frame,width=15,height=1,fg="#ff0000",bg="#f2fc9f", bd=0, highlightthickness=0,text="Reset Game ⟳", justify="center",font="times 18 bold italic", command= lambda: resetGame(root,frame))
    coordinates = [0,140,280]
    for i in range(3):
        for j in range(3):
            padButtons[i][j] = Button(gameBoard,bd=0,highlightthickness=0,width=120,height=120,bg="white",image=placeHolderImage)
            padButtons[i][j].place(x=coordinates[j],y=coordinates[i])
            padButtons[i][j].bind('<Button-1>',lambda event,a=i,b=j,button=padButtons[i][j],label=gameLabel,f=frame:performAction(button,label,f,a,b))
    turnBackgroundLabel.place(x=0,y=0)
    gameLabel.place(x=160,y=35)
    gameBoard.place(x=100,y=100)
    resetButton.place(x=195,y=535)
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
def goHome(root,frame,toRight=True):
    global mode
    destroyWindow(root,frame)
    newFrame = homeScreen(root)
    switchWindow(root,newFrame,frame,toRight)

def resetGame(root,currentFrame):
    global playerIcon
    global computerIcon
    playerIcon = playerIcon.zoom(2)
    computerIcon = computerIcon.zoom(2)
    newGame(root,currentFrame)
    
def resetGameBoard():
    global gameState
    for row in gameState:
        for i in range(3):
            row[i] = -1
    
def newGame(root,currentFrame):
    global turn
    global turnBackupForNewGame
    global playerIcon
    global computerIcon
    resetGameBoard()
    turn = turnBackupForNewGame
    newFrame = gameScreen(root)
    backAnimation(root,newFrame,currentFrame)
    destroyWindow(root,currentFrame)

def resultScreen(root,winner):
    global mode
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
        db.incrementScore("Draw",mode)
    else:
        if winner==1:
            computerImageLabel.pack(side=TOP)
            status = computerName + " Won !!"
            if mode==1:
                db.incrementScore("Computer",mode)
            else:
                db.incrementScore(computerName,mode)
        else:
            db.incrementScore(playerName,mode)
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

def homeScreenSwitch(root,frame, switchTo):
    destroyWindow(root,frame)
    switchWindow(root,switchTo,frame)

def homeScreen(root):
    global logo
    global aboutUsImage
    global recordsImage
    global letsPlayImage
    frame = Frame(root, width=600, height=600, bg="white")
    logoImageLabel = Label(frame, bg="white", image=logo, bd=0, highlightthickness=0)
    letsPlayButton = Button(frame, bg="white", image=letsPlayImage, bd=0, highlightthickness=0,command=lambda: homeScreenSwitch(root,frame,chooseMode(root)))
    aboutUsButton = Button(frame, bg="white", image=aboutUsImage, bd=0, highlightthickness=0,command=lambda: homeScreenSwitch(root,frame,infoScreen(root)))
    recordsButton = Button(frame, bg="white", image=recordsImage, bd=0, highlightthickness=0,command=lambda: homeScreenSwitch(root,frame,dbScreen(root)))
    logoImageLabel.place(x=50, y=0)
    letsPlayButton.place(x=200, y=300)
    aboutUsButton.place(x=200,y=400) 
    recordsButton.place(x=200,y=500)
    frame.place(x=0,y=-0)
    return frame

def getDatabaseData(value,changeButton,oldButton,frame):
    global db
    global data
    global clearTableCode
    if value==2:
        db.clearTable(clearTableCode)
    else:
        changeButton.configure(bg="white",fg="red")
        oldButton.configure(bg="grey",fg="black")
        clearTableCode = value
    data = db.returnTable(clearTableCode)
    if len(data) > 10:
        rowSize = 10
    else:
        rowSize = len(data)
    nameLabel = Label(frame, width=30,text="NAME",fg='red',bg="khaki", justify="center",font=('times',16,'bold italic'))
    scoreLabel = Label(frame, width=30,text="SCORE",fg='red',bg="khaki", font=('times',16,'bold italic'))
    nameLabel.grid(row=0, column=0,pady=10) 
    scoreLabel.grid(row=0, column=1,pady=10)
    frame.configure(bg="light sky blue")
    for i in range(10): 
        for j in range(2):
            if i%2==0:
                bgColor = "light salmon"
            else:
                bgColor = "light salmon"
            displayText = ""
            if i<len(data):
                displayText = str(data[i][j])
            e = Label(frame, width=30,text=displayText,bg=bgColor,fg='blue', font=('times',16,'italic')) 
            e.grid(row=i+1, column=j,pady=10) 
    print(data)

def dbScreen(root):
    global data
    frame = Frame(root, width=600, height=600, bg="white")
    buttonFrame = Frame(frame,bg="white")
    dataFrame = Frame(frame,bg="white")
    resetButtonFrame = Frame(frame,bg="white")
    dbButtonHvH = Button(buttonFrame,bd=0,width=25,bg="white",highlightthickness=0, text="Human v/s Human", font="times 16 bold italic")
    dbButtonHvAI = Button(buttonFrame,bd=0,width=25,bg="white",highlightthickness=0, text="Human v/s AI", font="times 16 bold italic")
    dbButtonHvH.configure(command=lambda value=0,changeButton=dbButtonHvH,oldButton=dbButtonHvAI,frame=dataFrame : getDatabaseData(value,changeButton,oldButton,frame))
    dbButtonHvAI.configure(command=lambda value=1,changeButton=dbButtonHvAI,oldButton=dbButtonHvH,frame=dataFrame: getDatabaseData(value,changeButton,oldButton,frame))
    resetButton = Button(frame,text="⚠ Reset Records ⚠", bd=1, highlightthickness=0,bg="khaki", fg="red",font="times 12 bold italic")
    resetButton.configure(command=lambda value=2,changeButton=dbButtonHvH,oldButton=dbButtonHvAI,frame=dataFrame : getDatabaseData(value,changeButton,oldButton,frame))
    homeButton = Button(frame,text="Go Home 🏠", bd=1, highlightthickness=0,bg="khaki", fg="green",font="times 12 bold italic",command=lambda: goHome(root,frame,False))
    buttonFrame.place(x=0,y=0)
    dbButtonHvH.pack(side=LEFT)
    dbButtonHvAI.pack(side=RIGHT)
    dataFrame.place(x=0,y=50)
    resetButton.place(x=320,y=565)
    homeButton.place(x=100,y=565)
    resetButtonFrame.place(x=00,y=500)
    frame.place(x=0,y=0)
    dbButtonHvH.invoke()
    return frame

def infoScreen(root):
    global nitJsrLogo
    developersName = "Vipin Singh Negi\nShobhit Verma\nAmit Gupta\nAbhishek Mishra\nKrishna\nDeepak Chauhan\nAparna Yaduvanshi"
    rollNumbers = "(2018PGCACA58)\n(2018PGCACA59)\n(2018PGCACA60)\n(2018PGCACA61)\n(2018PGCACA62)\n(2018PGCACA63)\n(2018PGCACA65)"
    frame = Frame(root, width=600, height=600, bg="white")
    homeButton = Button(frame,text="Go Home 🏠", bd=1, highlightthickness=0,bg="khaki", fg="green",font="times 12 bold italic",command=lambda: goHome(root,frame,False))
    nitJsrNameLabel = Label(frame, text = "National Institute of Technology\nJamshedpur",bg="white", fg="black",font="times 22 bold italic")
    nitJsrLogoLabel = Label(frame, image = nitJsrLogo, bg="white")
    professorNameLabel = Label(frame, text = "A Decision Support System Assignment under the supervision of\nDr. Dilip Kumar Shaw\n(Associate Professor and Head of Department)\nDepartment of Computer Application",bg="white", fg="black",font="times 14 italic")
    developedByLabel = Label(frame, text = "Developed By:",bg="white", fg="black",font="times 15 bold")
    namesLabel = Label(frame, text = developersName,bg="white", fg="black",justify="left",font="times 14 italic")
    rollNumberLabel = Label(frame,text=rollNumbers,bg="white", fg="black",justify="left",font="times 14 italic")
    nitJsrNameLabel.place(x=100,y=10)
    nitJsrLogoLabel.place(x=230,y=90)
    professorNameLabel.place(x=70,y=280)
    developedByLabel.place(x=10,y=380)
    namesLabel.place(x=10,y=405)
    rollNumberLabel.place(x=300,y=405)
    homeButton.place(x=230,y=565)
    frame.place(x=0,y=0)
    return frame

width = 600
height = 600
root.title("Tic Tac Toe - Revamped")
root.geometry( str(width) + "x" + str(height))
root.configure(bg="white")

# Main Call
homeScreen(root)
root.mainloop()