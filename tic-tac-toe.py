from typing import List
import random


def create_board(state: List[str]):
    """ prints the board with the current moves to stdout """
    print(" " + state[0] + " | " + state[1] + " | " + state[2] + " ")
    print("___|___|___")
    print(" " + state[3] + " | " + state[4] + " | " + state[5] + " ")
    print("___|___|___")
    print(" " + state[6] + " | " + state[7] + " | " + state[8] + " ")
    print("   |   |   ")

def win_list(pos: int):
    """ returns the list of lines attached to the given move """
    winList = {0: [[1,2], [3,6], [4,8]],
    1: [[0,2], [4,7]], 
    2: [[0,1],[5,8], [4,6]],
    3: [[0,6], [4,5]],
    4: [[0,8], [1,7],[2,6],[3,5]],
    5: [[2,8], [3,4]],
    6:[[0,3], [2,4], [7,8]],
    7:[[1,4], [6,8]],
    8:[[0,4],[2,5],[6,7]]}
    return winList[pos]

def check_win(pos: int, posList: List[str], letter: str):
    """ checks to see if either the user or computer have won the game """
    winList = win_list(pos)
    for i in winList:
        curVal = i[0]
        secVal = i[1]
        if (posList[curVal] == letter and posList[secVal] == letter):
            return True

def create_prompt():
    """ prompts the user for their next move """
    val = input("Choose a spot between 0 and 8: ")
    return int(val)

def mark_list(posList: List[str], val: int, letter: str):
    """ marks the latest move onto the board list"""
    posList[val] = letter
    return posList

def create_prompt_error():
    """ creates a new prompt if the user enters a number that has already been used"""
    val = input("That position is already taken. Choose a different number between 0 and 8: ")
    return int(val)

def generate_random(numList: List[int]):
    """ generates a random move using the remaining spaces """
    val = random.choice(numList)
    return val

def check_good_move(val: int, val2: int, posList: List[str]):
    """ checks to see if there is a move that will block the opponent
    or win the game """
    result = -1
    if (val2 != None):
        result = check_next("o", val2, posList)
    if (result == -1):
        result = check_next("x", val, posList)
    return result

def check_next(letter: str, val: int, posList: List[str]):
    """ checks to see if there is a line with two of the same letter in it"""
    winList = win_list(val)
    for i in winList:
        valOne = i[0]
        valTwo = i[1]
        if (posList[valOne] == letter and posList[valTwo] == " "):
            return valTwo
        elif (posList[valOne] == " " and posList[valTwo] == letter):
            return valOne
    return -1

def computer_move(numList: List[int], posList: List[str], val: int, val2: int):
    """ calls the functions to determine the computers next move """
    result = check_good_move(val, val2, posList)
    if (result == -1):
        val2 = generate_random(numList)
    else:
        val2 = result
    print("The computer chose", val2)
    posList = mark_list(posList, val2, "o")
    numList.remove(val2)
    return val2, numList

def user_move(numList: List[int], posList: List[str]):
    """ calls the functions to execute the users next move """
    val = int(create_prompt())
    while val not in numList:
        val = create_prompt_error()
    posList = mark_list(posList, val, "x")
    numList.remove(val)
    create_board(posList)
    return val, numList, posList


def start_game():
    """ calls the functions that will execute the game """
    posList = [" "," "," "," "," "," "," "," "," "]
    numList = [0,1,2,3,4,5,6,7,8]
    val2 = None
    for i in range(0,5):
        val, numList, posList = user_move(numList, posList)
        if (check_win(val, posList, "x")):
            return 1
        elif (i == 4):
            break
        val2, numList = computer_move(numList, posList, val, val2)
        create_board(posList)
        if (check_win(val2, posList, "o")):
            return 2
    return 0

def main():
    """ calls the functions to create the display in stdout and prints
    the results of the game """
    create_board(["0","1","2","3","4","5","6","7","8"])
    print("This is how the board will be laid out:")
    create_board([" "," "," "," "," "," "," "," "," "])
    outcome = start_game()
    if (outcome == 1):
        print("You won the game!")
    elif (outcome == 2):
        print("You lost the game!")
    else:
        print("It was a tie!")

main()
