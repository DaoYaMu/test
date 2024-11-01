import random


def roll_dice(numbers=3, points=None):
    print('<<<<< ROLL THE DICE! >>>>>')
    if points is None:
        points = []
    while numbers > 0:
        point = random.randrange(1, 7)
        points.append(point)
        numbers -= 1
    return points


def roll_result(total):
    is_big = 11 <= total <= 18
    is_small = 3 <= total <= 10
    if is_big:
        return 'Big'
    elif is_small:
        return 'Small'


def start_game():
    print('<<<<< GAME STARTS! >>>>>')
    choices = ['Big', 'Small']

    while True:
        your_choice = input('Big or Small (type "quit" to exit): ').capitalize()

        if your_choice == 'Quit':
            print('Exiting the game. Goodbye!')
            break

        if your_choice in choices:
            points = roll_dice()
            total = sum(points)
            result = roll_result(total)

            print('The points are', points)

            if your_choice == result:
                print('You win!')
            else:
                print('You lose!')
        else:
            print('Invalid input. Please enter "Big" or "Small".')


if __name__ == "__main__":
    start_game()
