import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess

# -------------------- Window Setup --------------------
root = tk.Tk()
root.title("Catch the Balls")
root.attributes("-fullscreen", True)  # Fullscreen mode
root.bind("<Escape>", lambda e: root.destroy())  # Exit with Esc

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# -------------------- Load Background Image --------------------
bg_image = Image.open("assets/images/landing_bg.jpg")
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


# -------------------- Font and Style Setup --------------------
try:
    font_family = "Times New Roman"
except:
    font_family = "Times New Roman"

style = ttk.Style()
style.theme_use("clam")
style.configure("Neon.TButton",
    font=(font_family, 14, "bold"),
    foreground="white",
    background="#5C2D91",
    padding=10,
    borderwidth=0
)
style.map("Neon.TButton",
    background=[("active", "#7E57C2"), ("hover", "#7E57C2")],
    foreground=[("disabled", "#888")]
)

# -------------------- Placeholder Functions --------------------
def start_game():
    try:
        print("Launching game...")
        subprocess.run(["python", "game.py"], check=True)
    except Exception as e:
        print("Failed to launch game:", e)


def open_levels():
    try:

        subprocess.run(["python", "menu.py"], check=True)
    except Exception as e:
        print("Failed to open level selection:", e)

def last_score():
    try:
        with open("last_score.txt", "r") as f:
            last = f.read().strip()
            if not last:
                last = "0"
    except FileNotFoundError:
        last = "0"

    # Create popup
    popup = tk.Toplevel(root)
    popup.title("Last Score")
    popup.configure(bg="#5C2D91")
    popup.resizable(False, False)

    # Set size and center it
    popup_width = 250
    popup_height = 150
    root.update_idletasks()
    x = root.winfo_x()
    y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    pos_x = x + (root_width // 2) - (popup_width // 2)
    pos_y = y + (root_height // 2) - (popup_height // 2)
    popup.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")

    # Content
    tk.Label(popup, text="🕹️ Last Score", font=("Helvetica", 14, "bold"), fg="white", bg="#5C2D91").pack(pady=10)
    tk.Label(popup, text=f"{last}", font=("Helvetica", 24), fg="white", bg="#5C2D91").pack()
    ttk.Button(popup, text="Close", command=popup.destroy, style="Neon.TButton").pack(pady=10)

def show_best_scores():
    scores = {"easy": "0", "medium": "0", "hard": "0"}
    try:
        with open("scores.txt", "r") as f:
            for line in f:
                if ":" in line:
                    level, value = line.strip().split(":")
                    scores[level.strip()] = value.strip()
    except FileNotFoundError:
        pass

    # Create popup window
    popup = tk.Toplevel(root)
    popup.title("Best Scores")
    popup.configure(bg="#5C2D91")
    popup.resizable(False, False)

    # Set size
    popup_width = 300
    popup_height = 200

    # Get main window position
    root.update_idletasks()
    x = root.winfo_x()
    y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # Calculate center position
    pos_x = x + (root_width // 2) - (popup_width // 2)
    pos_y = y + (root_height // 2) - (popup_height // 2)

    popup.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")

    # Content
    tk.Label(popup, text="🏆 Best Scores by Difficulty", font=("Helvetica", 14, "bold"), fg="white", bg="#5C2D91").pack(pady=10)

    for level in ["easy", "medium", "hard"]:
        tk.Label(popup, text=f"{level.capitalize()}: {scores[level]}", font=("Helvetica", 12), fg="white", bg="#5C2D91").pack()

    ttk.Button(popup, text="Close", command=popup.destroy, style="Neon.TButton").pack(pady=10)


def exit_game():
    root.destroy()

# -------------------- Create & Place Buttons --------------------
btn_new = ttk.Button(root, text="Best Score", command=show_best_scores, style="Neon.TButton")
canvas.create_window(screen_width * 0.25, screen_height * 0.4, window=btn_new)


btn_levels = ttk.Button(root, text="Levels", command=open_levels,style="Neon.TButton")
canvas.create_window(screen_width * 0.25, screen_height * 0.65, window=btn_levels)

btn_last = ttk.Button(root, text="Last Score", command=last_score, style="Neon.TButton")
canvas.create_window(screen_width * 0.75, screen_height * 0.4, window=btn_last)

btn_best = ttk.Button(root, text="EXIT", command=exit_game, style="Neon.TButton")
canvas.create_window(screen_width * 0.75, screen_height * 0.65, window=btn_best)


btn_exit = ttk.Button(root, text="New Game", command=start_game, style="Neon.TButton")
canvas.create_window(screen_width * 0.5, screen_height * 0.52, window=btn_exit)

# -------------------- Start Application --------------------
root.mainloop()