import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame

#colectii pentru pastrarea cartilor folosite
player_hand = []
dealer_hand = []
all_cards = []

#'sablonul' unei carti
class Card:
    def __init__(self, suit, value, image):
        self.suit = suit
        self.value = value
        self.image = image
        
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

#initializarea pachetului cu carti
deck = []

#functie ce da o noua carta
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
    
#scenariu - Game Over
lose_mesage_label = None
orig_img = Image.open(r"C:\Python\lucru_individual_py\images\defeat\you_lose_resize.png").convert("RGBA")

def lose_screen(w, h):
    global lose_mesage_label
    img = orig_img.copy().resize((w, h))
    tk_img = ImageTk.PhotoImage(img)

    if lose_mesage_label is None:
        lose_mesage_label = tk.Label(root, image=tk_img, bg="black")
        lose_mesage_label.place(relx=0.5, rely=0.5, anchor="center")
    else:
        lose_mesage_label.configure(image=tk_img)

    lose_mesage_label.image = tk_img
    
def game_over():
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
    
#Inceputul jocului nou
def start_game(event, root):
    root.unbind(event)
    press_to_start_label.destroy()
    new_game()
    root.after(1500, choice)
    
def new_game():
    #crearea si amesteczre pachetului cu carti
    deck = [Card(suit, value, fr"C:\Python\lucru_individual_py\images\PNG-cards-1.3\{value}_of_{suit}.png") for suit in suits for value in values]
    random.shuffle(deck)
    #curatam
    hit_label.unplace()
    stand_label.unplace()
    player_hand.clear()
    dealer_hand.clear()
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
    
#Jucatorul alege sa faca Hit
def hit_player():
    secrest_card_label.place_forget()
    player_score = 0
    aces = 0
    for value in player_hand:
        if value.isdigit():
            player_score += int(value)
        if value in ['jack','queen','king']:
            player_score += 10
        if value == 'ace':
            aces += 1
            
    for _ in range(aces):
        player_score += 11 if player_score + 11 <=21 else 1
    if player_score == 21:
        win()
    if player_score > 21:
        game_over()

#Jucatorul alege sa faca Stand
def stand():
    pass

#afisam butoane
def choice():
    hit_label.place(x=32, y=207)
    stand_label.place(x=800 - 32 - stand_label.winfo_reqwidth(), y=207)

