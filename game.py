# Receive server updates
# Code
import random
import lootcardfunctions as lcf
import cardoperations as co
import dice
import monstercardfunctions as mcf
from event import Event, EventType

game = None
server = None


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
    def __init__(self, name, passive_effect, active_effect, cost_effect, guppy):
        self.tapped = False  # Whether active item has been used (passive items keep this as false)
        self.passive_effect = passive_effect  # Effect of a grey treasure (and trinket)
        self.active_effect = active_effect  # Effect of gold treasure
        self.cost_effect = cost_effect  # Effect of activating "cost" actives (e.g pay 3 to roll something)
        self.guppy = int(guppy)
        super().__init__(name)


class MonsterCard(Card):
    def __init__(self, name, type, maxhealth, defence, swords, reward, souls, effectBool):
        self.type = type
        self.maxhealth = maxhealth
        self.health = maxhealth
        self.defence = defence
        self.swords = swords
        self.reward = reward
        self.souls = souls
        self.effectBool = effectBool
        super().__init__(name)

    def attack_monster(self, player, defense, turn_hp, game):
        player.sendMessage("Press enter to roll")
        player.getChoice()
        player_attack = dice.dice()
        # ADD MODIFIERS --------------------------------------------------------------------------------------------------
        if mcf.nodamage(self, player_attack) and self.effectBool == 1:
            return False

        if player_attack >= defense:

            if self.take_damage(player.swords, game, player):  # Method returns True when monster dead
                return "m"  # If monster dead, return False to show combat isn't active
            else:
                return False

        else:
            if player.takeDamage(self.swords):
                return "p"  # Same as above but for player
            else:
                return False

    def take_damage(self, damage, game, player):
        if self.name == "The Duke Of Flies" and dice.dice() == 1: # DOF Blocks damage on 1
            self.health += damage
            print("Rolled 1, Damage negated")
        self.health -= damage
        return self.check_dead(game, player)

    def check_dead(self, game, player):
        if self.health <= 0:  # Monster has died

            print(self.reward[1], self.reward[0])
            # Reward decoder:
            if self.reward[1] == "C":
                if self.reward[0] == "x":
                    determined_reward = dice.dice()
                else:
                    determined_reward = self.reward[0]
                print("Reward: "+str(determined_reward)+" coins")
                player.coins += int(determined_reward)
                print("You now have", player.coins)

            elif self.reward[1] == "L":
                if self.reward[0] == "x":
                    determined_reward = dice.dice()
                else:
                    determined_reward = self.reward[0]
                co.draw(int(determined_reward), "loot", player, game)

            elif self.reward[1] == "T":
                co.draw(int(self.reward[0]), "treasure", player, game)

            else:
                print("YOU MISSED A CODE")

            player.souls += self.souls

            for slot in game.active_monsters:
                if len(slot) == 0:  # If monster slot is empty, draw card
                    slot = [game.monster_deck.pop()]
                    while slot[-1].type == "immediate":
                        self.immediate_handler(slot[-1], game)
                        slot = [game.monster_deck.pop()]

            return True

        print("Target not dead, Remaining HP: " + str(self.health))
        return False

    def immediate_handler(self, card, game):
        if "Chest" in card.name or "Secret" in card.name:

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
                outcomes = "-1THP;-1THP;-1THP;-2THP;-2THP;--GUPPY"

            elif card.name == "Secret Room!":
                outcomes = "-3THP;-2L;-2L;+7C;+7C;+1T"

            else:
                print("FALSE DETECTION")

            lcf.roll(game.players[game.turn-1], outcomes, game)

        else:

            if card.name == "XL Floor!":
                game.active_monsters.append([])
                game.active_monsters[-1].append(game.monster_deck.pop())

            elif card.name == "We Need To Go Deeper":
                num = input("Enter how many discarded monsters to put back on top")
                size = len(game.monster_discard)
                for i in range(size-1, size-1-num, -1):
                    game.monster_deck.append(game.mondster_discard[i])
                    game.monster_discard.pop(i)
                print("Do you want to attack again?")
                player = game.players[game.turn-1]
                choice = player.getChoice(["Yes", "No"])
                if choice == 0:
                    player.attack()

            elif card.name == "Troll Bombs":
                game.players[game.turn-1].takeDamage(2)

            elif card.name == "I Can See Forever":
                lcf.cardtype(card, game.players[game.turn-1], game)

            elif card.name == "Greed!":
                candidates = []
                max = -1
                for player in game.players:
                    if player.coins > max:
                        candidates = [player]
                        max = player.coins
                    elif player.coins == max:
                        candidates.append[player]
                target = None
                if len(candidates) == 1:
                    target = candidates[0]
                elif len(candidates) > 1:
                    choices = []
                    for candidate in candidates:
                        choices.append("player " + str(candidate.id))
                    target = candidates[player.getChoice(choices)]
                if len != 0:
                    target.setCoins(0)

            elif card.name == "Mega Troll Bomb!":
                for player in game.players:
                    player.takeDamage(2)

            elif card.name == "Devil Deal":
                choices = ["Loot 2, Take 1 Damage", "Search the treasure deck for a guppy item. Gain it and take 2 damage. Shuffle the deck."]
                print(choices)
                player = game.players[game.turn-1]
                choice = int(player.getChoice())
                if choice == 0:
                    co.draw(2, "loot", player, game)
                    player.takeDamage(1)
                else:
                    deck = game.treasure_deck
                    card = None
                    for i in range(len(deck) - 1, 0, -1):
                        card1 = deck[i]
                        if card1.guppy == True:
                            card = card1
                    if card is None:
                        print("No guppy card")
                    else:
                        player.treasure_cards.append(card)
                        game.treasure_deck.remove(card)
                    player.takeDamage(2)

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
        self.coins = 20
        self.loot_cards = []
        self.treasure_cards = []
        self.character_card = None
        self.souls = 0
        self.id = id
        self.maxhealth = 2
        self.swords = 1
        self.temp_damage = 0
        self.health = self.maxhealth
        self.dead = False
        self.client = client

    def playLoot(self, selection):
        card = self.loot_cards[selection]
        lcf.cardtype(card, self, game)

    def takeDamage(self, amount):
        self.health -= amount
        if game.players[game.turn-1] == self: #Only display damage info about current player
            print("Took",amount,"damage. You are now on",self.health)
        if self.health <= 0:
            self.pay_death_penalities()
            return True
        return False


    def pay_death_penalities(self):

        if not self.dead:
            print("Player",self.id,"has died.")
            if len(self.loot_cards) > 0:
                print("Choose a loot card to discard (0-"+str(len(self.loot_cards)-1)+")")
                self.loot_cards.remove(co.chooseLootCard(self))
            if self.coins > 0:
                self.coins -= 1

            if len(self.treasure_cards) == 2:
                game.treasure_discard.append(self.treasure_cards[1])
                self.treasure_cards = []

            if len(self.treasure_cards) > 2:
                print("Choose a treasure card to discard (1-" + str(len(self.treasure_cards)-1) + ")")
                self.treasure_cards.remove(co.chooseTreasureCard(self))

            self.dead = True

    def getChoice(self, choices):
        server.sendEvent(self.client, Event(EventType.CLIENTBOUND_CHOICE_REQUEST, choices))

        response = []
        def onResponse(event):
            response.append(event.data[0])
            
        server.addListener(EventType.SERVERBOUND_CHOICE_RESPONSE, onResponse)

        while (len(response)) == 0:
            pass
        server.removeListener(EventType.SERVERBOUND_CHOICE_RESPONSE, onResponse)
        return response[0]

    def sendMessage(self, message):
        server.sendEvent(self.client, Event(EventType.CLIENTBOUND_SEND_MESSAGE, [message]))


class Game:
    def __init__(self, players):
        global game
        # Generate Decks as objects
        self.loot_deck = []
        self.treasure_deck = []
        self.treasure_discard = []
        self.monster_deck = []
        self.monster_discard = []
        self.character_deck = []
        self.active_monsters = [[], []]
        self.active_shop = []
        self.playerMap = {}

        # Create for n players. Works for up to 6 players
        self.players = []
        for i in range(1, players+1):
            self.players.append(Player(i, server.connections[i-1]))  # i is the player id

        # Current player's turn. Starts as turn = 1, as player 1 goes first. Number represents the player.
        self.turn = 1

        # Instantiate decks and shuffle
        self.loot_deck = Deck().createDeck(104, "loot")
        random.shuffle(self.loot_deck)
        self.treasure_deck = Deck().createDeck(105, "treasure")
        random.shuffle(self.treasure_deck)
        self.monster_deck = Deck().createDeck(107, "monster")
        random.shuffle(self.monster_deck)
        self.character_deck = Deck().createDeck(18, "character")
        random.shuffle(self.character_deck)

        # Give player starting loot cards
        for player in self.players:
            co.draw(30, "loot", player, self)

        for slot in self.active_monsters:
            while True:
                card_from_top = self.monster_deck.pop()
                if card_from_top.type == "monster":
                    slot.append(card_from_top)
                    break
                else:
                    self.monster_discard.append(card_from_top)

        for i in range(2):
            self.active_shop.append(self.treasure_deck.pop())

        game = self
        # Start the game
        self.main_loop()

    def sendMessageAll(self, messgae):
        for player in self.players:
            player.sendMessage

    def main_loop(self):

        currentPlayer = None
        for player in self.players:
            if self.turn == player.id:
                currentPlayer = player
                currentPlayer.health = currentPlayer.maxhealth
                currentPlayer.dead = False

        print("received response " + currentPlayer.getChoice(["Yes", "No"]))

        print("Starting player ", currentPlayer.id, "'s turn")

        currentPlayer.freecardplayed = False

        currentPlayer.coins += 1
        print("Player", currentPlayer.id, "has", currentPlayer.coins, "coins")

        co.draw(1, "loot", currentPlayer, self)

        while True:
            sendMessage("Play loot card? [Y/N]: ")
            playcard = getChoice()
            if playcard == "Y":
                card = co.chooseLootCard(currentPlayer)
                lcf.cardtype(card, currentPlayer, self)
                currentPlayer.loot_cards.remove(card)
                currentPlayer.freecardplayed = True
                break
            if playcard == "N":
                break
            else:
                pass

        if not currentPlayer.dead:
            if currentPlayer.freecardplayed:
                while True:
                    sendMessage("Play loot card? [Y/N]: ")
                    playcard = getChoice()
                    if playcard == "Y":
                        card = co.chooseLootCard(currentPlayer)
                        lcf.cardtype(card, currentPlayer, self)
                        currentPlayer.loot_cards.remove(card)
                        # Player card is tapped
                        break
                    if playcard == "N":
                        break
                    else:
                        pass

            if not currentPlayer.dead:

                print("SHOP: ")
                for slot in self.active_shop:
                    print(slot.name)  # Going to have to add card descriptors so people know what the card does :(

                if currentPlayer.coins >= 10:
                    while True:
                        sendMessage("Buy Item? [Y/N]: ")
                        buy_item = getChoice()
                        if buy_item == "Y":
                            choices = ["Deck"]
                            print("0: Deck")
                            for slot in self.active_shop:
                                choices.append(slot.name)
                                print(slot.name)

                            which_item = 999
                            while int(which_item) > len(choices):
                                sendMessage("Select Item [0-"+str(len(choices)-1)+"]: ")
                                which_item = getChoice()
                                if which_item == "0":
                                    currentPlayer.treasure_cards.append(self.treasure_deck.pop())
                                    currentPlayer.coins -= 10

                                else:
                                    print("Player "+str(currentPlayer.id)+" has bought "+str(self.active_shop[int(which_item)-1].name))
                                    currentPlayer.treasure_cards.append(self.active_shop[int(which_item)-1])
                                    self.active_shop[int(which_item)-1] = self.treasure_deck.pop()

                            currentPlayer.coins -= 10
                            break

                            # Look at current player treasure hand, if steam sale present, add 5 coins back
                        if buy_item == "N":
                            break
                        else:
                            pass

                else:
                    print("You don't have 10 coins, skipping shop phase")

                print()
                self.checkMonsterSlots()
                print("Active Monsters:")
                for slot in self.active_monsters:
                    print("Name:", str(slot[-1].name)+",", "Health:", str(slot[-1].health)+",", "Required Roll:", str(slot[-1].defence)+",", "Attack power:", str(slot[-1].swords)+",", "Rewards:", str(slot[-1].reward)+",",  "Souls:", str(slot[-1].souls))

                print()
                while True and not currentPlayer.dead:
                    sendMessage("Attack a monster? [Y/N]: ")
                    do_attack = getChoice()

                    if do_attack == "Y":
                        monsters = ["Deck"]
                        print("0: Deck")
                        for slot in self.active_monsters:
                            monsters.append(slot[-1].name)
                            print(slot[-1].name)

                        which_monster = 999
                        while int(which_monster) > len(monsters):
                            sendMessage("Select monster [0-"+str(len(monsters)-1)+"]")
                            which_monster = getChoice()

                            monster = None
                            while True:
                                if which_monster == "0":
                                    self.active_monsters[0].append(self.monster_deck.pop())
                                    monster = self.active_monsters[0][-1]
                                    if monster.type == "monster":
                                        print("Name:", str(self.active_monsters[0][-1].name) + ",", "Health:", str(self.active_monsters[0][-1].health) + ",", "Required Roll:", str(self.active_monsters[0][-1].defence) + ",", "Attack power:", str(self.active_monsters[0][-1].swords) + ",", "Rewards:",str(self.active_monsters[0][-1].reward) + ",", "Souls:", str(self.active_monsters[0][-1].souls))
                                    if monster.type == "immediate":
                                        print(monster.name)
                                        monster.immediate_handler(monster, self)
                                        self.active_monsters[0].pop()
                                        self.checkMonsterSlots()
                                        if player.health > 0:
                                            continue
                                        else:
                                            break
                                else:
                                    monster = self.active_monsters[int(which_monster)-1][-1]
                                    break

                            while True:
                                print(player.health)
                                if player.health <= 0: #If player died from an immediate being pulled from top
                                    break
                                combat_ended = monster.attack_monster(currentPlayer, monster.defence, monster.health, self)
                                if combat_ended == "m":
                                    print("Monster defeated")
                                    game.monster_discard.append(self.active_monsters[int(which_monster)-1].pop())

                                    self.checkMonsterSlots()
                                    break
                                elif combat_ended == "p":
                                    print("Player defeated")
                                    break
                                else:
                                    pass
                        break



                    if do_attack == "N":
                        break
                    else:
                        pass

        for slot in self.active_monsters:
            for monster in slot:
                monster.health = monster.maxhealth



        self.turn += 1

        if self.turn > len(self.players):
            self.turn = 1

    def checkMonsterSlots(self):
        for slot in self.active_monsters:
            while len(slot) == 0:
                newcard = self.monster_deck.pop()

                if newcard.type == "immediate":
                    newcard.immediate_handler(newcard, self)

                if newcard.type == "monster":
                    slot.append(newcard)

def createGame(s):
    global server
    server = s
    print("creating game")
    game = Game(len(server.connections))


