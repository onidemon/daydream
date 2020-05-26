'''Python Project Idea – Make a program which randomly chooses a number to guess and then the user will have a few 
chances to guess the number correctly. In each wrong attempt, the computer will give a hint that the number is greater
or smaller than the one you have guessed.'''

from random import randint 

secret = randint(1,101)

user_input = input('Try to guess the secret number between 1 and 100, you get 5 tries. x to quit > ')
chances = 0

while chances < 5 and user_input != 'x':
    if user_input == 'x':
        break
    elif not user_input.isdigit():
        user_input = input('Not a valid number ')
    elif int(user_input) > secret:
        user_input = input('too high ')
        chances += 1
    elif int(user_input) < secret:
        user_input = input('too low ')
        chances += 1
    elif int(user_input) == secret:
        print(f'Congratulations you guess right, the secret number was {secret}')
        break

if  chances == 5 or int(user_input) == secret:
    print(f'The secret number was {secret} thank you for playing!')
elif user_input == 'x':
    print('goodbye!')
