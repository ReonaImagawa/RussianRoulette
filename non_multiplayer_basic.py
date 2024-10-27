import random


def display_round(live, blank):
    print(f'{live} : Live Rounds; {blank} : Blank Rounds')


def take_shot(shot, player_health, opponent_health, player):
    shot_at = int(input(f'Choose who to take shot at Player {player} (Yourself({player}) or Opponent({3-player})): '))
    if shot_at == player:
        if shot == 1:  # Live round
            player_health -= 25
            print(f'You hit yourself Player {player}, New Health: {player_health}')
        else:  # Blank round
            print(f'You are safe Player {player}, Health: {player_health}. You take next shot.')
        next_shot = 1  # Player shoots again
    else:
        if shot == 1:  # Live round
            opponent_health -= 25
            print(f'You hit Player {3 - player}, Opponent Health: {opponent_health}')
        else:
            print(f'Player {3 - player} is safe, Opponent Health: {opponent_health}')
        next_shot = 2  # Opponent's turn

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
        elif round_num == 2:
            live_round, blank_round = 2, 3
        else:
            live_round, blank_round = 3, 3

        gun = initialize_gun(live_round, blank_round)
        display_round(live_round, blank_round)

        print(f"\n--- Round {round_num} ---")

        while gun and player_health > 0 and opponent_health > 0:
            shot = bullet(gun)
            #print(f'Shot Outcome: {"Live" if shot == 1 else "Blank"}')

            if next_shot == 1:
                player_health, opponent_health, next_shot = take_shot(shot, player_health, opponent_health, 1)
            else:
                opponent_health, player_health, next_shot = take_shot(shot, opponent_health, player_health, 2)

            print(f"Player 1 Health: {player_health}, Player 2 Health: {opponent_health}")

        round_num += 1

    if player_health <= 0:
        print("Player 1 has been defeated. Player 2 wins!")
    elif opponent_health <= 0:
        print("Player 2 has been defeated. Player 1 wins!")
    else:
        print("Game over! No one has been defeated.")


if __name__ == '__main__':
    GameLoop()
