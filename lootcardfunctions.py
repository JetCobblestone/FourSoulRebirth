import dice
import cardoperations as co


def cardtype(card, player, game):
    if card.type == "coin":
        player.coins += coin(card.func_args)
        print(player.coins)

    elif card.type == "bomb":
        print("Choose target: ")

        targets = []
        for player in game.players:
            targets.append(player)
        for monster_stack in game.active_monsters:
            targets.append(monster_stack[-1])

        for target in targets:
            try:
                print(target.name)

            except:
                print(target.id)

        target_choice = int(input())
        target = targets[target_choice]
        if str(type(target)) == "<class '__main__.Player'>":
            target.take_damage(bomb(card.func_args))
        else:
            if target.take_damage(bomb(card.func_args), game, player):  # Deal damage to the monster, if dead, handle it
                for slot in game.active_monsters:
                    if slot[-1] == target:
                        slot.pop()
                        game.checkMonsterSlots()
                        break


        # if target = monster, monster damage
        # else player damage

    elif card.type == "roll":
        roll(player, card.func_args, game)

    elif card.type == "battery":
        pass

    elif card.type == "prevent":
        pass

    elif card.type == "scry":
        scry(card.func_args, game)

    elif card.type == "buff":
        pass

    elif card.type == "reroll":
        # Doesn't worka atm, also useless as loot cards can only be played at the start of a turn
        reroll(card.func_args)

    elif card.type == "deny":
        pass

    elif card.type == "unique":
        pass

    elif card.type == "trinket":
        pass

    else:
        print("UNKNOWN CARD TYPE")


def coin(args):
    return int(args[0])


def bomb(args):
    try:
        int(args[0])

    # If args[0] is "roll", e.g. High Priestess is used
    except ValueError:
        return dice.dice()

    finally:
        return int(args[0])


def roll(player, args, game):
    elements = args.split(";")
    rolledElement = elements[dice.dice() - 1]

    # Roll decoder:
    # Read [:2] to determine magnitude of effect
    # Read [2:] end to determine what it does

    # Coin outcome:
    if rolledElement[2:] == "C":
        if rolledElement[0] == "+":
            player.coins += coin(rolledElement[1])
        elif rolledElement[0] == "-":
            player.coins -= coin(rolledElement[1])
            if player.coins < 0:
                player.coins = 0

        else:
            print("MISSING ADD/SUB")

        print(player.coins)

    # Loot Card outcome:
    elif rolledElement[2:] == "L":
        if rolledElement[0] == "+":
            co.draw(rolledElement[1], "loot", player, game)

        elif rolledElement[0] == "-":
            co.discardLoot(player)

        else:
            print("MISSING ADD/SUB")

    # Treasure outcome:
    elif rolledElement[2:] == "T":
        co.draw(1, "treasure", player, game)

    # TSW outcome:

    # THP outcome:

    # _all decoder:
    elif rolledElement[-3:] == "all":
        pass

    # GUPPY outcome:
    elif rolledElement[2:] == "GUPPY":
        deck = game.treasure_deck
        card = None
        for i in range(len(deck) - 1, 0, -1):
            card1 = deck[i]
            if card1.guppy:
                card = card1
        if card is None:
            print("No guppy card")
        else:
            player.treasure_cards.append(card)
            game.treasure_deck.remove(card)
        player.takeDamage(2)

    else:
        pass


def reroll(args):
    if args[0] == "roll":
        return dice.dice()

    elif args[0] == "choice":
        while True:
            choice = input("Enter a number between 1 and 6")

            try:
                choice = int(choice)

            except ValueError:
                print("NOT A NUM")

            finally:
                if 0 < choice < 7:
                    return choice

                else:
                    print("OUT OF RANGE")

    else:
        print("INVALID")


def scry(args, game):

    deck = args[0]
    lookat = args[1]
    ontop = args[2]

    # Initialise arrays
    scry_array = []
    ontop_array = []
    onbottom_array = []

    # Look at the designated num of values
    for i in range(0, lookat):
        scry_array.append = game.deck.pop()

    # Need to change so all players don't see it
    print(scry_array)
    # Player inputs their scry code
    scry_code = input("Enter a scry code as a list of indexes with no spaces: ")

    for i in range(len(scry_array)):
        if i < ontop:
            # Places the first ontop values in the array placed on the top of the deck
            ontop_array.append(scry_array[int(scry_code[i])])
        else:
            # The rest go on the bottom
            onbottom_array.append(scry_array[int(scry_code[i])])

    # Recreates deck with the scried cards. I'm sCRYING right now.
    deck = onbottom_array + deck + reversed(ontop_array)
    return deck
