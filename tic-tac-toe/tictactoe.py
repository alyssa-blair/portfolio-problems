from typing import List
import random

# list of winning lines
winList = {0: [[1,2], [3,6], [4,8]],
               1: [[0,2], [4,7]], 
               2: [[0,1],[5,8], [4,6]],
               3: [[0,6], [4,5]],
               4: [[0,8], [1,7],[2,6],[3,5]],
               5: [[2,8], [3,4]],
               6:[[0,3], [2,4], [7,8]],
               7:[[1,4], [6,8]],
               8:[[0,4],[2,5],[6,7]]}


def create_board(state: List[str]):
    # print the current state of the board
    print(" " + state[0] + " | " + state[1] + " | " + state[2] + " ")
    print("___|___|___")
    print(" " + state[3] + " | " + state[4] + " | " + state[5] + " ")
    print("___|___|___")
    print(" " + state[6] + " | " + state[7] + " | " + state[8] + " ")
    print("   |   |   ")
    
    
def check_win(pos: int, posList: List[str], letter: str):
    # check to see if there is a winning line
    curPos = winList[pos]
    
    for i in curPos:
        curVal = i[0]
        secVal = i[1]
        
        # if there is, return true
        if (posList[curVal] == letter and posList[secVal] == letter):
            return True

def check_good_move(val: int, val2: int, posList: List[str]):
    # check if there is an almost winning line for the computer or opponent
    result = -1
    if (val2 != None):
        # choose winning spot
        result = check_next("o", val2, posList)
    if (result == -1):
        # block user
        result = check_next("x", val, posList)
    return result

def check_next(letter: str, val: int, posList: List[str]):
    # check if there is an almost winning line
    curPos = winList[val]
    
    for i in curPos:
        valOne = i[0]
        valTwo = i[1]
        
        # if there is an almost winning line, return the empty position
        if (posList[valOne] == letter and posList[valTwo] == " "):
            return valTwo
        elif (posList[valOne] == " " and posList[valTwo] == letter):
            return valOne
          
    # otherwise, return -1
    return -1

def computer_move(numList: List[int], posList: List[str], val: int, val2: int):
    # check if the computer can block a line
    result = check_good_move(val, val2, posList)
    if (result == -1):
        # if not, pick random value from list
        val2 = random.choice(numList)
    else:
        val2 = result
        
    # display and mark off the computers move 
    print("The computer chose", val2)
    posList[val2] = "o"
    numList.remove(val2)
    return val2, numList

def user_move(numList: List[int], posList: List[str]):
    # prompt user until valid input
    val = int(input("Choose a spot between 0 and 8: "))
    while val not in numList:
        val = int(input("That position is already taken. Choose a different number between 0 and 8: "))

    # mark off the users move 
    posList[val] = "x"
    numList.remove(val)
    create_board(posList)
    return val, numList, posList


def start_game():
    # initialize the positions
    posList = [" "," "," "," "," "," "," "," "," "]
    numList = [0,1,2,3,4,5,6,7,8]
    val2 = None
    
    for i in range(0,5):
        # get the user move 
        val, numList, posList = user_move(numList, posList)
        
        # check if the user has won
        if (check_win(val, posList, "x")):
            return 1
        elif (i == 4):
            # no more moves
            break
           
        # create the computers move 
        val2, numList = computer_move(numList, posList, val, val2)
        create_board(posList)
        
        # check if computer won the game
        if (check_win(val2, posList, "o")):
            return 2
        
    # otherwise, it was a tie
    return 0

def main():
    # display layout of game board
    create_board(["0","1","2","3","4","5","6","7","8"])
    print("This is how the board will be laid out:")
    create_board([" "," "," "," "," "," "," "," "," "])
    
    outcome = start_game()
    
    # determine the outcome 
    if (outcome == 1):
        print("You won the game!")
    elif (outcome == 2):
        print("You lost the game!")
    else:
        print("It was a tie!")

main()
