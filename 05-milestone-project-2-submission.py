from IPython.display import clear_output # For Jupyter Notebooks
import random

# Global variables for use throughout the program
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = (
  'Two',
  'Three',
  'Four',
  'Five',
  'Six',
  'Seven',
  'Eight',
  'Nine',
  'Ten',
  'Jack',
  'Queen',
  'King',
  'Ace'
)
values = {
  'Two': 2,
  'Three': 3,
  'Four': 4,
  'Five': 5,
  'Six': 6,
  'Seven': 7,
  'Eight': 8,
  'Nine': 9,
  'Ten': 10,
  'Jack': 10,
  'Queen': 10,
  'King': 10,
  'Ace': 11
}

playing = True

## Class objects within the game ##

# Card class for individual card
class Card:
    '''Single card class with suit and rank value'''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

# Deck class to store all card objects
class Deck:
    def __init__(self):
        '''
          Initialise Deck object with attribute of list of Card objects from all ranks and suits
        '''
        self.deck = []  # start with empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        '''Return back to print() a summary of all Deck card attributes'''
        deck_debug_list = ''
        cards_num = 0

        for card in self.deck:
            deck_debug_list += '\n '+ card.__str__()
            cards_num += 1

        return f'Number: {cards_num}\nDeck of cards contains: {deck_debug_list}'

    def shuffle(self):
        '''Randomize the order of Card objects in the deck'''
        random.shuffle(self.deck)
        
    def deal(self):
        '''Pop off the last card object from deck list, and return'''
        dealt_card = self.deck.pop()
        return dealt_card

# Hand class for players, stores card objects dealt from Deck, as well as calculate value of cards using values global
class Hand:
    def __init__(self):
        self.cards = []  # start with empty list
        self.value = 0   # start with zero value
        self.aces = 0    # add attribute to track aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1 

# Chips class to track players' starting value, bets, and winning/losses
class Chips:
    def __init__(self):
        self.total = 150
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


## Game Function Definitions ##

def take_bet(chips):
    '''
    Take an integer value bet amount from a player
    Check value against player chips total
    '''
    while True:
        try:
            chips.bet = int(input("Amount you would like to bet: "))
        except ValueError:
            print("Error: Bet amount must be a number")
            continue
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet cannot exceed your total chips amount of: €{chips.total}")
            else:
                print(f"Bet placed of €{chips.bet}")
                break


def hit_me(deck, hand):
    '''
    Deal one card off the deck and add it to the Hand
    Check for Aces after hit
    '''
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    '''
    Parent function to handle players hitting or standing
    ''' 
    global playing
    hit_options = ["h", "hi", "hit"]
    stand_options = ["s", "st", "sta", "stan", "stand"]
    
    while True:
        player_choice = str(input("Next action (Hit/Stand): "))

        if player_choice.lower() in hit_options:
            print("Hit me!\n")
            hit_me(deck,hand)
        elif player_choice.lower() in stand_options:
            print("Player stands, dealer to play")
            playing = False
        else:
            print("Please choose Hit or Stand")
            continue
        break

        
def show_some(player,dealer):
    '''Show players' hands and dealer starting position '''
    clear_output()
    print("Dealer's Hand: ")
    print("< card face down >")
    print("", dealer.cards[1])
    print("\n")
    print("Player's Hand: ", *player.cards, sep="\n")


def show_all(player,dealer):
    '''Show all players' hands and totals'''
    print("\n")
    print("Dealer's Hand: ", *dealer.cards, sep="\n")
    print(f"Hand Value: {dealer.value}")
    print("\n")
    print("Player's Hand: ", *player.cards, sep="\n")
    print(f"Hand Value: {player.value}")


def player_busts(chips):
    '''Player loses his hand'''
    print("Player bust, bet lost :(")
    chips.lose_bet()


def player_wins(chips):
    '''Player wins his hand'''
    print("Player wins, bet won :)")
    chips.win_bet()


def dealer_busts(chips):
    '''Dealer loses his hand'''
    print("Dealer busts! Bet won :)")
    chips.win_bet()


def dealer_wins(chips):
    '''Dealer wins his hand'''
    print("Dealer wins! Bet lost :(")
    chips.lose_bet()


def push():
    '''Dealer and player tie'''
    print("Dealer / Player tie. It's a push (whatever that is...)")


##################
### Game Setup ###
##################

while True:
    # Print the opening text
    print("Welcome to Python Blackjack!")
    print("Are you ready to begin?")
    while True:
        player_ready = input("(y/n): ")
        if player_ready == "y":
            print("Let's start dealing!")
            break
        else:
            print("Whenever you're ready")
            continue
    
    # Create and Shuffle the Deck
    game_deck = Deck()
    game_deck.shuffle()
    
    # Setup the players' hands
    game_dealer = Hand()
    player_one = Hand()
    
    # Set up the Player's chips
    player_one_bank = Chips()
    
    # Save all player hands and banks to lists
    all_players = [player_one]
    all_banks = [player_one_bank]
    
    # Deal two cards to each player
    for i in range(0,2):
        game_dealer.add_card(game_deck.deal())
    
    for player in all_players:
        for i in range(0,2):
            player.add_card(game_deck.deal())

    # Take player bets 
    for player in all_players:
        print(f"\nPlayer_{all_players.index(player)+1} place your bet")
        print(f"Current chips total: {all_banks[all_players.index(player)].total}")
        take_bet(all_banks[all_players.index(player)])
    
    # Show starting setup of cards
    print("\n")
    show_some(player_one,game_dealer)
    
    while playing:
        # Player hit or stand
        hit_or_stand(game_deck, player_one)
        
        # Show cards after hit
        show_some(player_one,game_dealer)
        
        # Player over 21, bust
        if player_one.value > 21:
            player_busts(player_one_bank)
            break
    
    if player_one.value <= 21:
        while game_dealer.value < 17:
            hit_me(game_deck, game_dealer)
        
        # Show all Cards
        show_all(player_one, game_dealer)
        
        # Run different win scenarios
        if game_dealer.value > 21:
            dealer_busts(player_one_bank)
        elif game_dealer.value > player_one.value:
            dealer_wins(player_one_bank)
        elif game_dealer.value < player_one.value:
            player_wins(player_one_bank)
        else:
            push()
    else:
        # Show all Cards
        show_all(player_one, game_dealer)
    
    # Inform Player of their chips total 
    print("\nPlayer's chips total stands at",player_one_bank.total)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        clear_output()
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break