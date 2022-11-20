def nodamage(monster, roll):
    if monster.name == "Hopper" and player_attack == 6:
        return True

    if monster.name == "Carrion Queen" and (player_attack == 4 or player_attack == 5):
        return True

