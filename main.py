import copy
import math
from typing import Union


# One way to optimize the code complexity would be to use a more efficient algorithm for finding the closest player.
# Currently, the code uses a nested loop to iterate over all remaining players and calculate the distance to each one.
# This has a time complexity of O(n^2), where n is the number of remaining players.
#
# A more efficient approach would be to use a data structure that allows for efficient nearest-neighbor searches, such
# as a kd-tree. A kd-tree can be used to store the positions of the remaining players and perform nearest-neighbor
# searches in O(log n) time on average. This would reduce the overall time complexity of the code to O(n log n).
#
# Another optimization would be to avoid making unnecessary copies of data. For example, the code currently makes
# a deepcopy of the list of players at the beginning of each game. This is unnecessary since the players list is not
# modified during the game. Instead, the code could simply make a shallow copy of the list using the slicing notation
# remaining_players = players[:i] + players[i+1:].
#
# Overall, these optimizations would improve the performance and scalability of the code, especially for larger inputs.


def find_direction(x1: float, y1: float, x2: float, y2: float) -> str:
    """
    Finds the direction between two points on a 2D plane.

    :param x1: The x-coordinate of the first point.
    :param y1: The y-coordinate of the first point.
    :param x2: The x-coordinate of the second point.
    :param y2: The y-coordinate of the second point.
    :return: A string representing the direction from the first point to the second point.
    """
    dx = x2 - x1
    dy = y2 - y1
    # If the difference in x-coordinates is zero
    if dx == 0:
        # If the difference in y-coordinates is greater than zero, return "N" for North, otherwise return "S" for South
        if dy > 0:
            return "N"
        else:
            return "S"

    # If the difference in y-coordinates is zero
    if dy == 0:
        # If the difference in x-coordinates is greater than zero, return "E" for East, otherwise return "W" for West
        if dx > 0:
            return "E"
        else:
            return "W"

    # If the difference in x-coordinates is greater than zero
    if dx > 0:
        # If the difference in y-coordinates is greater than zero
        if dy > 0:
            # If the absolute value of the difference in x-coordinates is equal to the absolute value of the difference
            # in y-coordinates, return "NE" for Northeast
            if abs(dx) == abs(dy):
                return "NE"
        else:
            # If the absolute value of the difference in x-coordinates is equal to the absolute value of the difference
            # in y-coordinates, return "SE" for Southeast
            if abs(dx) == abs(dy):
                return "SE"
    else:
        # If the difference in y-coordinates is greater than zero
        if dy > 0:
            # If the absolute value of the difference in x-coordinates is equal to the absolute value of the difference
            # in y-coordinates, return "NW" for Northwest
            if abs(dx) == abs(dy):
                return "NW"
        else:
            # If the absolute value of the difference in x-coordinates is equal to the absolute value of the difference
            # in y-coordinates, return "SW" for Southwest
            if abs(dx) == abs(dy):
                return "SW"


def play_game(players: list[tuple], starting_player: int, starting_direction: str) -> tuple[int, int]:
    """
    Simulate the game.

    :param players: a list of tuples representing the players in the game. Each tuple contains the x and y coordinates
        of a player's position.
    :param starting_player: an integer representing the index of the starting player in the players list.
    :param starting_direction: a string representing the starting direction that the first throw will go in.
    :return: tuple of number of throws and last player index.
    """
    remaining_players: list = copy.deepcopy(players)
    remaining_players.remove(players[starting_player])

    current_player = players[starting_player]
    num_throws: int = 0

    next_direction = {
        "N": "NE",
        "NE": "E",
        "E": "SE",
        "SE": "S",
        "S": "SW",
        "SW": "W",
        "W": "NW",
        "NW": "N",
    }
    reversed_directions = {
        "N": "S",
        "NE": "SW",
        "E": "W",
        "SE": "NW",
        "S": "N",
        "SW": "NE",
        "W": "E",
        "NW": "SE",
    }
    last_direction: str = starting_direction
    set_round: bool = True
    starting_direction_one_round: Union[str, None] = None
    n_player: int = 0
    while True:

        closest_player = None
        next_player_direction = None
        min_distance = float("inf")
        for i, remaining_player in enumerate(remaining_players):
            player_direction = find_direction(
                current_player[0],
                current_player[1],
                remaining_player[0],
                remaining_player[1],
            )

            if next_direction[last_direction] == player_direction:
                # TODO: sqrt operation can be removed and only squared Euclidean distance can be compared.
                distance = math.sqrt(
                    (remaining_player[0] - current_player[0]) ** 2
                    + (remaining_player[1] - current_player[1]) ** 2
                )
                if distance < min_distance:
                    min_distance = distance
                    closest_player = remaining_player
                    next_player_direction = player_direction

        if closest_player:
            n_player += 1
            last_direction: str = reversed_directions[next_player_direction]
            num_throws += 1
            current_player: tuple = closest_player
            remaining_players.remove(current_player)
            set_round: bool = True
            starting_direction_one_round: Union[str, None] = None
        else:
            last_direction = next_direction[last_direction]

            if starting_direction_one_round == last_direction:
                break

            if set_round:
                starting_direction_one_round: str = last_direction
                set_round: bool = False

    return num_throws, players.index(current_player)


if __name__ == "__main__":
    # Open and read the input file which contains information
    # about the number of test cases and the data for each test case.
    with open("test.in.txt", "r") as f:
        # Read the number of test cases from the first line
        T: int = int(f.readline().strip())

        # For each test case, read the data and call the `play_game` function
        for i in range(T):
            # Read the number of players for this test case
            N: int = int(f.readline().strip())

            # Read the coordinates of the players
            players: list[tuple] = []
            for j in range(N):
                x, y = map(int, f.readline().split())
                players.append((x, y))

            # Read the starting direction and player number
            starting_direction: str = f.readline().strip()
            starting_player: int = int(f.readline().strip()) - 1

            # Call the `play_game` function with the player data and starting info
            # The function will return the number of throws and the number of
            # the player who made the last catch.
            num_throws, last_player = play_game(
                players, starting_player, starting_direction
            )

            # Print the results for this test case
            print(num_throws, last_player + 1)
