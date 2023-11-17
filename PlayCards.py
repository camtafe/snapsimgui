import random

class DeckOfCards:
    # creates all the cards in the deck and initializes the cards
    def __init__(self):
        self.rank = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.suit = ['Clubs', 'Hearts', 'Diamonds', 'Spades']

        self.cards = [Card(rank, suit) for rank in self.rank for suit in self.suit]

    # simply returns the decks cards
    def deck(self):
        return self.cards

    # shuffles the cards randomly using the fisher-yates algorithm
    def shuffle(self, num=1):
        length = len(self.cards)
        for x in range(num):
            # Fisher-Yates shuffle algorithm
            for i in range(length - 1, 0, -1):
                randomi = random.randint(0, i)
                if i == randomi:
                    continue
                self.cards[i], self.cards[randomi] = self.cards[randomi], self.cards[i]

    # draws a card from the deck if it has cards
    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None
        
    # displays all the cards in the deck
    def display_deck(self):
        for card in self.cards:
            print(card)

    # deals out cards from the deck to players until there are none left to distribute
    def deal(self, num_players):
        hands = [[] for _ in range(num_players)]

        while len(self.cards) > 0:
            for player_num in range(num_players):
                if len(self.cards) > 0:
                    card = self.draw()
                    hands[player_num].append(card)

        return hands


# Prints cards in a more readable way
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Tests the deck if ran as the main file
if __name__ == "__main__":
    deck_instance = DeckOfCards()
    deck_instance.shuffle()
    deck_instance.display_deck()