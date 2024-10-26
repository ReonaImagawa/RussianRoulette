import random
round = 1
def display_round(live, blank):
    print(f'{live} : Live Rounds; {blank} : Blank Rounds')

def take_shot(shot, player_health, opponent_health):
    shot_at = int(input('Choose who to take shot at (Yourself(1) or Opponent(2)): '))
    if shot_at == 1:
        if shot == 1:
            player_health -= 50
            print(f'You hit yourself, New Health: {player_health}')
        else:
            print(f'You are safe, Health: {player_health}, You take next shot')

    if shot_at == 2:
        if shot == 1:
            opponent_health -= 50
            print(f'You hit opponent, Opponent Health: {opponent_health}')
        else:
            print(f'Opponent is safe, Opponent Health: {opponent_health}')

    return player_health, opponent_health
def bullet(live, blank, gun):
    for i in range(live):
        gun.append(1)
    for i in range(blank):
        gun.append(0)
    shot = gun[random.randint(0,live+blank-1)]
    gun = gun.remove(shot)
    return shot
def GameLoop():
    player_health = 100
    opponent_health = 100
    while (round < 4):
        gun = []
        if round == 1:
            live_round = 1
            blank_round = 2
            display_round(live_round, blank_round)
            shot = bullet(live_round, blank_round, gun)
            print(f'Shot: {shot}')
            print(gun)

        player_health, opponent_health = take_shot(shot, player_health, opponent_health)
        print(player_health, opponent_health)
        break
if __name__ == '__main__':
    GameLoop()