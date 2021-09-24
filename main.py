from tkinter import *
import pandas
import random

# Todo: Read csv and convert to list
try:
    french_english_data = pandas.read_csv("data/words_to_learn.csv").to_dict(orient='records')
    if len(french_english_data) == 0:
        french_english_data = pandas.read_csv("data/french_words.csv").to_dict(orient='records')
except FileNotFoundError:
    french_english_data = pandas.read_csv("data/french_words.csv").to_dict(orient='records')

current_card = {}


# ***************************************** SAVE DATA ****************************************************
def save_data():
    french_english_data.remove(current_card)
    words_to_learn_data = pandas.DataFrame(french_english_data)
    words_to_learn_data.to_csv("data/words_to_learn.csv", index=False)


# ***************************************** FLIP FLASH CARDS ****************************************************
def flip_flash_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# ***************************************** CREATE NEW FLASH CARDS ****************************************************
def generate_flash_cards():
    global current_card, flip_timer, french_english_data
    window.after_cancel(flip_timer)
    # Check if data in the words to learn is finished, then replenish it
    if len(french_english_data) == 0:
        french_english_data = pandas.read_csv("data/french_words.csv").to_dict(orient='records')
    current_card = random.choice(french_english_data)
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    flip_timer = window.after(3000, func=flip_flash_card)


# ***************************************** UI SETUP *******************************************************
# TODO: UI SETUP
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=0, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_flash_card)

canvas = Canvas(width=800, height=600, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 300, image=front_img)

# Canvas Text
language_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 300, text="", font=("Ariel", 48, "bold"))
canvas.grid(column=0, row=0, columnspan=2, padx=0, pady=0)

# Buttons
cancel_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=cancel_img, highlightthickness=0, command=generate_flash_cards)
wrong_btn.grid(column=0, row=1)

correct_img = PhotoImage(file="images/right.png")
right_btn = Button(image=correct_img, highlightthickness=0, command=lambda: [generate_flash_cards(), save_data()])
right_btn.grid(column=1, row=1)

generate_flash_cards()

window.mainloop()
