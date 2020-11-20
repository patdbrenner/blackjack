"Blackjack"
import random

suits = ("Hearts", "Diamonds", "Clubs", "Spades")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}


class Card:
    "Playing card"

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    "Deck of cards"

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))
                self.deck.append(Card(rank, suit))
                self.deck.append(Card(rank, suit))
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        "Shuffle deck"
        print("Dealer is shuffling...")
        random.shuffle(self.deck)
        line_break()

    def deal(self):
        "Deal one card"
        return self.deck.pop()


class Chips:
    "Gambling Chips"

    def __init__(self, bank=100):
        self.bank = bank
        self.bet = 0

    def win_bet(self):
        "Win chips"
        self.bank += self.bet

    def lose_bet(self):
        "Lose Chips"
        self.bank -= self.bet


class Hand:
    "Hand of cards"

    def __init__(self):
        self.value = 0
        self.aces = 0
        self.cards = []

    def check(self):
        "Check and display hand"
        self.ace_adjust()
        print("Your hand:")
        for card in self.cards:
            print(card)
        print(self.value)
        line_break()

    def check_dealer_some(self):
        "Check and display first card in hand"
        self.ace_adjust()
        print("Dealer shows: ")
        print(self.cards[0])
        print(self.cards[0].value)
        line_break()

    def check_dealer(self):
        "Check and display dealer hand"
        self.ace_adjust()
        print("Dealer's hand:")
        for card in self.cards:
            print(card)
        print(self.value)
        line_break()

    def add_card(self, card):
        "Add card to hand and check if an Ace"
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == "Ace":
            self.aces += 1

    def ace_adjust(self):
        "Allow Ace to be 11 or 1"
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


def bet(chips):
    "Place a bet"
    while True:
        print(f"Current chip total: {chips.bank}")
        try:
            chips.bet = int(input("Bet: "))
        except:
            print("Must bet an integer.")
        else:
            if chips.bet > chips.bank:
                print(
                    "Don't know what kinda place ya think we runnin' here, we don't take credit."
                )
            else:
                break


def begin_turn(hand, deck):
    "Add cards to hand at beginning of turn"
    hand.add_card(deck.deal())
    hand.add_card(deck.deal())


def hit(hand, deck):
    "Add one card and adjust for ace"
    hand.add_card(deck.deal())
    hand.ace_adjust()


def hit_or_stand(hand, deck):
    "Ask player to hit or stand"
    global GAME_ON
    if hand.value == 21:
        print("Blackjack!")
        line_break()
        GAME_ON = False
    else:
        while True:
            try:
                choice = int(input("Enter 1 to Hit\nEnter 2 to Stand\n"))
            except:
                print("That isn't one of your choices.")
            else:
                if choice == 1:
                    hit(hand, deck)
                    hand.check()
                    if hand.value > 21:
                        break
                elif choice == 2:
                    print("You stand. Dealer's turn.")
                    GAME_ON = False
                    break
                else:
                    print("That isn't one of your choices.")
                    continue


def player_busts(chips):
    print("Ya bust! Dealer wins this round.")
    chips.lose_bet()


def player_wins(chips):
    print("Ya win this round.")
    chips.win_bet()


def dealer_busts(chips):
    print("Dealer busts! Ya win this round!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins this round.")
    chips.lose_bet()


def push():
    print("The hands are tied... Push")

def check_bank(chips):
    "Check if player ran out of chips"
    if chips.bank < 1:
        print("Sorry Pal, looks like you're out of cash.")
        exit()


def line_break():
    "Clean it up"
    print("~~~~~~~~~~~~~~~~~~~")

player_chips = Chips()

while True:

    new_deck = Deck()
    new_deck.shuffle()

    player_hand = Hand()
    begin_turn(player_hand, new_deck)

    dealer_hand = Hand()
    begin_turn(dealer_hand, new_deck)

    bet(player_chips)

    line_break()

    player_hand.check()
    dealer_hand.check_dealer_some()

    GAME_ON = True

    while GAME_ON:

        hit_or_stand(player_hand, new_deck)

        if player_hand.value > 21:
            player_busts(player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(dealer_hand, new_deck)

        player_hand.check()
        dealer_hand.check_dealer()

        if dealer_hand.value > 21:
            dealer_busts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)

        else:
            push()

    line_break()
    check_bank(player_chips)
    print(f"\nYou have {player_chips.bank} in the bank.")

    print("Ya ready for another hand?")
    play_again = input("Enter 1 to play another hand, or any other key to quit.\n")

    if play_again.strip() != "1":
        print("Thanks for stoppin' by!")
        break
