BOARD_WIDTH = 10
BOARD_HEIGHT = 10

SHIPS = {
    "Cruiser" : 3,
    "Battleship" : 4,
    "AircraftCarrier" : 5
}

BOARD = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board():
    for i in range(BOARD_WIDTH):
        for j in range(BOARD_HEIGHT):
            print(BOARD[i][j], " ")
        print("\n")

print_board()