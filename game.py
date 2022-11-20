# Receive server updates
# Code
import random
import lootcardfunctions as lcf
from event import EventType, Event
import cardoperations as co
import dice


class Deck:

    def __init__(self):
        pass

    def createDeck(self, decksize, deckType):
        # Sets the max size of the deck
        cards = []
        if deckType == "loot":
            with open("textfiles/lootcards.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line == "---\n":
                        break
                    vals = line.split(',')
                    cardargs = []
                    for effect in range(2, len(vals)):
                        cardargs.append(vals[effect])

                    cardargs[-1] = cardargs[-1].strip("\n")

                    cards.append(LootCard(vals[0], vals[1], cardargs))

        elif deckType == "treasure":
            with open("textfiles/treasurecards.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line == "---\n":
                        break
                    vals = line.split(",")
                    vals[-1] = vals[-1].strip("\n")
                    cards.append(TreasureCard(vals[0], int(vals[1]), int(vals[2]), int(vals[3]), int(vals[4])))

        elif deckType == "monster":
            with open("textfiles/monstercards.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line == "---\n":
                        break
                    vals = line.split(',')
                    vals[-1] = vals[-1].strip("\n")

                    cards.append(MonsterCard(vals[0], vals[1], int(vals[2]), int(vals[3]), int(vals[4]), vals[5], int(vals[6]), int(vals[7])))
        elif deckType == "character":
            with open("textfiles/charactercards.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line == "---\n":
                        break
                    vals = line.split(',')
                    vals[-1] = vals[-1].strip("\n")
                    cards.append(CharacterCard(vals[0]))
        else:
            raise Exception("Invalid deck type")

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
    def __init__(self, name, type, health, defence, swords, reward, souls, effectBool):
        self.type = type
        self.health = health
        self.turn_hp = health
        self.defence = defence
        self.swords = swords
        self.reward = reward
        self.souls = souls
        self.effectBool = effectBool
        super().__init__(name)

    def attack_monster(self, player, defense, turn_hp):
        player_attack = dice.dice()
        # ADD MODIFIERS --------------------------------------------------------------------------------------------------
        if player_attack >= defense:
            self.take_damage(player.swords)
        else:
            player.turn_hp -= self.swords

    def take_damage(self, damage):
        self.turn_hp -= damage
        self.check_dead(game.players[game.turn])

    def check_dead(self, whos_turn):
        if self.turn_hp <= 0:  # Monster has died

            # Reward decoder:
            if self.reward[1] == "C":
                whos_turn.coins += int(self.reward[0])

            elif self.reward[1] == "L":
                co.draw(int(self.reward[0]), "loot", whos_turn, game)

            elif self.reward[1] == "T":
                co.draw(int(self.reward[0]), "treasure", whos_turn, game)

            else:
                print("YOU MISSED A CODE")

            whos_turn.souls += self.souls

            for slot in game.active_monsters:
                if len(slot) == 0:  # If monster slot is empty, draw card
                    slot.append(game.monster_deck.pop())
                    while slot[-1].type == "immediate":
                        self.immediate_handler((slot[-1]))
                        slot.append(game.monster_deck.pop())

        print("Target not dead, Remaining HP: " + str(self.turn_hp))

    def immediate_handler(self, card):

        if card.name.find("Chest") or card.name.find("Secret"):

            if card.name == "Gold_Chest":
                outcomes = "+1T;+1T;+1L;+1L;+2L,+2L"

            elif card.name == "Gold Chest":
                outcomes = "+1T;+1T;+5C;+5C;+7C;+7C"

            elif card.name == "Chest_":
                outcomes = "+1L;+1L;+2L;+2L;+3L;+3L"

            elif card.name == "Chest":
                outcomes = "+1C;+1C;+3C;+3C;+6C;+6C"

            elif card.name == "Dark_Chest":
                outcomes = "+1C;+1C;+2L;+2L;-2THP;-2THP"

            elif card.name == "Dark Chest":
                outcomes = "+1L;+1L;+3C;+3C;-2THP;-2THP"

            elif card.name == "Cursed Chest":
                outcomes = "-1THP;-1THP;-1THP;-2THP;-2THP;--GUPPY"  # <----------------- GUPPY

            elif card.name == "Secret Room!":
                outcomes = "-3THP;-2L;-2L;+7C;+7C;+1T"

            else:
                print("FALSE DETECTION")

            lcf.roll(game.players[game.turn], outcomes, game)
        else:

            if card.name == "XL Floor!":
                game.active_monsters.append([])
                game.active_monsters[-1].append(game.monster_deck.pop())

            elif card.name == "We Need To Go Deeper":
                pass

            elif card.name == "Troll Bombs":
                pass

            elif card.name == "I Can See Forever":
                pass

            elif card.name == "Greed!":
                pass

            elif card.name == "Mega Troll Bomb":
                pass

            elif card.name == "Devil Deal":
                pass

            else:
                print(card.name)
                print("Card name not found ^")

class LootCard(Card):
    def __init__(self, name, type, func_args):
        super().__init__(name)
        self.type = type
        self.func_args = func_args


class CharacterCard(Card):
    def __init__(self, name):
        super().__init__(name)


class Player:
    def __init__(self, id, client):
        self.coins = 3
        self.loot_cards = []
        self.treasure_cards = []
        self.character_card = None
        self.souls = 0
        self.id = id
        self.health = 2
        self.damage = 1
        self.temp_damage = 0
        self.temp_hp = 0
        self.client = client

    def playLoot(self, selection):
        card = self.loot_cards[selection]
        lcf.cardtype(card, self, game)


class Game:
    def __init__(self, players, server):
        # Generate Decks as objects
        self.loot_deck = []
        self.treasure_deck = []
        self.monster_deck = []
        self.monster_discard = []
        self.character_deck = []
        self.active_monsters = [[],[]]
        self.active_shop = []

        # Create for n players. Works for up to 6 players
        self.players = []
        for i in range(0, players):
            self.players.append(Player(i+1, server.connections[i]))  # i is the player id

        # Current player's turn. Starts as turn = 1, as player 1 goes first. Number represents the player.
        self.turn = 1

        # Instantiate decks and shuffle
        self.loot_deck = Deck().createDeck(104, "loot")
        random.shuffle(self.loot_deck)
        self.treasure_deck = Deck().createDeck(105, "treasure")
        random.shuffle(self.treasure_deck)
        self.monster_deck = Deck().createDeck(107,"monster")
        random.shuffle(self.monster_deck)
        self.character_deck = Deck().createDeck(18, "character")
        random.shuffle(self.character_deck)

        responses = {}

        # Called when a response is received
        def choicesMade(eventObj):
            responses[str(eventObj.data[0])] = eventObj.data[1]
            if len(responses) != len(self.players):
                return

            # Give player starting loot cards
            for player in self.players:
                co.draw(3, "loot", player)

            for slot in self.active_monsters:
                while True:
                    card_from_top = self.monster_deck.pop()
                    if card_from_top.type == "monster":
                        slot.append(card_from_top)
                        break
                    else:
                        game.monster_discard.append(card_from_top)

            # Start the game
            self.main_loop()
        game = self
        server.addListener(EventType.SERVERBOUND_CHARACTER_CHOICE, choicesMade)

        # Players make character selection
        for i in range(len(self.players)):
            player = self.players[i]
            server.sendEvent(player.client, Event(EventType.CLIENTBOUND_CHARACTER_CHOICE, [self.character_deck[(3*i)], self.character_deck[(3*i)+1], self.character_deck[(3*i)+2]]))

    def main_loop(self):

        if self.turn > len(self.players):
            self.turn = 1



        currentPlayer = None
        for player in self.players:
            if self.turn == player.id:
                currentPlayer = player

        self.turn += 1

        currentPlayer.freecardplayed = False

        currentPlayer.coins += 1

        co.draw(1, "loot", currentPlayer)

        while True:
            playcard = input("Play lootcard? Y/N: ")
            if playcard == "Y":
                card = co.chooseLootCard(currentPlayer)
                lcf.cardtype(card, currentPlayer, game)
                break
            if playcard == "N":
                break
            else:
                pass


def createGame(server):
    print("creating game")
    Game(len(server.connections), server)

game = ""