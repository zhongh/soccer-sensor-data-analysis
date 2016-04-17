__author__ = 'Hao'

import argparse
import time
from math import *
from helpers import *

#######################################
# Ontology variables

PREFIX_SO = "SO:"
PREFIX_LITERATE = "SOL:"
PREFIX_COLON = ":"
RDFS_TYPE = "rdfs:type"

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
    # Referee:
    "105": {"type": "referee", "label": "referee", "leg": "left"},
    "106": {"type": "referee", "label": "referee", "leg": "right"},
    # Balls:
    "4":  {"type": "ball", "label": "ball4"},
    "8":  {"type": "ball", "label": "ball8"},
    "10": {"type": "ball", "label": "ball10"},
    "12": {"type": "ball", "label": "ball12"},
    # Team A:
    "97": {"type": "glove", "team": "A", "label": "goalkeeperAleftglove", "name": "Nick Gertje", "arm": "left"},
    "98": {"type": "glove", "team": "A", "label": "goalkeeperArightglove", "name": "Nick Gertje", "arm": "right"},
    "13": {"type": "player", "team": "A", "label": "GoalkeeperA", "name": "Nick Gertje", "leg": "left"},
    "14": {"type": "player", "team": "A", "label": "GoalkeeperA", "name": "Nick Gertje", "leg": "right"},
    "47": {"type": "player", "team": "A", "label": "PlayerA1", "name": "Dennis Dotterweich", "leg": "left"},
    "16": {"type": "player", "team": "A", "label": "PlayerA1", "name": "Dennis Dotterweich", "leg": "right"},
    "49": {"type": "player", "team": "A", "label": "PlayerA2", "name": "Niklas Waelzlein", "leg": "left"},
    "88": {"type": "player", "team": "A", "label": "PlayerA2", "name": "Niklas Waelzlein", "leg": "right"},
    "19": {"type": "player", "team": "A", "label": "PlayerA3", "name": "Wili Sommer", "leg": "left"},
    "52": {"type": "player", "team": "A", "label": "PlayerA3", "name": "Wili Sommer", "leg": "right"},
    "53": {"type": "player", "team": "A", "label": "PlayerA4", "name": "Philipp Harlass", "leg": "left"},
    "54": {"type": "player", "team": "A", "label": "PlayerA4", "name": "Philipp Harlass", "leg": "right"},
    "23": {"type": "player", "team": "A", "label": "PlayerA5", "name": "Roman Hartleb", "leg": "left"},
    "24": {"type": "player", "team": "A", "label": "PlayerA5", "name": "Roman Hartleb", "leg": "right"},
    "57": {"type": "player", "team": "A", "label": "PlayerA6", "name": "Erik Engelhardt", "leg": "left"},
    "58": {"type": "player", "team": "A", "label": "PlayerA6", "name": "Erik Engelhardt", "leg": "right"},
    "59": {"type": "player", "team": "A", "label": "PlayerA7", "name": "Sandro Schneider", "leg": "left"},
    "28": {"type": "player", "team": "A", "label": "PlayerA7", "name": "Sandro Schneider", "leg": "right"},
    # Team B:
    "99": {"type": "glove", "team": "B", "label": "goalkeeperBleftglove", "name": "Leon Krapf", "arm": "left"},
    "100": {"type": "glove", "team": "B", "label": "goalkeeperBrightglove", "name": "Leon Krapf", "arm": "right"},
    "61": {"type": "player", "team": "B", "label": "GoalkeeperB", "name": "Leon Krapf", "leg": "left"},
    "62": {"type": "player", "team": "B", "label": "GoalkeeperB", "name": "Leon Krapf", "leg": "right"},
    "63": {"type": "player", "team": "B", "label": "GoalkeeperB", "name": "Kevin Baer", "leg": "left"},
    "64": {"type": "player", "team": "B", "label": "PlayerB1", "name": "Kevin Baer", "leg": "right"},
    "65": {"type": "player", "team": "B", "label": "PlayerB2", "name": "Luca Ziegler", "leg": "left"},
    "66": {"type": "player", "team": "B", "label": "PlayerB2", "name": "Luca Ziegler", "leg": "right"},
    "67": {"type": "player", "team": "B", "label": "PlayerB3", "name": "Ben Mueller", "leg": "left"},
    "68": {"type": "player", "team": "B", "label": "PlayerB3", "name": "Ben Mueller", "leg": "right"},
    "69": {"type": "player", "team": "B", "label": "PlayerB4", "name": "Vale Reitstetter", "leg": "left"},
    "38": {"type": "player", "team": "B", "label": "PlayerB4", "name": "Vale Reitstetter", "leg": "right"},
    "71": {"type": "player", "team": "B", "label": "PlayerB5", "name": "Christopher Lee", "leg": "left"},
    "40": {"type": "player", "team": "B", "label": "PlayerB5", "name": "Christopher Lee", "leg": "right"},
    "73": {"type": "player", "team": "B", "label": "PlayerB6", "name": "Leon Heinze", "leg": "left"},
    "74": {"type": "player", "team": "B", "label": "PlayerB6", "name": "Leon Heinze", "leg": "right"},
    "75": {"type": "player", "team": "B", "label": "PlayerB7", "name": "Leo Langhans", "leg": "left"},
    "44": {"type": "player", "team": "B", "label": "PlayerB7", "name": "Leo Langhans", "leg": "right"}
}

#######################################
# Initial conditions

INITIAL_TIME = 10629342490369879
APPROXIMATE_START_TIME = 119

BALL_CONTROL_DISTANCE = 2000

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
HALF_LENGTH = (Y_MAX - Y_MIN) / 2

# Team B is the red team and team A is the yellow team
GOAL_LINE_A = Y_MIN
GOAL_LINE_B = Y_MAX

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

        # Keep track of ball, player informations
        balls = {}
        players = {}
        teams = {}
        referees = {}
        gloves = {}

        # Setting up players, balls and referees
        for sid in SID_MAP:
            if SID_MAP[sid]["type"] is "ball":
                balls[SID_MAP[sid]["label"]] = {
                    "location": (0, 0, 0),
                    "ball-in": False,
                    "player": None,
                    "position": None
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
                    "challenging-opponent": None,
                    "position": None,
                    "in-offside-position": False
                }
            elif SID_MAP[sid]["type"] is "referee":
                referees[SID_MAP[sid]["label"]] = {
                    "label": "referee",
                    "location": (0, 0, 0),
                    "left": (0, 0, 0),
                    "right": (0, 0, 0),
                    "position": None
                }
            elif SID_MAP[sid]["type"] is "glove":
                gloves[SID_MAP[sid]["label"]] = {
                    "label": SID_MAP[sid]["label"],
                    "team": SID_MAP[sid]["team"],
                    "location": (0, 0, 0),
                    "position": None
                }

        # Setting up teams
        teams = {
            "A": {"label": "TeamA", "opponent": "B", "is-attacking": None, "second-last-player": None, "goal-line": Y_MIN, "sign": +1},
            "B": {"label": "TeamB", "opponent": "A", "is-attacking": None, "second-last-player": None, "goal-line": Y_MAX, "sign": -1}
        }


        game_status = False

        for line in f:

            count += 1

            words = line.strip().split(",")[0:5]

            # # Discard irrelevant sensor data
            # if words[0] in NOT_NEEDED_IDS:
            #     continue

            # Format time from picosends into MM:SS
            tmp_ts = int(words[1]) - INITIAL_TIME
            tmp_ts_str = str(tmp_ts)

            tmp_t = tmp_ts * 1e-12 - APPROXIMATE_START_TIME
            tmp_t_str = display_seconds_as_minutes(tmp_t)
            if tmp_t < 0:
                print(words[1])
                continue
            if tmp_t > 2:
                break
            if tmp_t > 1809:
                break

            # Type int for coordinates
            tmp_location = tuple(int(x) for x in words[2:5])

            # Sensor bearer type
            tmp_type = SID_MAP[words[0]]["type"]

            # When ball data comes in:
            if tmp_type == "ball":

                this_ball = SID_MAP[words[0]]["label"]

                balls[this_ball]["position"] = this_ball + "position" + tmp_ts_str
                #### print_results(this_ball, "hasPosition", balls[this_ball]["position"], "begin", tmp_t_str)


                # If the ball is OUT
                if is_out(tmp_location):

                    game_status = False

                    #########################################
                    # Print ball position output
                    # print_results_new(PREFIX_SO + this_ball, PREFIX_SO + "hasPosition", PREFIX_SO + balls[this_ball]["position"], "begin", tmp_ts_str, tmp_t_str)
                    # print_results_new(PREFIX_SO + this_ball, RDFS_TYPE, PREFIX_SO + "BackupBall", "begin", tmp_ts_str, tmp_t_str)
                    #########################################

                    # If the ball was IN
                    if balls[this_ball]["ball-in"]:
                        # Update ball status
                        balls[this_ball]["ball-in"] = False
                        print("\n<<<<<<<<<<<< " + this_ball + " goes out of bounds at " + tmp_t_str + "\n")

                        # Also set corresponding player and ball status to False or None, and print out end statements!!! ball-player, player-player, and offsides

                        # Ball-Player:
                        # If the ball was controlled previously by a player, make the change and output an end statement
                        if balls[this_ball]["player"]:
                            assert(players[balls[this_ball]["player"]]["ball-possession"])

                            print_results(balls[this_ball]["player"], "touches", this_ball, "end", tmp_t_str)
                            print_results(balls[this_ball]["player"], "hasPosition", players[balls[this_ball]["player"]]["position"], "end", tmp_t_str)
                            ###print_results(this_ball, "hasPosition", balls[this_ball]["position"], "end", tmp_t_str)
                            print_results(balls[this_ball]["player"], "isInvolvedIn", "BallTouch", "end", tmp_t_str)

                            players[balls[this_ball]["player"]]["ball-possession"] = False
                            balls[this_ball]["player"] = None

                        # Player-player
                        for player in players:
                            # If the player was challenging someone previously, remove that previous opponnent and make an end statement
                            if players[player]["challenging-opponent"]:
                                print_results(player, "challeges", players[player]["challenging-opponent"], "end", tmp_t_str)
                                players[players[player]["challenging-opponent"]]["challenging-opponent"] = None
                                players[player]["challenging-opponent"] = None


                        # Second last player
                        for team in teams:
                            if teams[team]["second-last-player"] != None:

                                print_results(teams[team]["second-last-player"], "rdf:type", "SecondLastPlayer", "end", tmp_t_str)
                                print_results(teams[team]["second-last-player"], "hasPosition", players[teams[team]["second-last-player"]]["position"], "end", tmp_t_str)

                                teams[team]["second-last-player"] = None

                        continue
                    # Else, the ball was OUT, too, do nothing and continue
                    else:
                        continue

                # If the ball is IN
                else:

                    game_status = True

                    #########################################
                    # Print ball position output
                    # print_results_new(PREFIX_SO + this_ball, PREFIX_SO + "hasPosition", PREFIX_SO + balls[this_ball]["position"], "begin", tmp_ts_str, tmp_t_str)
                    # print_results_new(PREFIX_SO + this_ball, RDFS_TYPE, PREFIX_SO + "InFieldBall", "begin", tmp_ts_str, tmp_t_str)
                    #########################################

                    # Update the ball location
                    balls[this_ball]["location"] = tmp_location

                    # If the ball was OUT
                    if not balls[this_ball]["ball-in"]:
                        balls[this_ball]["ball-in"] = True
                        print("\n>>>>>>>>>>>>>> " + this_ball + " goes into the field at " + tmp_t_str + "\n")
                    # Else, the ball was IN, do nothing



                    ###############################################
                    # Identify ball-player interference:
                    #

                    # Update each players distance to ball:
                    for p in players:
                        players[p]["distance-to-ball"] = get_distance(players[p]["location"], tmp_location)

                    # Find the player that is the closest to the ball
                    players_sorted = sorted(players.items(), key=lambda x: x[1]["distance-to-ball"])
                    nearest_player = players_sorted[0][0]
                    nearest_distance = players_sorted[0][1]["distance-to-ball"]


                    # If the nearest player has >= 2000mm to the ball then nobody has the ball
                    if nearest_distance >= BALL_CONTROL_DISTANCE:
                        # If the ball was controlled previously by a player, make the change and output an end output
                        if balls[this_ball]["player"]:
                            assert(players[balls[this_ball]["player"]]["ball-possession"])

                            print_results(balls[this_ball]["player"], "touches", this_ball, "end", tmp_t_str)
                            print_results(balls[this_ball]["player"], "hasPosition", players[balls[this_ball]["player"]]["position"], "end", tmp_t_str)
                            ###### print_results(this_ball, "hasPosition", balls[this_ball]["position"], "end", tmp_t_str)
                            print_results(balls[this_ball]["player"], "isInvolvedIn", "BallTouch", "end", tmp_t_str)

                            players[balls[this_ball]["player"]]["ball-possession"] = False
                            balls[this_ball]["player"] = None
                        # If the ball was NOT controlled previously by a player, do nothing

                    # If the nearest player has < 2000mm to the ball then he has the ball
                    if nearest_distance < BALL_CONTROL_DISTANCE:
                        # If the ball was controlled by no one
                        if not balls[this_ball]["player"]:
                            balls[this_ball]["player"] = nearest_player
                            players[nearest_player]["ball-possession"] = True

                            print_results(balls[this_ball]["player"], "touches", this_ball, "begin", tmp_t_str)
                            print_results(balls[this_ball]["player"], "hasPosition", players[balls[this_ball]["player"]]["position"], "begin", tmp_t_str)
                            ##### print_results(this_ball, "hasPosition", balls[this_ball]["position"], "begin", tmp_t_str)
                            print_results(balls[this_ball]["player"], "isInvolvedIn", "BallTouch", "begin", tmp_t_str)

                        # Else, if the ball was controlled by someone different
                        elif balls[this_ball]["player"] != nearest_player:

                            print_results(balls[this_ball]["player"], "touches", this_ball, "end", tmp_t_str)
                            print_results(balls[this_ball]["player"], "hasPosition", players[balls[this_ball]["player"]]["position"], "end", tmp_t_str)
                            ##### print_results(this_ball, "hasPosition", balls[this_ball]["position"], "end", tmp_t_str)
                            print_results(balls[this_ball]["player"], "isInvolvedIn", "BallTouch", "end", tmp_t_str)

                            players[balls[this_ball]["player"]]["ball-possession"] = False
                            balls[this_ball]["player"] = nearest_player
                            players[nearest_player]["ball-possession"] = True

                            print_results(balls[this_ball]["player"], "touches", this_ball, "begin", tmp_t_str)
                            print_results(balls[this_ball]["player"], "hasPosition", players[balls[this_ball]["player"]]["position"], "begin", tmp_t_str)
                            ##### print_results(this_ball, "hasPosition", balls[this_ball]["position"], "begin", tmp_t_str)
                            print_results(balls[this_ball]["player"], "isInvolvedIn", "BallTouch", "begin", tmp_t_str)

                        # Else, if the ball was controlled by same player, do nothing
                        elif balls[this_ball]["player"] == nearest_player:
                            pass
                    #
                    #
                    ###############################################


            # When player data comes in:
            elif tmp_type == "player":

                # Turn this back on when making sure end statements are printed when ball goes out of bounds
                # if game_status == False:
                #     continue

                this_player = SID_MAP[words[0]]["label"]
                this_leg = SID_MAP[words[0]]["leg"]
                this_team = SID_MAP[words[0]]["team"]

                players[this_player]["position"] = this_player + "Position" + words[1]

                ###############################################
                # Print player hasPosition triple
                # print_results_new(PREFIX_SO + this_player, PREFIX_SO + "hasPosition", PREFIX_SO + players[this_player]["position"], "begin", tmp_ts_str, tmp_t_str)
                # if not game_status:
                #     print_results_new(PREFIX_SO + players[this_player]["position"], RDFS_TYPE, PREFIX_LITERATE + "OffsideIrreleventPosition", "begin", tmp_ts_str, tmp_t_str)
                ###############################################

                # Update player location
                players[this_player][this_leg] = tmp_location
                players[this_player]["location"] = get_average(players[this_player]["left"], players[this_player]["right"])


                ###############################################
                # Identify second last player of his team
                #

                if game_status:
                    second_last_player = sorted([(k, v) for (k, v) in players.items() if v["team"] == this_team], key=lambda p: (p[1]["location"][1] - teams[this_team]["goal-line"]) * teams[this_team]["sign"])[1][0]
                    if teams[this_team]["second-last-player"] != second_last_player:
                        if teams[this_team]["second-last-player"] != None:
                            print_results(teams[this_team]["second-last-player"], "rdf:type", "SecondLastPlayer", "end", tmp_t_str)
                            print_results(teams[this_team]["second-last-player"], "hasPosition", players[teams[this_team]["second-last-player"]]["position"], "end", tmp_t_str)
                        teams[this_team]["second-last-player"] = second_last_player

                        print_results(teams[this_team]["second-last-player"], "rdf:type", "SecondLastPlayer", "begin", tmp_t_str)
                        print_results(teams[this_team]["second-last-player"], "hasPosition", players[teams[this_team]["second-last-player"]]["position"], "begin", tmp_t_str)

                    else:
                        pass

                ################################################
                # Identify if the player is in offside position

                if game_status:
                    opponent = teams[this_team]["opponent"]
                    distance_to_opponent_goal_line = (players[this_player]["location"][1] - teams[opponent]["goal-line"]) * teams[opponent]["sign"]
                    second_last_opponent = teams[opponent]["second-last-player"]
                    if second_last_opponent == None:
                        continue
                    distance_of_second_last_defender_to_opponent_goal_line = (players[second_last_opponent]["location"][1] - teams[opponent]["goal-line"]) * teams[opponent]["sign"]
                    distance_of_ball_to_opponent_goal_line = ([(k, v) for (k, v) in balls.items() if v["ball-in"]][0][1]["location"][1] - teams[opponent]["goal-line"]) * teams[opponent]["sign"]

                    if distance_to_opponent_goal_line < HALF_LENGTH and distance_to_opponent_goal_line < distance_of_second_last_defender_to_opponent_goal_line and distance_to_opponent_goal_line < distance_of_ball_to_opponent_goal_line:
                        if not players[this_player]["in-offside-position"]:
                            players[this_player]["in-offside-position"] = True
                            print_results(this_player, "hasPosition", players[this_player]["position"], "begin", tmp_t_str)
                            print_results(players[this_player]["position"], "isNearerToDefenderGoalLineThan", players[second_last_opponent]["position"], "begin", tmp_t_str)
                            print_results(players[this_player]["position"], "isNearerToDefenderGoalLineThan", [(k, v) for (k, v) in balls.items() if v["ball-in"]][0][1]["position"], "begin", tmp_t_str)
                        else:
                            pass
                    else:
                        if players[this_player]["in-offside-position"]:
                            players[this_player]["in-offside-position"] = False
                            print_results(this_player, "hasPosition", players[this_player]["position"], "end", tmp_t_str)
                            print_results(players[this_player]["position"], "isNearerToDefenderGoalLineThan", players[second_last_opponent]["position"], "end", tmp_t_str)
                            print_results(players[this_player]["position"], "isNearerToDefenderGoalLineThan", [(k, v) for (k, v) in balls.items() if v["ball-in"]][0][1]["position"], "end", tmp_t_str)
                        else:
                            pass



                ###############################################
                # Check if player challenges an opponent
                #

                # A player must not challenge an opponent when the game is off or when he has ball possession:
                if game_status and (not players[this_player]["ball-possession"]):

                    # Find the opponent that is the closest to the player
                    nearest_opponent = None
                    nearest_distance = 888888
                    distance = 888888
                    for p in {k:v for (k,v) in players.items() if v["team"] != this_team}:
                        # if players[p]["team"] != players[this_player]["team"]:
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
                            print(",".join([":" + this_player, ":challenges", ":" + nearest_opponent, "start", tmp_t_str]))
                        # Else, if this player is challenging a different player previously, we switch
                        elif players[this_player]["challenging-opponent"] != nearest_opponent:
                            print(",".join([":" + this_player, ":challenges", ":" + players[this_player]["challenging-opponent"], "end", tmp_t_str]))
                            players[this_player]["challenging-opponent"] = nearest_opponent
                            players[nearest_opponent]["challenging-opponent"] = this_player
                            print(",".join([":" + this_player, ":challenges", ":" + nearest_opponent, "start", tmp_t_str]))
                        # Else, if this player is challenging the same player, do nothing
                        else:
                            pass
                    # Else, the distance is not close enough:
                    else:
                        # If the player was challenging someone previously, remove that previous opponnent
                        if players[this_player]["challenging-opponent"]:
                            print(",".join([":" + this_player, ":challenges", ":" + players[this_player]["challenging-opponent"], "end", tmp_t_str]))
                            players[players[this_player]["challenging-opponent"]]["challenging-opponent"] = None
                            players[this_player]["challenging-opponent"] = None
                        # If the player was not challenging someone previously, do nothing



            elif tmp_type == "referee":
                # Update referee location
                this_referee = SID_MAP[words[0]]["label"]
                this_leg = SID_MAP[words[0]]["leg"]
                referees[this_referee][this_leg] = tmp_location
                referees[this_referee]["location"] = get_average(referees[this_referee]["left"], referees[this_referee]["right"])
                referees[this_referee]["position"] = this_referee + "position" + tmp_ts_str
                ###############################################
                # and print
                # print_results_new(PREFIX_SO + this_referee, PREFIX_SO + "hasPosition", PREFIX_SO + referees[this_referee]["position"], "begin", tmp_ts_str, tmp_t_str)
                ###############################################


            elif tmp_type == "glove":
                # Update glove position
                this_glove = SID_MAP[words[0]]["label"]
                gloves[this_glove]["location"] = tmp_location
                gloves[this_glove]["position"] = this_glove + "position" + tmp_ts_str
                ###############################################
                # and print
                # print_results_new(PREFIX_SO + this_glove, PREFIX_SO + "hasPosition", PREFIX_SO + gloves[this_glove]["position"], "begin", tmp_ts_str, tmp_t_str)
                # print_results_new(PREFIX_SO + gloves[this_glove]["position"], "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", PREFIX_LITERATE + "GlovePosition", "begin", tmp_ts_str, tmp_t_str)
                ###############################################

            else:
                exit(tmp_type)


        print("Total computation time elapsed: " + str(time.time() - t) + " seconds")


if __name__ == "__main__":
    main()
