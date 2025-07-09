from itertools import cycle
from tkinter import *
from tkinter.messagebox import showinfo
from random import randrange
from tkinter import font
import pygame
from PIL import Image, ImageTk
import json
import subprocess
import os
import random
# -------------------- Load Difficulty --------------------
with open("config.json", "r") as f:
    config = json.load(f)

difficulty = config.get("difficulty", "medium")

# -------------------- Settings --------------------

if difficulty == "easy":
    ball_speed = 60
    ball_interval = 2500
elif difficulty == "medium":
    ball_speed = 45
    ball_interval = 1800
elif difficulty == "hard":
    ball_speed = 30
    ball_interval = 1200
else:
    ball_speed = 50
    ball_interval = 2000

ball_score = 10
difficulty_factor = 0.95

ball_width = 45
ball_height = 45

catcher_width = 100
catcher_height = 20

# -------------------- Initialize --------------------
pygame.init()
root = Tk()
root.title("Catch the Balls")
root.attributes("-fullscreen", True)  # Make the window fullscreen
root.bind("<Escape>", lambda e: root.destroy())  # Allow exit with Esc key
root['bg'] = 'sky blue'


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

canvas_width = screen_width
canvas_height = screen_height

c = Canvas(root, width=canvas_width, height=canvas_height)
c.pack()

# -------------------- Main Menu --------------------
def main_menu():
    c.delete("all")

    # Title
    c.create_text(canvas_width / 2, canvas_height * 0.30,
                  text="🎮 Caught!",
                  font=("Helvetica", int(canvas_height * 0.09), "bold"),
                  fill="cyan")

    # Subtitle
    c.create_text(canvas_width / 2, canvas_height * 0.4,
                  text="Catch the falling balls. You have 3 lives!",
                  font=("Times New Roman", int(canvas_height * 0.035)),
                  fill="black")

    # Buttons
    button_font_size = int(19)
    start_btn = Button(root, text="Start Game",
                       font=("Times New Roman", button_font_size),
                       command=start_game)

    exit_btn = Button(root, text="Exit",
                      font=("Times New Roman", button_font_size),
                      command=exit_game)

    c.create_window(canvas_width / 2.75, canvas_height * 0.50, window=start_btn)
    c.create_window(canvas_width / 1.65, canvas_height * 0.50, window=exit_btn)

# -------------------- Start Game --------------------
def start_game():
    global score, lives, best_score, balls, game_running, catcher, score_text, best_score_text, lives_text

    c.delete("all")
    score = 0
    lives = 3
    balls = []
    game_running = True

    # Load best score
    try:
        with open("scores.txt", "r") as f:
            best_score = int(f.read())
    except:
        best_score = 0

    # Background
    bg_img = Image.open("assets/images/game_bg.jpg")
    bg_img = bg_img.resize((canvas_width, canvas_height))
    bg_photo = ImageTk.PhotoImage(bg_img)
    c.bg_photo = bg_photo  # prevent garbage collection
    c.create_image(0, 0, image=bg_photo, anchor="nw")

    # c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
    # c.create_rectangle(-5, canvas_height-100, canvas_width+5, canvas_height+5, fill="sea green", width=0)

    # Catcher
    catcher_startx = canvas_width / 2 - catcher_width / 2
    catcher_starty = canvas_height - catcher_height - 40

    catcher = c.create_rectangle(catcher_startx, catcher_starty,
                             catcher_startx + catcher_width, catcher_starty + catcher_height,
                             fill="#00f0ff", outline="#a0faff", width=4)


    # Score & Lives
    score_text = c.create_text(canvas_width - 100, 30, anchor="e",
                               font=("Times New Roman", 25, "bold"), fill="white",
                               text=f"Score: {score}")

    best_score_text = c.create_text(canvas_width - 100, 60, anchor="e",
                                    font=("Times New Roman", 20), fill="white",
                                    text=f"Best: {best_score}")

    lives_text = c.create_text(100, 30, anchor="w",
                               font=("Times New Roman", 25, "bold"), fill="white",
                               text=f"Lives: {lives}")

    # Bind keys
    root.bind("<Left>", move_left)
    root.bind("<Right>", move_right)

    # Start game loop
    root.after(1000, create_ball)
    
    c.create_text(canvas_width/2, 40, text=f"Difficulty: {difficulty.capitalize()}",
              font=("Times New Roman", 40, "bold"), fill="white")

#---------------------Exit_Game---------------------
def exit_game():    
    try:
        print("Leaving game...")
        root.destroy()
        subprocess.run(["python", "main.py"], check=True)
    except Exception as e:
        print("Failed to Main Menu:", e)

# -------------------- Movement --------------------
def move_left(event):
    if not game_running: return
    x1, y1, x2, y2 = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    if not game_running: return
    x1, y1, x2, y2 = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

# -------------------- Game Logic --------------------
color_cycle = cycle(["light blue", "light green", "pink", "yellow", "cyan", "brown"])
game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

catch_sound = pygame.mixer.Sound("assets/sounds/coin.mp3")
game_over_sound = pygame.mixer.Sound("assets/sounds/game-over.mp3")

balls = []
score = 0
lives = 3
best_score = 0
game_running = False

def create_ball():
    if not game_running: return
    x = randrange(10, canvas_width - ball_width)
    color = next(color_cycle)
    ball = c.create_oval(x, 0, x + ball_width, ball_height, fill=color, width=0)
    balls.append(ball)
    move_ball(ball)
    root.after(ball_interval, create_ball)

def move_ball(ball):
    def fall():
        if not game_running: return
        if c.coords(ball):
            c.move(ball, 0, 5)
            if check_catch(ball):
                c.delete(ball)
                balls.remove(ball)
                pygame.mixer.Sound.play(catch_sound)
                update_score()
            elif c.coords(ball)[3] < canvas_height:
                root.after(ball_speed, fall)
            else:
                c.delete(ball)
                balls.remove(ball)
                lose_life()
    fall()

def check_catch(ball):
    ball_coords = c.coords(ball)
    catcher_coords = c.coords(catcher)

    ball_x1, ball_y1, ball_x2, ball_y2 = ball_coords
    catch_x1, catch_y1, catch_x2, catch_y2 = catcher_coords

    return (ball_y2 >= catch_y1 and ball_y2 <= catch_y2 and
            ball_x2 >= catch_x1 and ball_x1 <= catch_x2)

def update_score():
    global score, best_score
    score += ball_score
    c.itemconfig(score_text, text=f"Score: {score}")
    if score > best_score:
        best_score = score
        c.itemconfig(best_score_text, text=f"Best: {best_score}")

def lose_life():
    global lives, game_running
    lives -= 1
    c.itemconfig(lives_text, text=f"Lives: {lives}")
    if lives == 0:
        game_running = False
        pygame.mixer.Sound.play(game_over_sound)
        
#----------------------Last Score----------------------        
        try:
    # Initialize scores dictionary
            scores = {}

    # Load existing scores from file
            if os.path.exists("scores.txt"):
                with open("scores.txt", "r") as f:
                    for line in f:
                        if ":" in line:
                            level, value = line.strip().split(":")
                            scores[level.strip()] = int(value.strip())

    # Ensure all difficulties are present
            for level in ["easy", "medium", "hard"]:
                if level not in scores:
                    scores[level] = 0

    # Update only the current difficulty if the new score is higher
            if score > scores[difficulty]:
                scores[difficulty] = score

    # Save all scores back to the file
            with open("scores.txt", "w") as f:
                for level in ["easy", "medium", "hard"]:
                    f.write(f"{level}: {scores[level]}\n")

        except Exception as e:
            print("Could not save best score:", e)
        showinfo("Game Over", f"Game Over!\nYour Score: {score}")

        main_menu()


# -------------------- Launch Menu --------------------
main_menu()
root.mainloop()