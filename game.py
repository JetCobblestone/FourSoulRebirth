# Receive server updates
# Code
import random

class Deck:
    def __init__(self):
        pass

    def createDeck(decksize, type):
        # Sets the max size of the deck

        if type == "loot":
            cards = []
            rawtext = open("textfiles/lootcards.txt")
            rawtext = rawtext.readlines()
            for card in rawtext:
                #Formatting text document
                card = card.split('"')
                card = "".join(card)
                card = card.split(',')
                for effect in range(2,len(card)):
                    card[effect] = card[effect].strip("\n")

                cards.append(card)

            return cards[0:decksize-1]
        

class DiscardPile:
    def __init__(self, type):
        self.type = type


class Card:
    def __init__(self, name):
        self.name = name


class TreasureCard(Card):
    def __init__(self, name, is_passive, passive_effect=None, active_effect=None, cost_effect=None):
        self.passive = is_passive  # Whether item is active or passive (Gold/Grey border)
        self.tapped = False  # Whether active item has been used (passive items keep this as false)
        self.passive_effect = passive_effect  # Effect of a grey treasure (and trinket)
        self.active_effect = active_effect  # Effect of gold treasure
        self.cost_effect = cost_effect  # Effect of activating "cost" actives (e.g pay 3 to roll something)
        super().__init__(name)


class MonsterCard(Card):
    def __init__(self, name):
        super().__init__(name)


class LootCard(Card):
    def __init__(self, name):
        super().__init__(name)


class CharacterCard(Card):
    def __init__(self, name):
        super().__init__(name)


class Player:
    def __init__(self, id):
        self.coins = 3
        self.loot_cards = []
        self.treasure_cards = []
        self.character_card = None
        self.souls = 0
        self.id = id
        self.health = 2
        self.damage = 1
        self.temp_damage = 0
        self.temp_health = 0


class Game:
    def __init__(self, players):
        # Generate Decks as objects

        # Create for n players. Works for up to 6 players
        self.players = []
        for i in range(0, players):
            self.players.append(Player(i+1))  # i is the player id

        # Current player's turn. Starts as turn = 1, as player 1 goes first. Number represents the player.
        self.turn = 1

    def createDecks(self):

        #Instantiate loot deck and shuffle
        self.loot_deck = Deck.createDeck(48, "loot")
        random.shuffle(self.loot_deck)

        #Start the game
        self.main_loop()

    def main_loop(self):

        currentPlayer = None
        for player in self.players:
            if self.turn == player.id:
                currentPlayer = player

        currentPlayer.coins += 1

        print(currentPlayer.loot_cards)
        currentPlayer.loot_cards += draw(1, "loot", currentPlayer)
        print(currentPlayer.loot_cards)


def draw(n, deck, player=None):
    global game
    # Draw n cards

    if deck == "Monster":
        pass

    elif deck == "Treasure":
        pass

    else:  # For loot cards
        for i in range(0,n):
            player.loot_cards.append(game.loot_deck.pop())





game = Game(3)
game.createDecks()
