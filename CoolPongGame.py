from tkinter import *
from time import sleep
import random
import datetime

# global variables
end = TRUE
x = 0
y = 0
move = 10
movel = 10
player1_score = 0
player2_score = 0
player1_name = ""
player2_name = ""
score = None
wait = True
Newlabel = None
bgcol = ""
textcol = ""
paddlecol = ""
ballcol = ""
ball = NONE
listboxb = None
listboxt = None
listboxp = None
listboxba = None
entry1 = ""
entry2 = ""
# -------------------------- UI SETUP --------------------------#
window = Tk()
window.title("Cool Pong Game")
window.minsize(width=1300, height=850)
window.configure(background="pink")

# Labels
Welcome_Message = Label(text="WELCOME TO THE GAME")
Welcome_Message.pack()

# Creating Canvas to display pic of snake
canvas = Canvas(width=1280, height=750, bg="pink", highlightthickness=0)
ponggame_Pic = PhotoImage(file="PongGame.png")
display_image = canvas.create_image(670, 325, image=ponggame_Pic)
canvas.pack()


# ---------------------------------------------------------------------#

# --------------------------------------Customization--------------------------------------------#
def listboxb_used(event):
    global bgcol
    # Gets current selection from listbox
    bgcol = listboxb.get(listboxb.curselection())


def listboxp_used(event):
    # Gets current selection from listbox
    global paddlecol
    paddlecol = listboxp.get(listboxp.curselection())


def listboxt_used(event):
    global textcol
    # Gets current selection from listbox
    textcol = (listboxt.get(listboxt.curselection()))


def listboxba_used(event):
    global ballcol
    # Gets current selection from listbox
    ballcol = (listboxba.get(listboxba.curselection()))


def nameselector():
    global player1_name
    global player2_name
    player1_name = (entry1.get())
    player2_name = (entry2.get())
    start_game_screen()


def custom():
    colorpallet = ["black", "blue", "orange", "yellow", "white", "pink"]
    global listboxb
    label1 = Label(text="Choose background colour")
    label1.pack()
    listboxb = Listbox(exportselection=0, height=6)
    for item in colorpallet:
        listboxb.insert(colorpallet.index(item), item)
    listboxb.bind("<<ListboxSelect>>", listboxb_used)
    listboxb.pack()
    global listboxt
    label2 = Label(text="Choose text colour")
    label2.pack()
    listboxt = Listbox(exportselection=0, height=6)
    for item in colorpallet:
        listboxt.insert(colorpallet.index(item), item)
    listboxt.bind("<<ListboxSelect>>", listboxt_used)
    listboxt.pack()
    global listboxp
    label3 = Label(text="Choose paddle colour")
    label3.pack()
    listboxp = Listbox(exportselection=0, height=6)
    for item in colorpallet:
        listboxp.insert(colorpallet.index(item), item)
    listboxp.bind("<<ListboxSelect>>", listboxp_used)
    listboxp.pack()
    global listboxba
    label4 = Label(text="Choose ball colour")
    label4.pack()
    listboxba = Listbox(exportselection=0, height=6)
    for item in colorpallet:
        listboxba.insert(colorpallet.index(item), item)
    listboxba.bind("<<ListboxSelect>>", listboxba_used)
    listboxba.pack()

    global entry1
    entry1 = Entry(width=30)
    # Add some text to begin with
    entry1.insert(END, string="Name of player on the left")
    entry1.pack()

    global entry2
    entry2 = Entry(width=30)
    # Add some text to begin with
    entry2.insert(END, string="Name of player on the right")
    entry2.pack()


# ------------------------------------collision test----------------------------------------------#
def collision_detector(ball, paddle, x):
    pos = canvas.coords(ball)
    pos2 = canvas.coords(paddle)
    if pos[0] < pos2[2] and pos[2] > pos2[0] and pos[1] < pos2[3] and pos[3] > pos2[1]:
        if x < 0:
            x -= 0.1
        else:
            x += 0.1
        x = -x

    return x


# -------------------------------------------------------------------------------------------------#

# --------------------------------------ScoreBoard---------------------------------------------------#
def scoreboard():
    global score
    score = canvas.create_text(635, 11,
                               text=f"Score of {player1_name} = {player1_score} : Score of {player2_name} ="
                                    f" {player2_score}",
                               fill=textcol, font=("Comic Sans MS", 20, "bold"))
    canvas.pack()


def update_score(scores):
    canvas.delete(score)
    return scores + 1


# ----------------------------------------------------------------------------------------------------------------#


# -----------------------------------Ball----------------------------------------#
def ball_maker():
    ball = canvas.create_oval(110, 10, 140, 40, fill=ballcol)
    canvas.pack()
    return ball


def moving_ball(ball, paddlel, paddler):
    global end
    global player2_score
    global player1_score
    global player2_name
    global player1_name
    global x, y
    canvas.moveto(ball, 650, 420)
    waiting = 0.002
    dir = [-1, 1]
    rand1 = random.randint(0, 1)
    rand2 = random.randint(0, 1)
    x = 3 * dir[rand1]
    y = 3 * dir[rand2]
    while player2_score < 10 and player1_score < 10 and end:
        pos = canvas.coords(ball)
        x = collision_detector(ball, paddlel, x)
        x = collision_detector(ball, paddler, x)
        if pos[3] > 750 or pos[1] < 0:
            if y < 0:
                y -= 0.1
            else:
                y += 0.1
            y = -y
            waiting /= 10
        if pos[2] > 1260:
            player1_score = update_score(player1_score)
            sleep(1)
            action()

        if pos[0] < 15:
            player2_score = update_score(player2_score)
            sleep(1)
            action()

        canvas.move(ball, x, y)
        sleep(waiting)
        window.update()
    if player2_score == 10 and end:
        end = False
        save(player2_score, player1_score, player2_name, player1_name)
        leaderboard()
    elif player1_score == 10 and end:
        end = False
        save(player1_score, player2_score, player1_name, player2_name)
        leaderboard()
    else:
        pass


# --------------------------------------------------------------------------------------------#

# -----------------------------------paddles-----------------------------------------------------#
def paddles(coord):
    paddle = canvas.create_rectangle(coord, fill=paddlecol)
    return paddle


def moveUp(event):
    pos = canvas.coords(right_paddle)
    if pos[1] > 10:
        canvas.move(right_paddle, 0, -move)


def moveUpl(event):
    pos = canvas.coords(left_paddle)

    if pos[1] > 10:
        canvas.move(left_paddle, 0, -movel)


def moveDown(event):
    pos = canvas.coords(right_paddle)
    if pos[3] < 740:
        canvas.move(right_paddle, 0, move)


def moveDownl(event):
    pos = canvas.coords(left_paddle)
    if pos[3] < 740:
        canvas.move(left_paddle, 0, movel)


# -----------------------------------------------------------------------------------------------#
# -----------------------------------------pausing function------------------------------------------------------#
def keypress(event):
    global wait
    if event.keysym == 'space':
        wait = False
        canvas.delete(Newlabel)


def keepPaused():
    global wait
    global Newlabel
    wait = True
    canvas.bind_all('<KeyPress-space>', keypress)
    Newlabel = canvas.create_text(635, 320,
                                  text="Click SPACE BAR to resume game or 'b' to access boss key",
                                  fill=textcol, font=("Comic Sans MS", 30, "bold"))
    canvas.pack()
    while wait:
        window.update()


# --------------------------------------------------------------------------------------------------#

# ---------------------------------------boss key----------------------------------------------------#

def keypressb(event):
    global wait
    if event.keysym == 'space':
        wait = False
        canvas.delete("all")
        start_game_screen()


def keepPausedb():
    global wait
    global Newlabel
    wait = True
    canvas.bind_all('<KeyPress-space>', keypressb)
    while wait:
        window.update()


def bossalert(event):
    canvas.delete("all")
    boss_screen = PhotoImage(file="Boss_key.png")
    canvas.create_image(670, 325, image=boss_screen)
    canvas.pack()
    keepPausedb()


# -----------------------------------------------------------------------------------------------------#
# -----------------------------cheat code----------------------------------------------------------------#

def slowball(event):
    global x, y
    x = x // 2
    y = y // 2


def fastmove(event):
    global move
    move = 15


def fastmovel(event):
    global movel
    movel = 15


# --------------------------------------------------------------------------------------------------------#
# --------------------------------------quit------------------------------------------------------------#
def quickend(event):
    global end
    end = False
    leaderboard()


# --------------------------------------------------------------------------------------------------------#

# movement
left_paddle = ""
right_paddle = ""
canvas.bind_all("<KeyPress-w>", moveUpl)
canvas.bind_all("<KeyPress-s>", moveDownl)
canvas.bind_all("<KeyPress-Up>", moveUp)
canvas.bind_all("<KeyPress-Down>", moveDown)
canvas.bind_all("<KeyPress-b>", bossalert)
canvas.bind_all("<Escape>", quickend)
canvas.bind_all("<KeyPress-l>", fastmovel)
canvas.bind_all("<KeyPress-r>", fastmove)
canvas.bind_all("<KeyPress-c>", slowball)


def start_game_screen():
    canvas.config(width=1280, height=750)
    button.config(text="click to pause", command=keepPaused)
    canvas.config(bg=bgcol)
    window.config(background=bgcol)
    left = (0, 275, 20, 375)
    right = (1255, 275, 1275, 375)
    global left_paddle
    global right_paddle
    global ball
    left_paddle = paddles(left)
    right_paddle = paddles(right)
    ball = ball_maker()
    action()


def action():
    # update(0)
    scoreboard()
    moving_ball(ball, left_paddle, right_paddle)


def customizer():
    canvas.delete("all")
    canvas.config(height=0, width=0)
    custom()
    button.config(text="Submit", command=nameselector)


# calls action() when pressed
button = Button(text="Click Me To Start game", command=customizer)
button.pack()


# ----------------------------------------saving and leaderboard-------------------------------------#
def save(win, lose, winner, loser):
    current_time = datetime.datetime.now()
    time = str(
        current_time.year) + "-" + str(current_time.month) + "-" + str(
        current_time.day) + " " + str(current_time.hour) + ":" + str(current_time.minute)
    f = open("scoresaver.txt", "a")
    f.write(f"\n{win - lose} : {win}-{lose} by {winner} vs {loser} played at:{current_time}")
    f.close()


def leaderboard():
    results = []
    with open('scoresaver.txt') as my_file:
        for line in my_file:
            results.append(line)
    results.sort(reverse=True)
    canvas.delete("all")
    canvas.create_text(635, 20,
                       text="🏆 Top 3 Wins: 🏆",
                       fill=textcol, font=("Comic Sans MS", 30, "bold"))
    canvas.pack()
    canvas.create_text(635, 90,
                       text=(results[0])[3:],
                       fill=textcol, font=("Comic Sans MS", 30, "bold"))
    canvas.pack()
    canvas.create_text(635, 135,
                       text=(results[1])[3:],
                       fill=textcol, font=("Comic Sans MS", 30, "bold"))
    canvas.pack()
    canvas.create_text(635, 160,
                       text=(results[2])[3:],
                       fill=textcol, font=("Comic Sans MS", 30, "bold"))
    canvas.pack()


# ------------------------------------------------------------------------------------------------------------#

window.mainloop()
