__author__ = 'Hao'

import argparse
import time
from math import *

#######################################
# Ontology variables

PREFIX = "http://tw.rpi.edu/web/Courses/Ontologies/2016/OE_6_Soccer_Offside/"
HAS_SENSOR = "<" + PREFIX + "hasSensor> "
HAS_SAMPLING_TIME = "<" + PREFIX + "hasSamplingTime> "
HAS_X = "<" + PREFIX + "hasX> "
HAS_Y = "<" + PREFIX + "hasY> "
HAS_Z = "<" + PREFIX + "hasZ> "

#######################################
# Metadata

REFEREE_IDS = ["105", "106"]
GLOVE_IDS = ["97", "98", "99", "100"]
BALL_SIDS = ["4", "8", "10"]
NOT_NEEDED_IDS = REFEREE_IDS + GLOVE_IDS

SID_MAP = {
    # Balls:
    "4":  {"type": "ball", "label": "ball004"},
    "8":  {"type": "ball", "label": "ball008"},
    "10": {"type": "ball", "label": "ball010"},
    # Team A:
    "13": {"type": "player", "team": "A", "label": "playerA1", "name": "Nick Gertje", "leg": "left"},
    "14": {"type": "player", "team": "A", "label": "playerA1", "name": "Nick Gertje", "leg": "right"},
    "47": {"type": "player", "team": "A", "label": "playerA2", "name": "Dennis Dotterweich", "leg": "left"},
    "16": {"type": "player", "team": "A", "label": "playerA2", "name": "Dennis Dotterweich", "leg": "right"},
    "49": {"type": "player", "team": "A", "label": "playerA3", "name": "Niklas Waelzlein", "leg": "left"},
    "88": {"type": "player", "team": "A", "label": "playerA3", "name": "Niklas Waelzlein", "leg": "right"},
    "19": {"type": "player", "team": "A", "label": "playerA4", "name": "Wili Sommer", "leg": "left"},
    "52": {"type": "player", "team": "A", "label": "playerA4", "name": "Wili Sommer", "leg": "right"},
    "53": {"type": "player", "team": "A", "label": "playerA5", "name": "Philipp Harlass", "leg": "left"},
    "54": {"type": "player", "team": "A", "label": "playerA5", "name": "Philipp Harlass", "leg": "right"},
    "23": {"type": "player", "team": "A", "label": "playerA6", "name": "Roman Hartleb", "leg": "left"},
    "24": {"type": "player", "team": "A", "label": "playerA6", "name": "Roman Hartleb", "leg": "right"},
    "57": {"type": "player", "team": "A", "label": "playerA7", "name": "Erik Engelhardt", "leg": "left"},
    "58": {"type": "player", "team": "A", "label": "playerA7", "name": "Erik Engelhardt", "leg": "right"},
    "59": {"type": "player", "team": "A", "label": "playerA8", "name": "Sandro Schneider", "leg": "left"},
    "28": {"type": "player", "team": "A", "label": "playerA8", "name": "Sandro Schneider", "leg": "right"},
    # Team B:
    "61": {"type": "player", "team": "B", "label": "playerB1", "name": "Leon Krapf", "leg": "left"},
    "62": {"type": "player", "team": "B", "label": "playerB1", "name": "Leon Krapf", "leg": "right"},
    "63": {"type": "player", "team": "B", "label": "playerB2", "name": "Kevin Baer", "leg": "left"},
    "64": {"type": "player", "team": "B", "label": "playerB2", "name": "Kevin Baer", "leg": "right"},
    "65": {"type": "player", "team": "B", "label": "playerB3", "name": "Luca Ziegler", "leg": "left"},
    "66": {"type": "player", "team": "B", "label": "playerB3", "name": "Luca Ziegler", "leg": "right"},
    "67": {"type": "player", "team": "B", "label": "playerB4", "name": "Ben Mueller", "leg": "left"},
    "68": {"type": "player", "team": "B", "label": "playerB4", "name": "Ben Mueller", "leg": "right"},
    "69": {"type": "player", "team": "B", "label": "playerB5", "name": "Vale Reitstetter", "leg": "left"},
    "38": {"type": "player", "team": "B", "label": "playerB5", "name": "Vale Reitstetter", "leg": "right"},
    "71": {"type": "player", "team": "B", "label": "playerB6", "name": "Christopher Lee", "leg": "left"},
    "40": {"type": "player", "team": "B", "label": "playerB6", "name": "Christopher Lee", "leg": "right"},
    "73": {"type": "player", "team": "B", "label": "playerB7", "name": "Leon Heinze", "leg": "left"},
    "74": {"type": "player", "team": "B", "label": "playerB7", "name": "Leon Heinze", "leg": "right"},
    "75": {"type": "player", "team": "B", "label": "playerB8", "name": "Leo Langhans", "leg": "left"},
    "44": {"type": "player", "team": "B", "label": "playerB8", "name": "Leo Langhans", "leg": "right"}
}

#######################################
# Initial conditions

INITIAL_TIME = 10629342490369879
APPROXIMATE_START_TIME = 119

# Suggested coordinates for the field of play: (0,33965), (0,-33960),(52483,33965),(52483,-33960)
#
# -33960--------0---y-->---33965
# |             |              |
# |             x              |
# |             |              |
# |             V              |
# |___________52483____________|

X_MIN = 0
X_MAX = 52483
Y_MIN = -33960
Y_MAX = 33965

# Team B is the red team and team A is the yellow team
GOAL_LINE_A = Y_MIN
GOAL_LINE_B = Y_MAX
# ===> NEED TO IMPLEMENT THIS NEXT

#######################################
# Helper functions

def toSID(x):
    return "SID" + "0" * (3 - len(x)) + x


def get_average(a, b):
    return (
        (a[0] + b[0]) / 2,
        (a[1] + b[1]) / 2,
        (a[2] + b[2]) / 2
    )


def get_distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def display_seconds_as_minutes(t):
    return str(floor(t / 60)) + ":" + str(round(t % 60, 3))


def print_list_with_linebreak(list):
    """
    Helper function to print out a list with line breaks for better display
    """
    for x in list:
        print(x)


def ball_out(x, y):
    return x < X_MIN or x > X_MAX or y < Y_MIN or y > Y_MAX


def is_out(loc):
    return loc[0] < X_MIN or loc[0] > X_MAX or loc[1] < Y_MIN or loc[1] > Y_MAX


#######################################
# Main parsing process

def main():

    t = time.time()

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT', help='input file')
    args = parser.parse_args()

    # Open input file
    with open(args.input, "r") as f:

        count = 0

        # Keep track of ball and player informations
        balls = {}
        players = {}
        for sid in SID_MAP:
            if SID_MAP[sid]["type"] is "ball":
                balls[SID_MAP[sid]["label"]] = {
                    "location": (0, 0, 0),
                    "ball-in": False,
                    "player": None
                }
                # print(balls[SID_MAP[sid]["label"]])
            elif SID_MAP[sid]["type"] is "player":
                players[SID_MAP[sid]["label"]] = {
                    "name": SID_MAP[sid]["name"],
                    "team": SID_MAP[sid]["team"],
                    "location": (0, 0, 0),
                    "left": (0, 0, 0),
                    "right": (0, 0, 0),
                    "ball-possession": False,
                    "distance-to-ball": 888888,
                    "challenging-opponent": None
                }


        while count < 3500000:

            line = f.readline()

            count += 1

            words = line.strip().split(",")[0:5]

            # Discard irrelevant sensor data
            if words[0] in NOT_NEEDED_IDS:
                continue

            # Format time from picosends into MM:SS
            tmp_t = (int(words[1]) - INITIAL_TIME) * 1e-12 - APPROXIMATE_START_TIME
            if tmp_t < 0:
                print(words[1])
                continue
            if tmp_t > 1809:
                break

            # Type int for coordinates
            tmp_location = tuple(int(x) for x in words[2:5])

            # When ball data comes in:
            if words[0] in BALL_SIDS:
                if is_out(tmp_location) and balls[SID_MAP[words[0]]["label"]]["ball-in"]:
                    balls[SID_MAP[words[0]]["label"]]["ball-in"] = False
                    # players[balls[SID_MAP[words[0]]["label"]]["player"]]["ball-possession"] = False
                    for p in players: players[p]["ball-possession"] = False
                    balls[SID_MAP[words[0]]["label"]]["player"] = None
                    print("<--------- Ball " + SID_MAP[words[0]]["label"] + " goes out of bounds at " + display_seconds_as_minutes(tmp_t))
                    continue
                elif not is_out(tmp_location):
                    balls[SID_MAP[words[0]]["label"]]["location"] = tmp_location
                    if not balls[SID_MAP[words[0]]["label"]]["ball-in"]:
                        balls[SID_MAP[words[0]]["label"]]["ball-in"] = True
                        print("---------> Ball " + SID_MAP[words[0]]["label"] + " goes into the field at " + display_seconds_as_minutes(tmp_t))

                    # Find the player that is the closest to the ball
                    for p in players:
                        players[p]["distance-to-ball"] = get_distance(players[p]["location"], tmp_location)
                    players_sorted = sorted(players.items(), key=lambda x: x[1]["distance-to-ball"])

                    # If the nearest player has >= 2000mm to the ball then nobody has the ball
                    if players_sorted[0][1]["distance-to-ball"] >= 2000:
                        # If the ball was controlled previously by a player, make the change and output an end output
                        if balls[SID_MAP[words[0]]["label"]]["player"]:
                            assert(players[balls[SID_MAP[words[0]]["label"]]["player"]]["ball-possession"])
                            players[balls[SID_MAP[words[0]]["label"]]["player"]]["ball-possession"] = False
                            print(",".join([balls[SID_MAP[words[0]]["label"]]["player"], "touch", SID_MAP[words[0]]["label"], "end", display_seconds_as_minutes(tmp_t)]))
                            balls[SID_MAP[words[0]]["label"]]["player"] = None
                        # If the ball was NOT controlled previously by a player, do nothing

                    # If the nearest player has < 2000mm to the ball then he has the ball
                    if players_sorted[0][1]["distance-to-ball"] < 2000:
                        # If the ball was controlled by no one
                        if not balls[SID_MAP[words[0]]["label"]]["player"]:
                            balls[SID_MAP[words[0]]["label"]]["player"] = players_sorted[0][0]
                            players[players_sorted[0][0]]["ball-possession"] = True
                            print(",".join([balls[SID_MAP[words[0]]["label"]]["player"], "touch", SID_MAP[words[0]]["label"], "start", display_seconds_as_minutes(tmp_t)]))
                        # Else, if the ball was controlled by someone different
                        elif balls[SID_MAP[words[0]]["label"]]["player"] != players_sorted[0][0]:
                            print(",".join([balls[SID_MAP[words[0]]["label"]]["player"], "touch", SID_MAP[words[0]]["label"], "end", display_seconds_as_minutes(tmp_t)]))
                            balls[SID_MAP[words[0]]["label"]]["player"] = players_sorted[0][0]
                            players[balls[SID_MAP[words[0]]["label"]]["player"]]["ball-possession"] = False
                            players[players_sorted[0][0]]["ball-possession"] = True
                            print(",".join([balls[SID_MAP[words[0]]["label"]]["player"], "touch", SID_MAP[words[0]]["label"], "start", display_seconds_as_minutes(tmp_t)]))
                        # Else, if the ball was controlled by same player, do nothing
                        elif balls[SID_MAP[words[0]]["label"]]["player"] == players_sorted[0][0]:
                            pass

            # When player data comes in:
            else:
                this_player = SID_MAP[words[0]]["label"]
                # Update player location
                players[this_player][SID_MAP[words[0]]["leg"]] = tmp_location
                players[this_player]["location"] = get_average(players[this_player]["left"], players[this_player]["right"])
                # Check if player challenges an opponent
                # Find the opponent that is the closest to the player
                nearest_opponent = None
                nearest_distance = 888888
                distance = 888888
                for p in players:
                    if players[p]["team"] != players[this_player]["team"]:
                        distance = get_distance(players[p]["location"], players[this_player]["location"])
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_opponent = p
                # If the distance is close, then they are challengeing
                if nearest_distance < 750:
                    # If this player is not challenging previously, then add them
                    if not players[this_player]["challenging-opponent"]:
                        players[this_player]["challenging-opponent"] = nearest_opponent
                        players[nearest_opponent]["challenging-opponent"] = this_player
                        print(nearest_distance)
                        print(",".join([this_player, "challenges", nearest_opponent, "start", display_seconds_as_minutes(tmp_t)]))
                    # Else, if this player is challenging a different player previously, we switch
                    elif players[SID_MAP[words[0]]["label"]]["challenging-opponent"] != nearest_opponent:
                        print(nearest_distance)
                        print(",".join([this_player, "challenges", players[this_player]["challenging-opponent"], "end", display_seconds_as_minutes(tmp_t)]))
                        players[this_player]["challenging-opponent"] = nearest_opponent
                        players[nearest_opponent]["challenging-opponent"] = this_player
                        print(",".join([this_player, "challenges", nearest_opponent, "start", display_seconds_as_minutes(tmp_t)]))
                    # Else, if this player is challenging the same player, do nothing
                    else:
                        pass
                # Else, if the distance is not close enough:
                else:
                    # If the player was challenging someone previously, remove that previous opponnent
                    if players[this_player]["challenging-opponent"]:
                        print(nearest_distance)
                        print(",".join([this_player, "challenges", players[this_player]["challenging-opponent"], "end", display_seconds_as_minutes(tmp_t)]))
                        players[players[this_player]["challenging-opponent"]]["challenging-opponent"] = None
                        players[SID_MAP[words[0]]["label"]]["challenging-opponent"] = None
                    # If the player was not challenging someone previously, do nothing


        print("Total computation time elapsed: " + str(time.time() - t) + " seconds")


            # sorted(d.items(), key=lambda x: x[1])[0][1]
if __name__ == "__main__":
    main()