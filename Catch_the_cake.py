import tkinter as tk
import random
from PIL import Image, ImageTk  

# Creating window
root = tk.Tk()
root.title("Catch the Cake Game")
root.geometry("400x500")

# Canvas with birthday background
canvas = tk.Canvas(root, width=400, height=500, bg="#ffe4e1")  # Light pink
canvas.pack()

# Birthday message
canvas.create_text(200, 40, text="🎉 Happy Birthday! 🎂", font=("Arial", 20, "bold"), fill="#d2691e")

# Balloons
for i in range(5):
    x = 60 + i*60
    canvas.create_oval(x, 70, x+30, 110, fill=random.choice(["red", "yellow", "blue", "green", "purple"]), outline="black")
    canvas.create_line(x+15, 110, x+15, 130, fill="black")

# Player 
girl_img_raw = Image.open("girl.png")  # Use a PNG with transparent background!
girl_img_raw = girl_img_raw.resize((100, 100), Image.Resampling.LANCZOS)
girl_img = ImageTk.PhotoImage(girl_img_raw)

girl_x = 200
girl = canvas.create_image(girl_x, 460, image=girl_img)

# Score
score = 0
score_text = canvas.create_text(50, 20, text="Score: 0", font=("Arial", 16))

# Cakes list
cakes = []
game_over = False

def draw_cake(x, y):
    # Wider and more rectangular cake
    middle = canvas.create_rectangle(x-22, y-8, x+22, y+8, fill="#ffe4b5", outline="#d2691e")
    top = canvas.create_oval(x-22, y-18, x+22, y-2, fill="pink", outline="#d2691e")
    candle = canvas.create_line(x, y-18, x, y-25, fill="blue", width=2)
    flame = canvas.create_oval(x-3, y-28, x+3, y-25, fill="yellow", outline="orange")
    return (middle, top, candle, flame)
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
    win = tk.Toplevel(root)
    win.title("Game Over")
    win.geometry("300x200")
    tk.Label(win, text="Game Over!", font=("Arial", 20, "bold"), fg="red").pack(pady=10)
    tk.Label(win, text=f"Final Score: {final_score}", font=("Arial", 16)).pack(pady=5)
    tk.Label(win, text=msg, font=("Arial", 14), fg="blue").pack(pady=5)
    tk.Button(win, text="Restart", font=("Arial", 12), command=lambda: [win.destroy(), restart_game()]).pack(pady=15)

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
        if abs(middle_pos[0] + 15 - girl_pos[0]) < 40 and middle_pos[3] >= 440:
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
            for item in cake:
                canvas.delete(item)
            cakes.remove(cake)
        # Check if missed (touches ground)
        elif middle_pos[3] > 500:
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

new_cake()
move_cakes()
root.mainloop()
