import tkinter as tk
import random
from PIL import Image, ImageTk

# Creating window
root = tk.Tk()
root.title("Catch the Cake Game")
root.geometry("400x500")
root.configure(bg="#ffb6c1")  # Light pink for window background

# Canvas with image background
bg_img_raw = Image.open("background.jpeg").resize((400, 500), Image.Resampling.LANCZOS)
bg_img = ImageTk.PhotoImage(bg_img_raw)
canvas = tk.Canvas(root, width=400, height=500, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=bg_img)

# Player
girl_img_raw = Image.open("girl.png").resize((100, 100), Image.Resampling.LANCZOS)
girl_img = ImageTk.PhotoImage(girl_img_raw)
girl_x = 200
girl = canvas.create_image(girl_x, 460, image=girl_img)

# Score
score = 0
score_text = canvas.create_text(350, 10, text="Score: 0", font=("Arial", 16), fill="#F04084")

# Cakes list and image reference
cakes = []
cake_images = []  # Keep references to cake images
game_over = False

def draw_cake(x, y):
    cake_img_raw = Image.open("cake.png").resize((80, 80), Image.Resampling.LANCZOS)
    cake_img = ImageTk.PhotoImage(cake_img_raw)
    cake_images.append(cake_img)  # Prevent garbage collection
    cake_item = canvas.create_image(x, y, image=cake_img)
    return [cake_item]

# Move girl
def move(event):
    global girl_x
    if not game_over:
        x = event.x
        if 30 < x < 370:
            girl_x = x
            canvas.coords(girl, girl_x, 460)
root.bind("<Motion>", move)

def new_cake():
    if not game_over:
        x = random.randint(30, 370)
        cake_items = draw_cake(x, 0)
        cakes.append(cake_items)
        root.after(1500, new_cake)

def show_game_over_window(final_score, msg):
    # Center the window over the main window
    root.update_idletasks()
    main_x = root.winfo_x()
    main_y = root.winfo_y()
    main_w = root.winfo_width()
    main_h = root.winfo_height()
    win_w, win_h = 320, 220
    pos_x = main_x + (main_w // 2) - (win_w // 2)
    pos_y = main_y + (main_h // 2) - (win_h // 2)

    win = tk.Toplevel(root)
    win.title("Game Over")
    win.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    win.resizable(False, False)
    win.configure(bg="#ffe4e1")

    tk.Label(win, text="Game Over!", font=("Arial", 18, "bold"), fg="#F04084", bg="#ffe4e1").pack(pady=10)
    tk.Label(win, text=f"Final Score: {final_score}", font=("Arial", 14, "bold"), fg="#d2691e", bg="#ffe4e1").pack(pady=5)
    tk.Label(win, text=msg, font=("Arial", 12), fg="blue", bg="#ffe4e1").pack(pady=5)
    tk.Button(win, text="Restart", font=("Arial", 12, "bold"), bg="#F04084", fg="white",
              command=lambda: [win.destroy(), restart_game()]).pack(pady=15)

def move_cakes():
    global score, game_over
    if game_over:
        return
    for cake in cakes[:]:
        for item in cake:
            canvas.move(item, 0, 5)
        middle_pos = canvas.coords(cake[0])
        girl_pos = canvas.coords(girl)
        # Check if caught (simple collision)
        if abs(middle_pos[0] - girl_pos[0]) < 40 and middle_pos[1] >= 440:
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
            for item in cake:
                canvas.delete(item)
            cakes.remove(cake)
        # Check if missed (touches ground)
        elif middle_pos[1] > 500:
            for item in cake:
                canvas.delete(item)
            cakes.remove(cake)
            game_over = True
            # Interesting message based on score
            if score == 0:
                msg = "You missed all the cake!😥"
            elif score < 5:
                msg = "You had a small treat!😉"
            elif score < 10:
                msg = "Yum! You enjoyed some cake!😋"
            else:
                msg = "You ate too much cake!🤤"
            show_game_over_window(score, msg)
            return
    root.after(50, move_cakes)

def restart_game():
    global score, cakes, game_over
    for cake in cakes:
        for item in cake:
            canvas.delete(item)
    cakes.clear()
    score = 0
    canvas.itemconfig(score_text, text="Score: 0")
    game_over = False
    new_cake()
    move_cakes()

# --- Start Window with Instructions ---
def show_start_window():
    win_w, win_h = 320, 220
    root.update_idletasks()
    main_x = root.winfo_x()
    main_y = root.winfo_y()
    main_w = root.winfo_width()
    main_h = root.winfo_height()
    pos_x = main_x + (main_w // 2) - (win_w // 2)
    pos_y = main_y + (main_h // 2) - (win_h // 2)

    start_win = tk.Toplevel(root)
    start_win.title("Welcome!")
    start_win.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    start_win.resizable(False, False)
    start_win.configure(bg="#ffe4e1")

    tk.Label(start_win, text="Catch the Cake Game", font=("Arial", 18, "bold"), fg="#F04084", bg="#ffe4e1").pack(pady=10)
    tk.Label(start_win, text="Instructions:", font=("Arial", 14, "bold"), fg="#d2691e", bg="#ffe4e1").pack(pady=5)
    tk.Label(start_win, text="1. Catch the cakes to gain score.", font=("Arial", 12), bg="#ffe4e1").pack()
    tk.Label(start_win, text="2. If you miss a cake, the game will be over.", font=("Arial", 12), bg="#ffe4e1").pack()
    tk.Button(start_win, text="Start Game", font=("Arial", 12, "bold"), bg="#F04084", fg="white",
              command=lambda: [start_win.destroy(), start_game()]).pack(pady=15)

def start_game():
    new_cake()
    move_cakes()

show_start_window()
root.mainloop()
