import dice
import cardoperations as co


def cardtype(card, player):
    global game

    if card.type == "coin":
        player.coins += coin(card.func_args)
        print(player.coins)

    elif card.type == "bomb":
        print("Choose target: ")

        targets = game.players + game.active_monsters
        target_choice = input()
        target = targets[target_choice]
        target.turn_hp -= bomb(card.func_args)
        # target.checkdead()

    elif card.type == "roll":
        roll(player, card.func_args)

    elif card.type == "battery":
        pass

    elif card.type == "prevent":
        pass

    elif card.type == "scry":
        pass

    elif card.type == "buff":
        pass

    elif card.type == "reroll":
        pass

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


def roll(player, args):
    elements = args.split(";")
    rolledElement = elements[dice.dice()-1]

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
            co.draw(rolledElement[1], "loot", player)

        elif rolledElement[0] == "-":
                co.discardLoot(player)

        else:
            print("MISSING ADD/SUB")

    # Treasure outcome:
    elif rolledElement[2:] == "T":
        co.draw(1, "treasure", player)

    # TSW outcome:

    # THP outcome:

    # _all decoder:
    elif rolledElement[-3:-1] == "all":
        pass

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
        