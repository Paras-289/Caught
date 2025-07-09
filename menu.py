import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import subprocess

# -------------------- Setup --------------------
root = tk.Tk()
root.title("Select Level")
root.resizable(False, False)

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size
window_width = 800
window_height = 400

# Calculate position to center the window
pos_x = (screen_width // 2) - (window_width // 2)
pos_y = (screen_height // 2) - (window_height // 2)

# Apply geometry
root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")

# -------------------- Load Background --------------------
bg_image = Image.open("assets/images/level_bg.jpg")
bg_image = bg_image.resize((800, 400))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=800, height=400, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# -------------------- ttk Style --------------------
style = ttk.Style()
style.theme_use("clam")
style.configure("Level.TButton",
    font=("Times New Roman", 14, "bold"),
    foreground="white",
    background="#2e86de",
    padding=10,
    borderwidth=0
)
style.map("Level.TButton",
    background=[("active", "#4fa3f7")]
)

# -------------------- Save Difficulty and Launch --------------------
def launch_game(difficulty):
    # Save to config.json
    with open("config.json", "w") as f:
        json.dump({"difficulty": difficulty}, f)
    root.destroy()
    subprocess.run(["python", "game.py"])

# -------------------- Back Button --------------------
def go_back():
    root.destroy()
    subprocess.run(["python", "main.py"])

# -------------------- Buttons --------------------
easy_btn = ttk.Button(root, text="Easy", style="Level.TButton", command=lambda: launch_game("easy"))
canvas.create_window(400, 120, window=easy_btn)

medium_btn = ttk.Button(root, text="Medium", style="Level.TButton", command=lambda: launch_game("medium"))
canvas.create_window(400, 180, window=medium_btn)

hard_btn = ttk.Button(root, text="Hard", style="Level.TButton", command=lambda: launch_game("hard"))
canvas.create_window(400, 240, window=hard_btn)

back_btn = ttk.Button(root, text="Back", style="Level.TButton", command=go_back)
canvas.create_window(400, 310, window=back_btn)

# -------------------- Run --------------------
root.mainloop()
