import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame

pygame.mixer.init()
pygame.mixer.music.load(r"sounds\background.mp3")

cardFlip = pygame.mixer.Sound(r"sounds\flipcard.mp3")

class Card:
    def __init__(self, suit, value, image):
        self.suit = suit
        self.value = value
        self.image = image
        
    def __str__(self):
        return f"{self.value} of {self.suit}"

suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

deck = []
    
player_hand = []
dealer_hand = []
all_cards = []

root = tk.Tk()
root.title('Black Jack')
root.geometry('800x600')
pygame.mixer.music.play(loops = -1)

#scenariu - Egalitate
push_img = Image.open(r"images\victory\push_resize.png")
push_img = push_img.resize((234, 100))
push_img = ImageTk.PhotoImage(push_img)
push_label = tk.Label(root, image = push_img)
push_label.image = push_img

def give_new_card(card_nr):
    new_card = deck.pop()
    with Image.open(new_card.image) as img:
        img = img.resize((80, 116))  
        card_image = ImageTk.PhotoImage(img.copy())
    new_card_label = tk.Label(root, image=card_image)
    new_card_label.image = card_image
    if card_nr < 0:
        new_card_label.place(x=663+card_nr*25, y=43)
        dealer_hand.append(new_card.value)
    else:
        new_card_label.place(x=71+card_nr*25, y=371)
        player_hand.append(new_card.value)
    cardFlip.play()
    all_cards.append(new_card_label)
    
#Game Over - script
lose_mesage_label = None
orig_img = Image.open(r"images\defeat\you_lose_resize.png").convert("RGBA")
lose_hit = pygame.mixer.Sound(r"sounds\lose_hit.mp3")

def lose_screen(w, h):
    global lose_mesage_label
    img = orig_img.copy().resize((w, h))
    tk_img = ImageTk.PhotoImage(img)

    if lose_mesage_label is None:
        lose_mesage_label = tk.Label(root, image=tk_img, bg="black")
        lose_mesage_label.place(relx=0.5, rely=0.5, anchor="center")
    else:
        lose_mesage_label.configure(image=tk_img)
        lose_mesage_label.place(relx=0.5, rely=0.5, anchor="center")

    lose_mesage_label.image = tk_img
    
def game_over():
    hit_label.unbind("<Button-1>")
    stand_label.unbind("<Button-1>")
    secrest_card_label.place_forget()
    root.after(1000, lose_screen, 800, 130)
    root.after(1033, lose_screen, 733, 120)
    root.after(1066, lose_screen, 667, 110)
    root.after(1099, lose_screen, 600, 100)
    root.after(1132, lose_screen, 533, 90)
    root.after(1165, lose_screen, 467, 80)
    root.after(1198, lose_screen, 400, 70)
    root.after(1231, lose_screen, 333, 60)
    root.after(1264, lose_screen, 267, 50)
    root.after(1297, lose_screen, 200, 40)
    root.after(1330, lose_screen, 267, 50)
    root.after(700, lambda: lose_hit.play())
   
#Victory - script
victory_mesage_label = None
victory_img = Image.open(r"images\victory\you_win_resized.png").convert("RGBA")
#victory_hit = pygame.mixer.Sound(r"C:\Python\lucru_individual_py\sounds\win_sound.mp3")

def victory_screen(w, h):
    global victory_mesage_label
    img = victory_img.copy().resize((w, h))
    tk_img = ImageTk.PhotoImage(img)

    if victory_mesage_label is None:
        victory_mesage_label = tk.Label(root, image=tk_img, bg="black")
        victory_mesage_label.place(relx=0.5, rely=0.5, anchor="center")
    else:
        victory_mesage_label.configure(image=tk_img)
        victory_mesage_label.place(relx=0.5, rely=0.5, anchor="center")

    victory_mesage_label.image = tk_img

def victory():
    hit_label.unbind("<Button-1>")
    stand_label.unbind("<Button-1>")
    secrest_card_label.place_forget()
    root.after(1000, victory_screen, 200, 108)
    root.after(1033, victory_screen, 267, 145)
    root.after(1066, victory_screen, 333, 180)
    root.after(1099, victory_screen, 467, 253)
    root.after(1132, victory_screen, 400, 217)
#     root.after(1165, victory_screen, 533, 288)
#     root.after(1198, victory_screen, 600, 325)
#     root.after(1231, victory_screen, 667, 361)
#     root.after(1264, victory_screen, 733, 397)
#     root.after(1290, victory_screen, 800, 433)
#     root.after(1330, victory_screen, 733, 397)
#     root.after(700, lambda: victory_hit.play())
    root.after(500, lambda: lose_hit.play())
    
def start_game(event=None):
    root.unbind("<Button-1>")
    press_to_start_label.destroy()
    new_game()
    root.after(1500, choice)
    
def new_game():
    #crearea si amesteczre pachetului cu carti
    global deck
    deck = [Card(suit, value, fr"images\PNG-cards-1.3\{value}_of_{suit}.png") for suit in suits for value in values]
    random.shuffle(deck)
    #curatam
    global victory_mesage_label, lose_mesage_label
    if victory_mesage_label is not None:
        victory_mesage_label.place_forget()
        victory_mesage_label = None
    if lose_mesage_label is not None:
        lose_mesage_label.place_forget()
        lose_mesage_label = None
    push_label.place_forget()
    try_again_label.place_forget()
    quit_label.place_forget()
    hit_label.place_forget()
    stand_label.place_forget()
    player_hand.clear()
    dealer_hand.clear()
    player_score = calculate_score(player_hand)
    for card in all_cards:
        card.destroy()
    all_cards.clear()
    #dam noi carti
    root.after(200, give_new_card, 1)
    root.after(500, give_new_card, 2)
    root.after(800, give_new_card, -1)
    #ascundem una din carti la inceput
    root.after(1101, lambda: (secrest_card_label.place(x=613, y=43),
                              secrest_card_label.lift()))
    root.after(1100, give_new_card, -2)
    
def calculate_score(hand):
    score = 0
    aces = 0
    for value in hand:
        if value.isdigit():
            score += int(value)
        elif value in {"jack", "queen", "king"}:
            score += 10
        else:
            aces += 1
            
    #calcularea mai multor asuri trebuie corectata pentru cazurile ex. A A K
    #se poate ceva cu score += 11*aces
    for _ in range(aces):
        score += 11 if score + 11 <= 21 else 1
    return score
    
def hit_player(event=None):
    give_new_card(len(player_hand)+1)
    player_score = calculate_score(player_hand)
    if player_score > 21:
        game_over()
        root.after(2500, proceed)

def stand(event=None):
    secrest_card_label.place_forget()
    hit_label.unbind("<Button-1>")
    stand_label.unbind("<Button-1>")
    player_score = calculate_score(player_hand)
    if player_score == 21:
        victory()
        root.after(2500, proceed)
        return
    while True:
        dealer_score = calculate_score(dealer_hand)
        if dealer_score >= 17: break
        give_new_card(-len(dealer_hand)-1)
    
    if dealer_score == player_score:
        push_label.place(relx=0.5, rely=0.5, anchor="center")
        lose_hit.play()
    elif dealer_score > 21 or player_score > dealer_score:
        victory()
    else:
        game_over()
    root.after(2500, proceed)

hit_label = tk.Label(root, text = 'Hit', font=("ocr a extended", 30), fg="white", bg="black", cursor="hand2")
stand_label = tk.Label(root, text = 'Stand', font=("ocr a extended", 30), fg="white", bg="black", cursor="hand2")
def choice():
    hit_label.place(x=32, y=207)
    stand_label.place(x=800 - 32 - stand_label.winfo_reqwidth(), y=207)
    
    hit_label.bind('<Button-1>', hit_player)
    stand_label.bind('<Button-1>', stand)

try_again_label = tk.Label(root, text = 'Try again?', font=("ocr a extended", 30), fg="white", bg="black", cursor="hand2")
quit_label = tk.Label(root, text = 'Quit', font=("ocr a extended", 30), fg="white", bg="black", cursor="hand2")
def proceed():
    try_again_label.place(relx=0.5, y=400, anchor="center")
    try_again_label.lift()
    try_again_label.bind('<Button-1>', lambda e: start_game())
    quit_label.place(relx=0.5, y=450, anchor="center")
    quit_label.lift()
    quit_label.bind('<Button-1>', lambda event:root.destroy())
    
    
    

#ascundem una din carti
card_back_img = Image.open(r"images\card_back\card_back_black.png")
card_back_img = card_back_img.resize((80, 116))
card_back_img = ImageTk.PhotoImage(card_back_img)
secrest_card_label = tk.Label(root, image = card_back_img)

#root.bind("<Button-1>", on_click)

#fundal
with Image.open(r"images\fundal\BG_Table.png") as img:
    img = img.resize((800, 600))  
    bg_image = ImageTk.PhotoImage(img.copy())

font = tk.Label(root, image=bg_image)
font.image = bg_image
font.pack(fill = 'x')
font.lower()

press_to_start_label = tk.Label(root, text = 'PRESS to Start', font=("ocr a extended", 24), fg="white", bg="black")
press_to_start_label.place(relx=0.5, y=515, anchor="n")

root.bind("<Button-1>", start_game)
hit_label.bind("<Button-1>", hit_player)
stand_label.bind("<Button-1>", stand)

root.mainloop()
pygame.mixer.music.stop()