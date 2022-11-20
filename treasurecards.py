import cardoperations as co
import lootcardfunctions as lcf
import game
import random

# Unless specified, player == player who owns the treasure

# -- General Passive:


# Steamy Sale!
def steamy_sale(player):
    player.coins += 5


# -- On Death:


# Suicide King
def suicide_king(player):
    co.draw(3, "loot", player, game)


# -- Greed's Gullet
def greeds_gullet(player):
    player.coins += 8


# -- On Damage:

# Fanny Pack:
def fanny_pack(player):
    co.draw(1, "loot", player, game)

# -- End of Turn:


# Starter Deck
def starter_deck(player):
    if len(player.loot_cards) >= 8:
        co.draw(2, "loot", player, game)


# Eden's Blessing
def edens_blessing(player):
    if player.coins == 0:
        player.coins += 6


# The Polaroid
def the_polaroid(player):
    if len(player.loot_cards) == 0:
        co.draw(2, "loot", player, game)


# The Map
def the_map(player):
    args = "monster,4,4"
    lcf.scry(args, game)


# The Blue Map
def the_blue_map(player):
    args = "treasure,4,4"
    lcf.scry(args, game)


# The Compass
def the_compass(player):
    args = "loot,4,4"
    lcf.scry(args, game)

# -- Start of Turn:


# Mom's Coin Purse
def moms_coin_purse(player):
    co.draw(1, "loot", player, game)


# Mom's Purse
def moms_purse(player):
    co.draw(1, "loot", player, game)


# Dark Bum
def dark_bum(player):
    args = "+3C;+3C;+1L:+1L;-1THP;-1THP"
    lcf.reroll(args)


# -- On Roll Val:

# Mom's Box
def moms_box(player, dice_roll):
    if dice_roll == 4:
        player.sendMessage("Mom's Box? Y/N")
        choice = player.getChoice()
        if choice == "Y":
            co.draw(1, "loot", player, game)
            co.discardLoot(player)


# Sacred Heart
def sacred_heart(player, dice_roll, current_player):
    if dice_roll == 1 and player == current_player:
        player.sendMessage("Sacred Heart? Y/N")
        choice = player.getChoice()
        if choice == "Y":
            dice_roll = 1
    return dice_roll


# The Relic
def the_relic(player, dice_roll):
    if dice_roll == 1:
        co.draw(1, "loot", player, game)


# Dad's Lost Coin
def dads_lost_coin(player, dice_roll):
    if dice_roll == 1:
        player.sendMessage("Dad's Lost Coin? Y/N")
        choice = player.getChoice()
        if choice == "Y":
            dice_roll = lcf.reroll("roll")

    return dice_roll


# Eye of Greed
def eye_of_greed(player, dice_roll):
    if dice_roll == 5:
        player.coins += 3


# -- Tap Treasures:

# Jawbone
def jawbone(player, target_player):
    if target_player.coins > 3:
        player.coins += target_player.coins
        target_player.coins = 0
    else:
        player.coins += 3
        target_player.coins -= 3


# Lucky Foot
def lucky_foot(roll):
    roll += 2
    return roll


# Mr Boom
def mr_boom(player, monster):
    monster.take_damage(1, game, player)


# Mystery Sack
def mystery_sack(player):
    args = "+1L;+1L;+4C;+4C;---;---"
    lcf.roll(player, args, game)


# Boomerang
def boomerang(player, target):
    target_index = random.randint(0,len(target.loot_cards)-1)
    target_card = target.loot_cards[target_index]
    target.loot_cards.remove(target_card)
    player.loot_cards.append(target_card)


# Book of Sin
def book_of_sin(player):
    args = "+1C;+1C;+1L;+1L;+1THP;+1THP"
    lcf.reroll(args)


# The D100
def the_d100(player):
    args = "+1L;2L;+3C;+4C;+1THP:-1TSW"
    lcf.reroll(args)


# Godhead
def godhead(player, dice_roll):
    player.sendMessage("1 or 6? ")
    choice = player.getChoice()
    if choice == "1":
        dice_roll = 1
    elif choice == "6":
        dice_roll = 6
    else:
        print("Failed")

    return dice_roll


# Sack Head
def sack_head(player, game):
    player.sendMessage("Enter a deck: ")
    deck = player.getChoice()
    card_look_at = game.deck.pop()
    print(card_look_at)
    player.sendMessage("Place on bottom? Y/N ")
    bot_or_top = player.getChoice()
    if bot_or_top == "Y":
        dummy_array = [card_look_at]
        deck = card_look_at + deck
    else:
        deck = deck.append(card_look_at)

    game.deck = deck


# -- Spend Treasures:


# Smelter
def smelter(player):
    if len(player.loot_cards) > 0:
        co.discardLoot(player)
        player.coins += 3
    else:
        print("No cards to smelt")


# Portable Slot Machine
def portable_slot_machine(player):
    if player.coins < 3:
        print("Not enough money")
    else:
        player.coins -= 3
        args = "+1L;+1L;+4C;+4C;---;---"



















