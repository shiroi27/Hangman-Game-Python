import tkinter as tk
from tkinter import messagebox
import random
import os
import sys

# Game setup
words = [
    "UMBRELLA", "COMPUTER", "TELESCOPE", "SMARTPHONE", "NOTEBOOK",
    "PYTHON", "HANGMAN", "LANTERN", "HEADPHONES", "MICROSCOPE",
    "BACKPACK", "KEYBOARD", "BICYCLE", "EARRINGS", "LADDER"]

hint = {
    "UMBRELLA": "Used when it rains ☔",
    "COMPUTER": "Has a CPU 🖥️",
    "TELESCOPE": "Helps you see stars 🔭",
    "SMARTPHONE": "Used to call and text 📱",
    "NOTEBOOK": "You write your notes in this 📓",
    "PYTHON": "A popular programming language 🐍",
    "HANGMAN": "The game you're playing now 🎯",
    "LANTERN": "Portable light source 🏮",
    "HEADPHONES": "Used to listen to music 🎧",
    "MICROSCOPE": "Used to see tiny things 🔬",
    "BACKPACK": "You carry it on your back 🎒",
    "KEYBOARD": "Used to type on computers ⌨️",
    "BICYCLE": "Pedaled vehicle with two wheels 🚴",
    "EARRINGS": "Worn on ears for fashion 💎",
    "LADDER": "Used to climb up high 🪜"
}

word = random.choice(words)
guessed_word = ["_" for _ in word]
total_chances = 7
score = 0
wrong_guesses = 0

# GUI Setup
root = tk.Tk()
root.title("Hangman")
root.geometry("1000x600+350+50")
root.configure(bg="#FDF6EC")
root.resizable(False, False)

# Header
header = tk.Label(root, text="🎯 HANGMAN 🎯", font=("Courier New", 36, "bold"), bg="#FC5185", fg="white", height=1)
header.pack(fill=tk.X)

# Divider
divider = tk.Frame(root, bg="#364F6B", height=8)
divider.pack(fill=tk.X)

# Word display
word_label = tk.Label(root, text=" ".join(guessed_word), font=("Georgia", 28), bg="#FDF6EC", fg="#364F6B")
word_label.place(x=100, y=120)

# Hint
hint_label = tk.Label(root, text="Hint: " + hint[word], font=("Arial", 16, "italic"), bg="#FDF6EC", fg="#3FC1C9")
hint_label.place(x=100, y=190)

# Input box
input_var = tk.StringVar()
input_entry = tk.Entry(root, textvariable=input_var, font=("Arial", 30), width=6, justify='center', bg="#FCE38A", fg="#364F6B")
input_entry.place(x=100, y=250)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="#FDF6EC", fg="#FC5185")
result_label.place(x=100, y=400)

# Score and chances
status_label = tk.Label(root, text=f"Score: {score}   Chances Left: {total_chances}", font=("Arial", 16), bg="#FDF6EC", fg="#364F6B")
status_label.place(x=100, y=330)

# Canvas for drawing hangman
canvas = tk.Canvas(root, width=300, height=300, bg="#FDF6EC", highlightthickness=0)
canvas.place(x=650, y=130)

def draw_hangman(stage):
    canvas.delete("all")
    # Draw gallows on the right
    canvas.create_line(150, 280, 250, 280, fill="black", width=4)  # base
    canvas.create_line(200, 280, 200, 20, fill="black", width=4)    # pole
    canvas.create_line(200, 20, 100, 20, fill="black", width=4)     # top bar
    canvas.create_line(100, 20, 100, 50, fill="black", width=4)     # rope

    if stage >= 1:
        canvas.create_oval(80, 50, 120, 90, outline="black", width=3)  # head
    if stage >= 2:
        canvas.create_line(100, 90, 100, 160, fill="black", width=3)  # body
    if stage >= 3:
        canvas.create_line(100, 110, 80, 130, fill="black", width=3)  # left arm
    if stage >= 4:
        canvas.create_line(100, 110, 120, 130, fill="black", width=3)  # right arm
    if stage >= 5:
        canvas.create_line(100, 160, 80, 200, fill="black", width=3)  # left leg
    if stage >= 6:
        canvas.create_line(100, 160, 120, 200, fill="black", width=3)  # right leg
    if stage == 7:
        canvas.create_text(100, 230, text="💀", font=("Arial", 36))

def check_letter(event=None):
    global total_chances, score, wrong_guesses
    letter = input_var.get().upper()
    input_var.set("")

    if not letter.isalpha() or len(letter) != 1:
        result_label.config(text="Please enter a single letter.")
        return

    if letter in word:
        for i in range(len(word)):
            if word[i] == letter:
                guessed_word[i] = letter
        word_label.config(text=" ".join(guessed_word))
        result_label.config(text="Correct!", fg="#3FC1C9")
    else:
        total_chances -= 1
        wrong_guesses += 1
        draw_hangman(wrong_guesses)
        result_label.config(text=f"Wrong guess! '{letter}' not in word.", fg="#FC5185")

    status_label.config(text=f"Score: {score}   Chances Left: {total_chances}")

    if "_" not in guessed_word:
        score += 1
        messagebox.showinfo("Victory", "🎉 Congratulations! You guessed the word!")
        reset_game()

    if total_chances == 0:
        word_label.config(text=word)
        draw_hangman(7)
        retry = messagebox.askyesno("Game Over", f"You lost! The word was: {word}\n\nDo you want to play again?")
        if retry:
            root.destroy()
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            root.destroy()

def reset_game():
    global word, guessed_word, total_chances, wrong_guesses
    word = random.choice(words)
    guessed_word = ["_" for _ in word]
    total_chances = 7
    wrong_guesses = 0
    word_label.config(text=" ".join(guessed_word))
    hint_label.config(text="Hint: " + hint[word])
    result_label.config(text="")
    status_label.config(text=f"Score: {score}   Chances Left: {total_chances}")
    draw_hangman(0)

input_entry.bind("<Return>", check_letter)

root.mainloop()