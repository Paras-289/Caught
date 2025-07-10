# 🎮 Caught — Catch the Balls Game

Welcome to **Caught**, a fast-paced, fun-filled ball-catching game built with Python’s Tkinter GUI toolkit and Pygame for sound effects. Test your reflexes as colorful balls tumble from the sky—can you catch them all before you run out of lives?

---

## 🚀 Features

- 🌈 Full-screen, vibrant interface
- 🔊 Sound effects for catching and game over events
- 🧠 Difficulty selector: Easy, Medium, and Hard
- 🥇 Score tracking and saving system (last and best scores)
- 🖱️ Intuitive controls using arrow keys
- 🎨 Background images and styled buttons for immersive gameplay

---

## 🛠️ Project Structure

Caught/ 
├── assets/ # Contains images and sounds used in the game 
|        ├── images/ # Backgrounds for main, menu, and gameplay 
|        └── sounds/ # Sound effects (catch & game-over) 
├── game.py # Core gameplay logic (ball falling, catching, scoring) 
├── main.py # Landing screen with navigation buttons 
├── menu.py # Level selection interface (Easy, Medium, Hard) 
├── UI_UTILS.py # (Optional) Shared UI helper functions (if used) 
├── config.json # Stores selected difficulty 
├── scores.txt # High scores for each difficulty 
├── last_score.txt # Stores latest game score 
└── README.md # Project description and setup guide


---

## 💡 How to Play

1. Launch `main.py`.
2. Choose a level from the **Levels** screen.
3. Use **← Left** and **→ Right** arrow keys to move your catcher.
4. Catch falling balls to earn points.
5. Avoid missing balls—you only have 3 lives!
6. Try to beat your best score!

---

## 🧰 Requirements

- Python 3.8+
- Required libraries:
  - `tkinter` (comes built-in with Python)
  - `Pillow`
  - `pygame`

You can install external dependencies using:

```bash
pip install pillow pygame



🎯 Difficulty Levels
Each difficulty controls the ball drop speed and interval:

Level	Ball Speed	Ball Interval	Challenge
Easy	60 ms	    2500 ms	        Chill pace
Medium	45 ms	    1800 ms	        Balanced
Hard	30 ms	    1200 ms	        High adrenaline

Created by: Paras  
Icon and sound assets sourced via free-use licenses.

📬 Feedback

---

Let me know if you want to localize the README for a specific language, include code samples or illustrations, or generate a stylish banner for your project. I’d be happy to spruce it up further! 🪩