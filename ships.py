import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 10

SHIPS = {
    "Cruiser" : 3,
    "Battleship" : 4,
    "AircraftCarrier" : 5
}

BOARD = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board():
    print(" -" * BOARD_WIDTH)
    for i in range(BOARD_WIDTH):
        print("| ", end="")
        for j in range(BOARD_HEIGHT):
            print(BOARD[i][j], end=" ")
        print("|\n")
    print(" -" * BOARD_WIDTH)

def _orientations(cells):
    """Return unique rotations of a shape, normalized to its top-left corner."""
    result = []
    current = list(cells)
    for _ in range(4):
        min_x = min(x for x, _ in current)
        min_y = min(y for _, y in current)
        normalized = tuple(sorted((x - min_x, y - min_y) for x, y in current))
        if normalized not in result:
            result.append(normalized)
        current = [(-y, x) for x, y in current]
    return result


def place_ships(board_width : int, board_height : int, ships : dict) -> dict:
    if board_width < 1 or board_height < 1:
        raise ValueError("Board dimensions must be positive.")
    if any((ship_size if isinstance(ship_size, int) else len(ship_size)) < 1 for ship_size in ships.values()):
        raise ValueError("Ship sizes must be positive.")
    if sum(ship_size if isinstance(ship_size, int) else len(ship_size) for ship_size in ships.values()) > board_width * board_height:
        raise ValueError("The ships have more cells than the board.")

    board = [[None for _ in range(board_width)] for _ in range(board_height)]

    for ship_name, ship in ships.items():
        if isinstance(ship, int):
            cells = [(i, 0) for i in range(ship)]
        else:
            cells = ship
        placed = False
        for _ in range(1000):
            shape = random.choice(_orientations(cells))
            shape_width = max(x for x, _ in shape) + 1
            shape_height = max(y for _, y in shape) + 1
            if shape_width > board_width or shape_height > board_height:
                continue
            x = random.randint(0, board_width - shape_width)
            y = random.randint(0, board_height - shape_height)
            positions = [(x + cell_x, y + cell_y) for cell_x, cell_y in shape]

            # Check whether all positions are empty
            if all(board[py][px] is None for px, py in positions):

                # Place the ship
                for px, py in positions:
                    board[py][px] = ship_name

                placed = True
                break

        if not placed:
            raise ValueError(f"Unable to place {ship_name}; try a larger board or fewer ships.")

    return board

