from PlayCards import DeckOfCards
import pygame as pg
import random
import time

# setting variables for dimensions and speed of the game
pg.init()
width, height = 400, 450
fps = 30
clock = pg.time.Clock()
clock.tick(fps)
display_surface = pg.display.set_mode((width, height))
pg.display.set_caption('Snap Game GUI')


# colors for the background and text
white = (255, 255, 255)
black = (0, 0, 0)
mint = (107, 214, 189)
pg.font.init()
font = pg.font.SysFont(None, 24)


# holds the players cards that are dealt from the DeckOfCards deck
class Player:
    def __init__(self):
        self.inventory = []


# creates the requirements for a player to successfully snap
# if the last two cards on the pile are the same rank or number, they can be snapped
def snap(pile):
    if len(pile) >= 2:
        last_card = pile[-1]
        second_last_card = pile[-2]
        if last_card.rank == second_last_card.rank or last_card.suit == second_last_card.suit:
            return True
    return False

# method for displaying the text on the screen
def create_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    display_surface.blit(text_surface, text_rect)

# creates the display and allows for text from the simulation to be displayed
def create_game(players, current_player_index, pile, last_print_text):
    display_surface.fill(mint)

    # display player hand sizes
    for i, player in enumerate(players):
        create_text(f"Player {i + 1}: {len(player.inventory)} cards", black, 100, 50 + i * 25)

    # display current player acting
    create_text(f"Current Player: {current_player_index + 1}", black, width // 2, height - 50)

    # display pile size
    create_text(f"Pile: {len(pile)}", black, width // 2, height - 80)

    # prints the last statement created from the simulation
    create_text(last_print_text, black, width // 2, height - 150)

    # refreshes the screen
    pg.display.flip()


# checks the amount of players to determine when to stop the loop
# counts each player that has an inventory/hand bigger than 0 and returns it
def player_check(players):
    count = sum(1 for player in players if len(player.inventory) > 0)
    return count


def simulate_game(num_players):
    deck_instance = DeckOfCards()
    deck_instance.shuffle()
    hands = deck_instance.deal(num_players)
    players = [Player() for _ in range(num_players)]
    current_player_index = 0
    pile = []

    for i, player_hand in enumerate(hands):
        players[i].inventory = player_hand
        print(f"Player {i + 1} Hand: {len(players[current_player_index].inventory)} Cards")

    if player_check(players) > 1:
        running = True
        while running and player_check(players) > 1:
            # Esc to quit during loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

            # game logic
            # skips a player if they do not have any cards to play
            if len(hands[current_player_index]) > 0:
                # places the players card from their hand into the pile and states which card is placed into the pile
                played_card = hands[current_player_index].pop(0)
                pile.append(played_card)
                print(f"Player {current_player_index + 1} places {played_card} into the pile.")
                create_game(players, current_player_index, pile, f"Player {current_player_index + 1} places {played_card} into the pile.")
                time.sleep(0.5)

                # adds the cards from the pile to the players inventory if they successfully snap
                if snap(pile):
                    # 90% chance the bot will realise it is a snap to add some randomness to who wins
                    if random.random() > 0.10:
                        pile_amount = len(pile)
                        print(f"\nSnap! Player {current_player_index + 1} called snap!")
                        create_game(players, current_player_index, pile, f"Snap! Player {current_player_index + 1} called snap and gained {pile_amount} cards!")
                        time.sleep(1)
                        players[current_player_index].inventory.extend(pile)
                        print(f"Player {current_player_index + 1} gained: {pile_amount} cards!")
                        print(f"Player {current_player_index + 1} has: {len(players[current_player_index].inventory)} cards!\n")
                        pile = []
                    else:
                        print(f"\nWow! Player {current_player_index + 1} missed the snap, how unfortunate!\n")
                        create_game(players, current_player_index, pile, f"Wow! Player {current_player_index + 1} missed the snap, how unfortunate!")
                    time.sleep(0.5)

                # if a player uses their final card and does not get a snap, it states their elimination from the game aka having no cards to play and being skipped
                if len(hands[current_player_index]) == 0:
                    print(f"\nPlayer {current_player_index + 1} has exhausted their hand! They have been eliminated from the game!\n")
                    create_game(players, current_player_index, pile, f"Player {current_player_index + 1} has no cards! They've been eliminated!")
                    time.sleep(1)

            # iterates between each player
            current_player_index = (current_player_index + 1) % num_players

    # displays the final results
    for i, player in enumerate(players):
        print(f"Player {i + 1} has {len(player.inventory)} cards.")

    winner = next((i for i, player in enumerate(players) if len(player.inventory) > 0), None)
    if winner is not None:
        print(f"\nPlayer {winner + 1} is the winner!")
        create_game(players, current_player_index, pile, f"Player {winner + 1} is the winner!")
    else:
        print("\nIt's a draw!")
        create_game(players, current_player_index, pile, f"It is a draw!")

    # Esc to quit after loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False


# if this is ran as the main file, it will play the game and inquire into how many players and error handle misinputs
if __name__ == "__main__":
    while True:
        try:
            amount = int(input("How many players do you want to play with? "))
            if 2 <= amount <= 10:
                break
            else:
                print("Select a number between 2 and 10.")
        except ValueError:
            print("Invalid input. Put in a number from 2 to 10.")

    simulate_game(amount)
    pg.quit()
