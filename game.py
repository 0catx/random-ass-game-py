# *
# * Copyright (C) 2026 0catx.me
# * This file is part of random-ass-game.
# *
# * DOUBLE GUESS is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * any later version.
# *

import random
import sys
import os
import time, datetime
import uuid
import sqlite3

os.environ['TZ']='UTC'
time.tzset()

Range_Start = 1
Range_End = 11

NumA = 0
NumB = 0

GuessA = 0
GuessB = 0

# | Diff | Pay |
# |------|-----|
# | 0    | 3   |
# | 1    | 2   |
# | 2    | 1   |
# | 3    | 1   |
# | 4    | 1   |
# | 5    | 0   |
# | 6    | 0   |
# | 7    | 0   |
# | 8    | 0   |
# | 9    | 0   |
# | 10   | 0   |

Payouts = [
    (0, 3),
    (1, 2),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 0),
    (6, 0),
    (7, 0),
    (8, 0),
    (9, 0),
    (10, 0)
]

def get_payout(inputted,):
    
    # Create offset-to-payout dictionary for faster lookup
    payout_map = {offset: pay for offset, pay in Payouts}
    
    return payout_map.get(inputted, 0)

def gen_numbers():
    global NumA
    global NumB

    NumA = random.randint(Range_Start, Range_End)
    NumB = random.randint(Range_Start, Range_End)

def find_offset(num, inputted):
    return abs(num - int(inputted))

def is_input_valid(inputted):
    if inputted=="69" or inputted=="67" or inputted=="420" or inputted=="clanker" or inputted=="e=mc^2" or inputted=="e" or inputted=="amongus" or inputted=="gyatt" or inputted=="skibidi" or inputted=="ohio rizz" or inputted=="rizz":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Just Why!?!??\nYou know what? screw you, I'ma restart the game now >:P\a")
        time.sleep(5)
        main()
    else:
        try:
            int(inputted)
            if int(inputted) in range(Range_Start, Range_End):
                return True
            else:
                return False
        except ValueError:
            return False

def record_outcomes(Final_payout, NumA, GuessA, NumB, GuessB):
    ID = str(uuid.uuid4())
    time = str(datetime.datetime.now())

    try:
        con = sqlite3.connect("game.db")
        cur = con.cursor()
        cur.execute(
    "INSERT INTO games (ID, Score, NumA, NumAGuess, NumB, NumBGuess, CreateTime) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (str(ID), int(Final_payout), int(NumA), int(GuessA), int(NumB), int(GuessB), str(time)))
        cur.connection.commit()
        cur.connection.close()
    except Exception as e:
        raise ValueError(f"\a{e}")


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    global GuessA
    global GuessB

    gen_numbers()
    print("\033[1mDOUBLE GUESS!\033[0m v0.1\nA really dumb number guessing game :p\n\n   Copyright (c) 2093, all rights not reversed.\n\nTwo numbers are randomly picked from \033[1m1 to 10\033[0m, you have to \033[1mguess what’s\nthe two numbers within the range\033[0m, you earn points based on how close you are to the picked number\nwithin a offset tolerance of \033[1m±4\033[0m.\n(0 being spot on, giving $3. within ±1 to ±4 is fairly accurate, giving $2-1. ±5 and beyond gets nothing)\n")

    # Ask for 1st guess
    GuessA = input("What's your guess for the \033[1mfirst number\033[0m? ")
    inputted = GuessA.lower()
    while is_input_valid(inputted)==False:
        GuessA = input("Seems invalid, I'll ask again. What's your guess for the \033[1mfirst number\033[0m? ")
        inputted = GuessA.lower()
        if is_input_valid(inputted)==False:
            continue
        else:
            break

    # Ask for 2nd guess
    GuessB = input("What's your guess for the \033[1msecond number\033[0m? ")
    inputted = GuessB.lower()
    while is_input_valid(inputted)==False:  
        GuessB = input("Seems invalid, I'll ask again. What's your guess for the \033[1msecond number\033[0m? ")
        inputted = GuessB.lower()
        if is_input_valid(inputted)==False:
            continue
        else:
            break
    
    # Offset
    num = NumA
    inputted = GuessA
    offsetA = find_offset(num, inputted)
    num = NumB
    inputted = GuessB
    offsetB = find_offset(num, inputted)

    # Payout
    inputted = offsetA
    payA = get_payout(inputted)
    inputted = offsetB
    payB = get_payout(inputted)

    Final_payout = payA + payB


    # Final results
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"How close where you? Well...\nThe first number was {NumA}, you said {GuessA}: You're {offsetA} units off, you earn \033[1m${payA}\033[0m. \nThe second number was {NumB}, you said {GuessB}: You're {offsetB} units off, you earn \033[1m${payB}\033[0m.")

    try:
        record_outcomes(Final_payout, NumA, GuessA, NumB, GuessB)
    except Exception as e:
        print(f"\n There was recoverable error recording you're payout, check in with the operator for assistance.\nError: {e}")

    print(f"\nYour final Payout is \033[1m${Final_payout}\033[0m, check in with the operator to claim your prize.\a\n\nPress any key to restart.")

    input()
    main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAlright, bye... (Check in operator for assistance)\a")
    except Exception as e:
        print(f"\nThere was a error! Get the lazy operator for assistance: {e}\a")
