# FinalProject.py
# Russell Doucet
# Russ
# rcdoucet@syr.edu
### Jeopardy ####
# A classic game of Jeopardy! Categories, Questions and Answers will be
# be imported through a file. The game can run with two players, updating
# their current score at the top of the screen. First person to $1600 wins the game!
# At the end a file will be outputted with Player names and scores.
#################
from graphics import *
from random import *


# CLOD
class Question:
    # The constructor: Initializes the size, category, value of the question. The constructor also takes in the window
    # in which the question wants to be drawn in while also taking in the actual question as a parameter as well.
    def __init__(self, p1, p2, category, question, answer, value, window):
        self.p1 = p1
        self.p2 = p2
        self.category = category
        self.question = question
        self.answer = answer
        self.value = value
        self.window = window

        drawButton(window, self.value, self.p1, self.p2, "Amatic SC")

    def getQuestion(self):
        return self.question

    def checkAnswer(self, user_answer):
        if user_answer == self.answer:
            return True
        else:
            return False

    def getValue(self):
        return self.value

    def getCategory(self):
        return self.category


def removeBox(box):
    box.undraw()


def processFile(filename):
    # IFL
    # Creating two empty lists that will eventually be filled with questions and answers
    listQ = [""] * 4
    listA = [""] * 4

    infile = open(filename, "r")
    infile.readline()
    lineList = infile.readlines()
    isQuestion = True
    count = 0

    # Counts through the lines in the file and takes the first four lines, not including the first one,
    # and initializes a list using all of the questions from the file
    while isQuestion:
        if count == 4:
            isQuestion = False
        else:
            listQ[count] = lineList[count]
            count += 1

    # Initializing a list with all of the answers to the questions defined above
    for i in range(4):
        listA[i] = lineList[count + 1]
        count += 1

    # Making sure to get rid of the unwanted new-line characters within each answer
    for i in range(len(listQ)):
        listQ[i] = listQ[i].strip('\n')
        listA[i] = listA[i].strip('\n')
    return listQ, listA


# Custom built Rectangle function that allows the user to to make a rectangle of any size and place text in the center
# of the rectangle all in one step.
def drawButton(win, value, p1, p2, font):
    button = Rectangle(Point(p1.getX(), p1.getY()), Point(p2.getX(), p2.getY()))
    button.draw(win)

    phrase = Text(Point((p1.getX() + p2.getX())/2, (p1.getY() + p2.getY())/2), value)
    phrase.setFace(font)
    phrase.draw(win)


# A function that takes in the phrase the user wants to draw. Then uses a centerpoint, font and size for the text
# allow the user to customize the text they are drawing with fewer graphics functions.
def drawText(phrase, centerpoint, font, size):
    text = Text(centerpoint, phrase)
    text.setFace(font)
    text.setSize(size)
    return text


# Function takes in the last point the users clicked along the bounds of the selected area; if the mouse click
# is within the bounded area, then the function returns true, if not, the function returns false.
def checkButtonClick(clickedpoint, lower_left, upper_right):
    # IMS
    clickedPointX = clickedpoint.getX()
    clickedPointY = clickedpoint.getY()
    if (lower_left.getX() < clickedPointX < upper_right.getX()) and (lower_left.getY() < clickedPointY < upper_right.getY()):
        return True
    else:
        return False


# Function sets-up and draws the Login Window. This is where players will choose their names and start the game!
def setupLoginWindow():
    user1name = ""
    user2name = ""
    # Creating the user login window for the game
    loginWindow = GraphWin("Player Setup Window", 500, 500)
    loginWindow.setCoords(0, 0, 10, 10)
    loginWindow.setBackground("orange")
    drawButton(loginWindow, "User1", Point(1, 8), Point(5, 8.5), "Amatic SC")
    drawButton(loginWindow, "User2", Point(1, 7), Point(5, 7.5), "Amatic SC")

    # Header
    # FNC
    jeopardy_header = drawText("SYRACUSE JEOPARDY", Point(5, 9), "Amatic SC", 18)
    jeopardy_header.draw(loginWindow)

    # IEB
    # Box entry for the first user's name
    user1Entry = Entry(Point(6, 8.25), 10)
    user1Entry.draw(loginWindow)
    drawButton(loginWindow, "Setname", Point(7, 8), Point(9, 8.5), "Amatic SC")
    # Box entry for the second user's name
    user2Entry = Entry(Point(6, 7.25), 10)
    user2Entry.draw(loginWindow)
    drawButton(loginWindow, "Setname", Point(7, 7), Point(9, 7.5), "Amatic SC")

    chosen = False
    playerCount = 0

    # Makes sure that the Game won't be able to start until both players have chosen their names
    while not chosen and playerCount < 2:
        lastClick = loginWindow.getMouse()
        print(lastClick)
        user1final = checkButtonClick(lastClick, Point(7, 8), Point(9, 8.5))
        user2final = checkButtonClick(lastClick, Point(7, 7), Point(9, 7.5))
        # Checks if User 1 has clicked the set name button, if so, sets User 1's name to the inputted value.
        if user1final:
            # OTXT
            playerCount += 1
            player1Confirmation = drawText("Player 1 Chosen!", Point(5, 5), "Amatic SC", 15)
            player1Confirmation.draw(loginWindow)
            user1name = user1Entry.getText()
        # Checks if User 2 has clicked the set name button, if so, sets User 2's name to the inputted value.
        if user2final:
            playerCount += 1
            player2Confirmation = drawText("Player 2 Chosen!", Point(5, 4), "Amatic SC", 15)
            player2Confirmation.draw(loginWindow)
            user2name = user2Entry.getText()
        # If both playes have chosen their names, chosen becomes True and the game is able to begin
        if playerCount == 2:
            chosen = True
    drawButton(loginWindow, "Start the Game!", Point(4, 1), Point(6, 2), "Amatic SC")
    clicked_point = loginWindow.getMouse()
    if checkButtonClick(clicked_point, Point(4, 1), Point(6, 2)):
        loginWindow.quit()
    return user1name, user2name


def setUpQuestions(window):
    category1List = []
    category2List = []
    category3List = []
    category4List = []

    # Creating the four category objects by inputting designated Question and Answer Files. Creates a list of
    cat1Q, cat1A = processFile("SyracuseCategory.txt")
    cat2Q, cat2A = processFile("HistoryCategory.txt")
    cat3Q, cat3A = processFile("ScienceCategory.txt")
    cat4Q, cat4A = processFile("RandomCategory.txt")

    # Initializing all of the questions, their values, and their answers, then draws them within the game window.
    cat1_question1 = Question(Point(-8, 2), Point(-5, 3), "Syracuse Trivia!", cat1Q[0], cat1A[0], 100, window)
    cat1_question2 = Question(Point(-8, 0), Point(-5, 1), "Syracuse Trivia!", cat1Q[1], cat1A[1], 200, window)
    cat1_question3 = Question(Point(-8, -2), Point(-5, -1), "Syracuse Trivia!", cat1Q[2], cat1A[2], 300, window)
    cat1_question4 = Question(Point(-8, -4), Point(-5, -3), "Syracuse Trivia!", cat1Q[3], cat1A[3], 400, window)
    # LOOD
    category1List.extend((cat1_question1, cat1_question2, cat1_question3, cat1_question4))

    # Initializing all of the questions, their values, and their answers, then draws them within the game window.
    cat2_question1 = Question(Point(-4, 2), Point(-1, 3), "United States History", cat2Q[0], cat2A[0], 100, window)
    cat2_question2 = Question(Point(-4, 0), Point(-1, 1), "United States History", cat2Q[1], cat2A[1], 200, window)
    cat2_question3 = Question(Point(-4, -2), Point(-1, -1), "United States History", cat2Q[2], cat2A[2], 300, window)
    cat2_question4 = Question(Point(-4, -4), Point(-1, -3), "United States History", cat2Q[3], cat2A[3], 400, window)
    # LOOD
    category2List.extend((cat2_question1, cat2_question2, cat2_question3, cat2_question4))

    # Initializing all of the questions, their values, and their answers, then draws them within the game window.
    cat3_question1 = Question(Point(0, 2), Point(3, 3), "Science!", cat3Q[0], cat3A[0], 100, window)
    cat3_question2 = Question(Point(0, 0), Point(3, 1), "Science!", cat3Q[1], cat3A[1], 200, window)
    cat3_question3 = Question(Point(0, -2), Point(3, -1), "Science!", cat3Q[2], cat3A[2], 300, window)
    cat3_question4 = Question(Point(0, -4), Point(3, -3), "Science!", cat3Q[3], cat3A[3], 400, window)
    # LOOD
    category3List.extend((cat3_question1, cat3_question2, cat3_question3, cat3_question4))

    # Initializing all of the questions, their values, and their answers, then draws them within the game window.
    cat4_question1 = Question(Point(4, 2), Point(7, 3), "Random!", cat4Q[0], cat4A[0], 100, window)
    cat4_question2 = Question(Point(4, 0), Point(7, 1), "Random!", cat4Q[1], cat4A[1], 200, window)
    cat4_question3 = Question(Point(4, -2), Point(7, -1), "Random!", cat4Q[2], cat4A[2], 300, window)
    cat4_question4 = Question(Point(4, -4), Point(7, -3), "Random!", cat4Q[3], cat4A[3], 400, window)
    # LOOD
    category4List.extend((cat4_question1, cat4_question2, cat4_question3, cat4_question4))

    return category1List, category2List, category3List, category4List


def clickedQuestion(cq_click, turn, score1, score2, win, c_clicked, catList, p1, p2, index, qclicked):
    if cq_click and not c_clicked:
        if turn == 0:
            score1 = questionWindow(catList[index], score1)
            question_cover1a = Rectangle(p1, p2)
            question_cover1a.setFill("grey")
            question_cover1a.draw(win)
            c_clicked = True
        elif turn == 1:
            score2 = questionWindow(catList[index], score2)
            question_cover1b = Rectangle(p1, p2)
            question_cover1b.setFill("grey")
            question_cover1b.draw(win)
            c_clicked = True
        qclicked = True
    return score1, score2, c_clicked, qclicked


def startMainWindow():
    # Creating the four category objects by inputting designated Question and Answer Files. Creates a list of
    # cat1Q, cat1A = processFile("SyracuseCategory.txt")
    # cat2Q, cat2A = processFile("HistoryCategory.txt")
    # cat3Q, cat3A = processFile("ScienceCategory.txt")
    # cat4Q, cat4A = processFile("RandomCategory.txt")

    # Creating Boolean variables that will become True once the user has clicked the specified question. Will use this
    # to ensure that someone isn't allowed to choose the same question over and over again. (The first number stands for
    # the category and the second number stands for which question it is within that category)
    c11_clicked, c12_clicked, c13_clicked, c14_clicked = False, False, False, False
    c21_clicked, c22_clicked, c23_clicked, c24_clicked = False, False, False, False
    c31_clicked, c32_clicked, c33_clicked, c34_clicked = False, False, False, False
    c41_clicked, c42_clicked, c43_clicked, c44_clicked = False, False, False, False

    score1, score2, turn = 0, 0, 0

    # GW
    color_list = ["blue", "orange", "purple", "green"]
    win = GraphWin("It's Time to Play Jeopardy!", 1000, 1000)
    win.setCoords(-10, -10, 10, 10)

    # RND
    win.setBackground(color_list[randrange(0, len(color_list))])

    cat1List, cat2List, cat3List, cat4List = setUpQuestions(win)

    main_header = drawText("Welcome To Jeopardy!", Point(0, 8), "Amatic SC", 25)
    main_header.draw(win)

    user1_header = drawText(u1name + "'s Score:", Point(-6, 6), "Amatic SC", 18)
    user1_header.draw(win)

    user2_header = drawText(u2name + "'s Score:", Point(6, 6), "Amatic SC", 18)
    user2_header.draw(win)

    while score1 < 1000 and score2 < 1000:
        # Creating a boolean to track whether or not the user has a clicked a question
        question_clicked = False
        scoreboard1 = drawText(str(score1), Point(-4, 6), "Amatic SC", 18)
        scoreboard1.draw(win)

        scoreboard2 = drawText(str(score2), Point(8, 6), "Amatic SC", 18)
        scoreboard2.draw(win)

        last_click = win.getMouse()

        # Creating boolean variables for each question's dimensions, allows me to check whether the user has clicked on
        # a specific question or not.
        c1q1_click = checkButtonClick(last_click, Point(-8, 2), Point(-5, 3))
        c1q2_click = checkButtonClick(last_click, Point(-8, 0), Point(-5, 1))
        c1q3_click = checkButtonClick(last_click, Point(-8, -2), Point(-5, -1))
        c1q4_click = checkButtonClick(last_click, Point(-8, -4), Point(-5, -3))

        # Passes in the most recent clicked point, current turn, player scores and other information in order
        # to determine whether the player has clicked on a question box. If the player clicks on the question box
        # and enters an answer, score1, score2, and the clicked variable will change respectively.

        score1, score2, c11_clicked, question_clicked = clickedQuestion(c1q1_click, turn, score1, score2, win, c11_clicked, cat1List,
                                                      Point(-8, 2), Point(-5, 3), 0, question_clicked)
        score1, score2, c12_clicked, question_clicked = clickedQuestion(c1q2_click, turn, score1, score2, win, c12_clicked, cat1List,
                                                      Point(-8, 0), Point(-5, 1), 1, question_clicked)
        score1, score2, c13_clicked, question_clicked = clickedQuestion(c1q3_click, turn, score1, score2, win, c13_clicked, cat1List,
                                                      Point(-8, -2), Point(-5, -1), 2, question_clicked)
        score1, score2, c14_clicked, question_clicked = clickedQuestion(c1q4_click, turn, score1, score2, win, c14_clicked, cat1List,
                                                      Point(-8, -4), Point(-5, -3), 3, question_clicked)

        # Creating boolean variables for each question's dimensions, allows me to check whether the user has clicked on
        # a specific question or not.
        c2q1_click = checkButtonClick(last_click, Point(-4, 2), Point(-1, 3))
        c2q2_click = checkButtonClick(last_click, Point(-4, 0), Point(-1, 1))
        c2q3_click = checkButtonClick(last_click, Point(-4, -2), Point(-1, -1))
        c2q4_click = checkButtonClick(last_click, Point(-4, -4), Point(-1, -3))

        # Passes in the most recent clicked point, current turn, player scores and other information in order
        # to determine whether the player has clicked on a question box. If the player clicks on the question box
        # and enters an answer, score1, score2, and the clicked variable will change respectively.

        score1, score2, c21_clicked, question_clicked = clickedQuestion(c2q1_click, turn, score1, score2, win, c21_clicked, cat2List,
                                                      Point(-4, 2), Point(-1, 3), 0, question_clicked)
        score1, score2, c22_clicked, question_clicked = clickedQuestion(c2q2_click, turn, score1, score2, win, c22_clicked, cat2List,
                                                      Point(-4, 0), Point(-1, 1), 1, question_clicked)
        score1, score2, c23_clicked, question_clicked = clickedQuestion(c2q3_click, turn, score1, score2, win, c23_clicked, cat2List,
                                                      Point(-4, -2), Point(-1, -1), 2, question_clicked)
        score1, score2, c24_clicked, question_clicked = clickedQuestion(c2q4_click, turn, score1, score2, win, c24_clicked, cat2List,
                                                      Point(-4, -4), Point(-1, -3), 3, question_clicked)

        # Creating boolean variables for each question's dimensions, allows me to check whether the user has clicked on
        # a specific question or not.
        c3q1_click = checkButtonClick(last_click, Point(0, 2), Point(3, 3))
        c3q2_click = checkButtonClick(last_click, Point(0, 0), Point(3, 1))
        c3q3_click = checkButtonClick(last_click, Point(0, -2), Point(3, -1))
        c3q4_click = checkButtonClick(last_click, Point(0, -4), Point(3, -3))

        # Passes in the most recent clicked point, current turn, player scores and other information in order
        # to determine whether the player has clicked on a question box. If the player clicks on the question box
        # and enters an answer, score1, score2, and the clicked variable will change respectively.

        score1, score2, c31_clicked, question_clicked = clickedQuestion(c3q1_click, turn, score1, score2, win, c31_clicked, cat3List,
                                                      Point(0, 2), Point(3, 3), 0, question_clicked)
        score1, score2, c32_clicked, question_clicked = clickedQuestion(c3q2_click, turn, score1, score2, win, c32_clicked, cat3List,
                                                      Point(0, 0), Point(3, 1), 1, question_clicked)
        score1, score2, c33_clicked, question_clicked = clickedQuestion(c3q3_click, turn, score1, score2, win, c33_clicked, cat3List,
                                                      Point(0, -2), Point(3, -1), 2, question_clicked)
        score1, score2, c34_clicked, question_clicked = clickedQuestion(c3q4_click, turn, score1, score2, win, c34_clicked, cat3List,
                                                      Point(0, -4), Point(3, -3), 3, question_clicked)

        # Creating boolean variables for each question's dimensions, allows me to check whether the user has clicked on
        # a specific question or not.
        c4q1_click = checkButtonClick(last_click, Point(4, 2), Point(7, 3))
        c4q2_click = checkButtonClick(last_click, Point(4, 0), Point(7, 1))
        c4q3_click = checkButtonClick(last_click, Point(4, -2), Point(7, -1))
        c4q4_click = checkButtonClick(last_click, Point(4, -4), Point(7, -3))

        # Passes in the most recent clicked point, current turn, player scores and other information in order
        # to determine whether the player has clicked on a question box. If the player clicks on the question box
        # and enters an answer, score1, score2, and the clicked variable will change respectively.

        score1, score2, c41_clicked, question_clicked = clickedQuestion(c4q1_click, turn, score1, score2, win, c41_clicked, cat4List,
                                                      Point(4, 2), Point(7, 3), 0, question_clicked)
        score1, score2, c42_clicked, question_clicked = clickedQuestion(c4q2_click, turn, score1, score2, win, c42_clicked, cat4List,
                                                      Point(4, 0), Point(7, 1), 1, question_clicked)
        score1, score2, c43_clicked, question_clicked = clickedQuestion(c4q3_click, turn, score1, score2, win, c43_clicked, cat4List,
                                                      Point(4, -2), Point(7, -1), 2, question_clicked)
        score1, score2, c44_clicked, question_clicked = clickedQuestion(c4q4_click, turn, score1, score2, win, c44_clicked, cat4List,
                                                      Point(4, -4), Point(7, -3), 3, question_clicked)

        # Making sure to alternate turns between players. If the previous turn was used by User 1, the next turn is
        # used by User 2, and vice-versa.
        if turn == 1 and question_clicked:
            turn = 0
        elif turn == 0 and question_clicked:
            turn = 1

        scoreboard1.undraw()
        scoreboard2.undraw()
    win.quit()
    return score1, score2


def endGameWindow(score1, score2):
    win = ''
    los = ''

    # Checks who won the game and sets the winner and loser appropriately
    if score1 >= 1000:
        win = u1name
        los = u2name
    if score2 >= 1000:
        win = u2name
        los = u1name

    # Creating the Graphics window that will be displayed when the game has finished
    endWin = GraphWin(win, 400, 400)
    endWin.setCoords(0, 0, 4, 4)
    endWin.setBackground("Orange")

    # Creating the header that will be displayed at the tip of the graphics window
    winning_header = drawText(win + " beats " + los + "!", Point(2, 3.5), "Amatic SC", 18)
    winning_header.setFill("black")
    winning_header.draw(endWin)

    # Creating subheaders for the winner and loser
    winning_subheader = drawText(win + "'s score:", Point(1, 2.5), "Amatic SC", 18)
    winning_subheader.draw(endWin)
    winning_subheader2 = drawText(los + "'s score:", Point(3, 2.5), "Amatic SC", 18)
    winning_subheader2.draw(endWin)

    # Compares the two scores and decides which headers to draw within the end window.
    if score1 > score2:
        score_subheader1 = drawText(score1, Point(1, 2), "Amatic SC", 18)
        score_subheader1.draw(endWin)
        score_subheader2 = drawText(score2, Point(3, 2), "Amatic SC", 18)
        score_subheader2.draw(endWin)
    else:
        score_subheader1 = drawText(score1, Point(3, 2), "Amatic SC", 18)
        score_subheader1.draw(endWin)
        score_subheader2 = drawText(score2, Point(1, 2), "Amatic SC", 18)
        score_subheader2.draw(endWin)

    endWin.getMouse()
    endWin.quit()
    return win, los, score1, score2


def questionWindow(question, score):
    # Initializes and creates the question window
    q_win = GraphWin(question.getCategory(), 400, 400)
    q_win.setCoords(-10, -10, 10, 10)
    q_win.setBackground("Orange")

    # Creating an entry box so that the user can enter their answer to the question
    user_entry = Entry(Point(0, 7), 10)
    header = Text(Point(0, 9), question.getQuestion())
    drawButton(q_win, "Enter", Point(-2, -1), Point(2, 1), "Amatic SC")
    user_entry.draw(q_win)
    header.draw(q_win)

    # When the player clicks enter, the program will then check whether their answer matches
    # with the one in the category file.
    click = q_win.getMouse()
    enter_answer = checkButtonClick(click, Point(-2, -1), Point(2, 1))
    if enter_answer:
        if question.checkAnswer(user_entry.getText()):
            score += question.getValue()
    q_win.close()
    return score


def process_outfile(winner, loser, score1, score2):
    # OFL
    outfile = open("GameHasEnded.txt", "w")
    print(winner + " beats " + loser, file=outfile)
    print("Player 1 Score:", score1, file=outfile)
    print("Player 2 Score:", score2, file=outfile)


if __name__ == "__main__":
    u1name, u2name = setupLoginWindow()
    s1, s2 = startMainWindow()
    win, los, s1, s2 = endGameWindow(s1, s2)
    process_outfile(win, los, s1, s2)
