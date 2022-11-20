def draw(n, deck, player, game):
    # Draw n cards

    if deck == "treasure":
        for i in range(0, n):
            player.treasure_cards.append(game.treasure_deck.pop())
            item = player.treasure_cards[-1]
            print("You have been given",item.name)

    else:  # For loot cards
        for i in range(0, n):
            player.loot_cards.append(game.loot_deck.pop())
        print(str(n)+" cards given to player "+str(player.id))


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


def chooseTreasureCard(player):
    for card in player.treasure_cards:
        print(vars(card))

    while True:
        selection = input("Select card (By number (1-" + str(len(player.treasure_cards) - 1) + "): ")
        try:
            selection = int(selection)
            if 0 < selection < len(player.treasure_cards):
                player.treasure_cards[selection]

        except:
            continue
        break


def discardLoot(player):
    lootcard = chooseLootCard(player)
    player.loot_cards.remove(lootcard)