# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
from scipy import spatial


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "xhemals",  # TODO: Your Battlesnake Username
        "color": "#ff0000",  # TODO: Choose color
        "head": "ski",  # TODO: Choose head
        "tail": "nr-booster",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")
    print(f"Width: {game_state['board']['width']}")
    print(f"Height: {game_state['board']['height']}")
    print(f"Head: {game_state['you']['body'][0]}")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    my_body = game_state['you']['body']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    opponents = game_state['board']['snakes']
    foods = game_state['board']['food']
    hazards = game_state['board']['hazards']

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    possible_moves = {
        "up": {
            "x": my_head["x"],
            "y": my_head["y"] - 1,
            "safe": True,
        },
        "down": {
            "x": my_head["x"],
            "y": my_head["y"] + 1,
            "safe": True,
        },
        "left": {
            "x": my_head["x"] - 1,
            "y": my_head["y"],
            "safe": True,
        },
        "right": {
            "x": my_head["x"] + 1,
            "y": my_head["y"],
            "safe": True,
        }
    }
    
    def avoidBody():
        for c in my_body:
            if c["x"] == my_head["x"] - 1 and c["y"] == my_head["y"]:
                possible_moves["left"]["safe"] = False
            elif c["x"] == my_head["x"] + 1 and c["y"] == my_head["y"]:
                possible_moves["right"]["safe"] = False
            elif c["y"] == my_head["y"] - 1 and c["x"] == my_head["x"]:
                possible_moves["down"]["safe"] = False
            elif c["y"] == my_head["y"] + 1 and c["x"] == my_head["x"]:
                possible_moves["up"]["safe"] = False
    
    def avoidWalls():
        if my_head["x"] == 0:
            possible_moves["left"]["safe"] = False
        if my_head["x"] == board_width-1:
            possible_moves["right"]["safe"] = False
        if my_head["y"] == 0:
            possible_moves["down"]["safe"] = False
        if my_head["y"] == board_height-1:
            possible_moves["up"]["safe"] = False
        return is_move_safe

    def avoidSnakes():
        for s in opponents:
            for c in s["body"]:
                if c["x"] == my_head["x"] - 1 and c["y"] == my_head["y"]:
                    possible_moves["left"]["safe"] = False
                elif c["x"] == my_head["x"] + 1 and c["y"] == my_head["y"]:
                    possible_moves["right"]["safe"] = False
                elif c["y"] == my_head["y"] - 1 and c["x"] == my_head["x"]:
                    possible_moves["down"]["safe"] = False
                elif c["y"] == my_head["y"] + 1 and c["x"] == my_head["x"]:
                    possible_moves["up"]["safe"] = False
        return is_move_safe

    def avoidHazards():
        for c in hazards:
            if c["x"] == my_head["x"] - 1 and c["y"] == my_head["y"]:
                possible_moves["left"]["safe"] = False
            elif c["x"] == my_head["x"] + 1 and c["y"] == my_head["y"]:
                possible_moves["right"]["safe"] = False
            elif c["y"] == my_head["y"] - 1 and c["x"] == my_head["x"]:
                possible_moves["down"]["safe"] = False
            elif c["y"] == my_head["y"] + 1 and c["x"] == my_head["x"]:
                possible_moves["up"]["safe"] = False

    def findFood():
        coordinates = []
        if len(foods) == 0:
            return None

        for food in foods:
            coordinates.append((food["x"], food["y"]))

        tree = spatial.KDTree(coordinates)
        results = tree.query([(my_head["x"], my_head["y"])])[1]
        return foods[results[0]]
    
    def goToFood():
        distance_x = abs(my_head["x"] - target["x"])
        distance_y = abs(my_head["y"] - target["y"])

        for direction, location in possible_moves.items():
            new_distance_x = abs(location["x"] - target["x"])
            new_distance_y = abs(location["y"] - target["y"])
            if new_distance_x < distance_x or new_distance_y < distance_y:
                return direction
        
        return list(possible_moves.keys())[0]



    # Are there any safe moves left?
    avoidWalls()
    avoidBody()
    avoidSnakes()
    avoidHazards()
    safe_moves = []
    for move, isSafe in possible_moves.items():
        if not isSafe["safe"]:
            safe_moves.append(move)
            
    intersection = [i for i in safe_moves if i in possible_moves]
    for move in intersection:
            del possible_moves[move]
    target = findFood()

    

    if len(possible_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        print(f"Head: {my_head}")
        print(f"Body: {my_body}")
        print(f"Possible Moves: {safe_moves}")
        return {"move": "down"}

    # Choose a random move from the safe ones
    if target is not None:
        next_move = goToFood()
        print(next_move)
    else:
        possible_moves = list(possible_moves.keys())
        next_move = random.choice(possible_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer

    print(f"Head: {my_head}")
    print(f"Body: {my_body}")
    print(f"Possible Moves: {possible_moves}")
    print(f"Food: {target}")
    # print(f"Board: {game_state['board']}")
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})
