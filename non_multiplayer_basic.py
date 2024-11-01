import random


def display_round(live, blank):
    print(f'{live} : Live Rounds; {blank} : Blank Rounds')


def take_shot(shot, player_health, opponent_health, player, kill):
    shot_at = int(input(f'Choose who to take shot at Player {player} (Yourself({player}) or Opponent({3 - player})): '))
    if shot_at == player:
        if shot == 1:  # Live round
            player_health -= kill
            print(f'You hit yourself Player {player}, New Health: {player_health}')
        else:  # Blank round
            print(f'You are safe Player {player}, Health: {player_health}. You take next shot.')
        next_shot = player  # Player shoots again
    else:
        if shot == 1:  # Live round
            opponent_health -= kill
            print(f'You hit Player {3 - player}, Opponent Health: {opponent_health}')
        else:
            print(f'Player {3 - player} is safe, Opponent Health: {opponent_health}')
        next_shot = 3 - player  # Opponent's turn

    return player_health, opponent_health, next_shot


def initialize_gun(live, blank):
    gun = [1] * live + [0] * blank
    random.shuffle(gun)
    return gun


def bullet(gun):
    return gun.pop() if gun else None


def GameLoop():
    round_num = 1
    player_health = 100
    opponent_health = 100
    next_shot = 1  # Player 1 starts

    while player_health > 0 and opponent_health > 0 and round_num <= 3:
        if round_num == 1:
            live_round, blank_round = 1, 2
            player1items, player2items = GetItem()
        elif round_num == 2:
            live_round, blank_round = 3, 2
            player1items, player2items = GetItem()
        else:
            live_round, blank_round = 3, 3
            player1items, player2items = GetItem()

        gun = initialize_gun(live_round, blank_round)
        display_round(live_round, blank_round)

        print(f"\n--- Round {round_num} ---")

        while gun and player_health > 0 and opponent_health > 0:
            shot = bullet(gun)
            # print(f'Shot Outcome: {"Live" if shot == 1 else "Blank"}')

            if next_shot == 1:
                item = SelectItem(player1items, player2items, 1)
                if item is None:
                    saw_used = False
                else:
                    gun, player_health, saw_used = UseItem(item, gun, player_health, player1items, shot)
                player_health, opponent_health, next_shot = take_shot(shot, player_health, opponent_health, 1,
                                                                      50 if saw_used else 25)
            else:
                item = SelectItem(player1items, player2items, 2)
                if item is None:
                    saw_used = False
                else:
                    gun, opponent_health, saw_used = UseItem(item, gun, opponent_health, player2items, shot)
                opponent_health, player_health, next_shot = take_shot(shot, opponent_health, player_health, 2,
                                                                      50 if saw_used else 25)

            print(f"Player 1 Health: {player_health}, Player 2 Health: {opponent_health}")

        round_num += 1

    if player_health <= 0:
        print("Player 1 has been defeated. Player 2 wins!")
    elif opponent_health <= 0:
        print("Player 2 has been defeated. Player 1 wins!")
    else:
        print("Game over! No one has been defeated.")


def GetItem():
    itemlist = ['Beer', 'Burner Phone', 'Cigarette', 'Saw', 'Inverter', 'Magnifying Glass']
    player1_items = random.choices(itemlist, k=4)
    player2_items = random.choices(itemlist, k=4)
    return player1_items, player2_items


def SelectItem(player_1_items, player_2_items, player):
    selection = int(input(
        f'Select which item you want from your list Player {player} (Enter 0 if none are required at this point) {player_1_items if player == 1 else player_2_items} : ')) - 1
    return None if selection < 0 else player_1_items[selection] if player == 1 else player_2_items[selection]


def UseItem(item, gun, player_health, player_items, shot):
    if item == 'Beer':
        ejected = gun.pop() if len(gun) > 0 else shot
        print(f"Ejected Shell was {'Live' if ejected == 1 else 'Blank'} ")
    elif item == 'Burner Phone':
        position = random.randint(0, len(gun))
        print(f"Shot No {position} from this shot is  {'Live' if gun[-position] == 1 else 'Blank'}")
    elif item == 'Cigarette':
        player_health += 50 if player_health <= 50 else 100 - player_health
    elif item == 'Inverter':
        position = random.randint(0, len(gun) - 1)
        gun[position] = 0 if gun[position] == 1 else 1
    elif item == 'Magnifying Glass':
        shell = shot
        print(f'The shot in the chamber is a {'Live' if shell == 1 else 'Blank'}')
    player_items.remove(item)
    return gun, player_health, True if item == 'Saw' else False


if __name__ == '__main__':
    GameLoop()
