def draw(n, deck, player=None):
    global game
    # Draw n cards

    if deck == "Monster":
        pass

    elif deck == "Treasure":
        pass

    else:  # For loot cards
        for i in range(0, n):
            player.loot_cards.append(game.loot_deck.pop())


def chooseLootCard(player):
    for card in player.loot_cards:
        print(vars(card))

    while True:
        selection = input("Select card (By number (0-" + str(len(player.loot_cards) - 1) + "): ")
        try:
            selection = int(selection)
            player.loot_cards[selection]
        except:
            continue
        else:
            player.freecardplayed = True
            return player.loot_cards[selection]
        break


def discardLoot(player):
    lootcard = chooseLootCard(player)
    player.loot_cards.remove(lootcard)