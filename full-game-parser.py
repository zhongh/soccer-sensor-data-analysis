__author__ = 'Hao'

import argparse
import time
from math import *

from helpers import *
from metadata import *


# Ontology prefixes and abbreviations
PREFIX_SO = ""
PREFIX_LITERATE = ""
PREFIX_COLON = ":"
RDF_TYPE = "a"


# Initial conditions:
FIRST_HALF_START_TIMESTAMP = 10749277974056600
BALL_CONTROL_DISTANCE = 500
# Team B is the red team and team A is the yellow team
GOAL_LINE_A = Y_MIN
GOAL_LINE_B = Y_MAX


def main():

    t = time.time()

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT', help='input file')
    args = parser.parse_args()

    # Open input file
    with open(args.input, "r") as f:

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
            "A": {"label": "TeamA", "opponent": "B", "is-attacking": None, "second-last-player": None, "goal-line": Y_MIN, "sign": +1, "own-half-min": Y_MIN, "own-half-max": HALF_LINE},
            "B": {"label": "TeamB", "opponent": "A", "is-attacking": None, "second-last-player": None, "goal-line": Y_MAX, "sign": -1, "own-half-min": HALF_LINE, "own-half-max": Y_MAX}
        }


        game_status = False


        for line in f:

            words = line.strip().split(",")[0:5]

            timestamp_raw = int(words[1]) - FIRST_HALF_START_TIMESTAMP
            timestamp_raw_str = str(timestamp_raw)

            # Format time from picosends into MM:SS
            timestamp_float = round(timestamp_raw * 1e-12, 4)
            timestamp_float_str = str(timestamp_float)

            tmp_t = timestamp_float
            tmp_t_str = display_seconds_as_minutes(tmp_t)

            # Start and termination time
            if tmp_t < 1384:
                continue
            elif tmp_t > 1389.8:
                break

            # Type int for coordinates
            tmp_location = tuple(int(x) for x in words[2:5])

            # Sensor bearer type
            tmp_type = SID_MAP[words[0]]["type"]

            # When ball data comes in:
            if tmp_type == "ball":

                this_ball = SID_MAP[words[0]]["label"]

                balls[this_ball]["position"] = this_ball + "position" + timestamp_raw_str


                # If the ball is OUT
                if is_out(tmp_location):

                    #########################################
                    # Print ball position output
                    #
                    print_results_new(PREFIX_SO + this_ball, PREFIX_SO + "hasPosition", PREFIX_SO + balls[this_ball]["position"], timestamp_float_str, tmp_t_str)
                    print_results_new(PREFIX_SO + this_ball, RDF_TYPE, PREFIX_SO + "BackupBall", timestamp_float_str, tmp_t_str)
                    #########################################

                    game_status = False or is_out(tmp_location)

                    # Update the ball location
                    balls[this_ball]["location"] = tmp_location

                    # If the ball was IN
                    if balls[this_ball]["ball-in"]:
                        # Update ball status
                        balls[this_ball]["ball-in"] = False
                        #print("\n<<<<<<<<<<<< " + this_ball + " goes out of bounds at " + tmp_t_str + "\n")

                        # Also set corresponding player and ball status to False or None, and print out end statements!!! ball-player, player-player, and offsides

                        # Ball-Player:
                        # If the ball was controlled previously by a player, make the change
                        if balls[this_ball]["player"]:
                            assert(players[balls[this_ball]["player"]]["ball-possession"])
                            players[balls[this_ball]["player"]]["ball-possession"] = False
                            balls[this_ball]["player"] = None

                    # Else, the ball was OUT, too, do nothing and continue
                    else:
                        continue

                # If the ball is IN
                else:

                    game_status = True

                    #########################################
                    # Print ball position output
                    print_results_new(PREFIX_SO + this_ball, PREFIX_SO + "hasPosition", PREFIX_SO + balls[this_ball]["position"], timestamp_float_str, tmp_t_str)
                    print_results_new(PREFIX_SO + this_ball, RDF_TYPE, PREFIX_SO + "InFieldBall", timestamp_float_str, tmp_t_str)
                    #########################################

                    # Update the ball location
                    balls[this_ball]["location"] = tmp_location

                    # If the ball was OUT
                    if not balls[this_ball]["ball-in"]:
                        balls[this_ball]["ball-in"] = True
                        #print("\n>>>>>>>>>>>>>> " + this_ball + " goes into the field at " + tmp_t_str + "\n")
                    # Else, the ball was IN, do nothing


                    # Identify ball-player interference:

                    # Update each players distance to ball:
                    for p in players:
                        # players[p]["distance-to-ball"] = get_distance(players[p]["location"], tmp_location)
                        players[p]["distance-to-ball"] = min(get_distance(players[p]["left"], tmp_location), get_distance(players[p]["left"], tmp_location))

                    # Find the player that is the closest to the ball
                    players_sorted = sorted(players.items(), key=lambda x: x[1]["distance-to-ball"])
                    nearest_player = players_sorted[0][0]
                    nearest_distance = players_sorted[0][1]["distance-to-ball"]

                    # If the nearest player has >= 1000mm to the ball then nobody has the ball
                    if nearest_distance >= BALL_CONTROL_DISTANCE:
                        balls[this_ball]["player"] = None

                    # If the nearest player has < 1000mm to the ball then he has the ball
                    if nearest_distance < BALL_CONTROL_DISTANCE:
                        balls[this_ball]["player"] = nearest_player
                        players[nearest_player]["ball-possession"] = True

                        ###############################################
                        # Annotate ball touch
                        #
                        print_results_new(PREFIX_SO + balls[this_ball]["player"], PREFIX_SO + "touches", PREFIX_SO + this_ball, timestamp_float_str, tmp_t_str)
                        ###############################################

                        # Calculate player isNearerToGoalline than properties

                        this_team = players[nearest_player]["team"]
                        opponent = teams[this_team]["opponent"]
                        opponent_goal_line = teams[opponent]["goal-line"]
                        opponent_goal_line_sign = teams[opponent]["sign"]

                        if teams[opponent]["second-last-player"] == None:
                            continue
                        else:
                            second_last_opponent = teams[opponent]["second-last-player"]


                        ###############################################
                        # Annotate second last player of the opponents
                        #
                        print_results_new(PREFIX_SO + second_last_opponent, RDF_TYPE, PREFIX_SO + "SecondLastPlayer", timestamp_float_str,  tmp_t_str)
                        ##############################################

                        distance_of_second_last_defender_to_opponent_goal_line = min(abs(players[second_last_opponent]["left"][1] - opponent_goal_line), abs(players[second_last_opponent]["right"][1] - opponent_goal_line))
                        distance_of_ball_to_opponent_goal_line = abs(tmp_location[1] - opponent_goal_line)

                        for this_player in {k:v for (k,v) in players.items() if v["team"] == this_team}:
                            distance_to_opponent_goal_line = min(abs(players[this_player]["left"][1] - opponent_goal_line), abs(players[this_player]["right"][1] - opponent_goal_line))

                            if distance_to_opponent_goal_line < HALF_LENGTH and distance_to_opponent_goal_line < distance_of_second_last_defender_to_opponent_goal_line and distance_to_opponent_goal_line < distance_of_ball_to_opponent_goal_line:
                                    players[this_player]["in-offside-position"] = True
                            else:
                                    players[this_player]["in-offside-position"] = False

                            ###############################################
                            # Annotate isNearer than
                            #
                            if distance_to_opponent_goal_line < distance_of_second_last_defender_to_opponent_goal_line:
                                print_results_new(PREFIX_SO + this_player, PREFIX_SO + "isNearerToDefenderGoalLineThan", PREFIX_SO + second_last_opponent, timestamp_float_str, tmp_t_str)
                            if distance_to_opponent_goal_line < distance_of_ball_to_opponent_goal_line:
                                print_results_new(PREFIX_SO + this_player, PREFIX_SO + "isNearerToDefenderGoalLineThan", PREFIX_SO + this_ball, timestamp_float_str, tmp_t_str)
                            ###############################################


            # When player data comes in:
            elif tmp_type == "player":

                # Turn this back on when making sure end statements are printed when ball goes out of bounds
                # if game_status == False:
                #     continue

                this_player = SID_MAP[words[0]]["label"]
                this_leg = SID_MAP[words[0]]["leg"]
                this_team = SID_MAP[words[0]]["team"]

                players[this_player]["position"] = this_player + "Position" + timestamp_raw_str

                ###############################################
                # annotate player hasPosition triple
                #
                print_results_new(PREFIX_SO + this_player, PREFIX_SO + "hasPosition", PREFIX_SO + players[this_player]["position"], timestamp_float_str, tmp_t_str)
                if not game_status:
                    print_results_new(PREFIX_SO + players[this_player]["position"], RDF_TYPE, PREFIX_LITERATE + "OffsideIrreleventPosition", timestamp_float_str, tmp_t_str)
                ###############################################

                # Update player location
                players[this_player][this_leg] = tmp_location
                players[this_player]["location"] = get_average(players[this_player]["left"], players[this_player]["right"])

                ###############################################
                # Annotate player in own half
                #
                if players[this_player]["location"][1] > teams[this_team]["own-half-min"] and players[this_player]["location"][1] < teams[this_team]["own-half-max"]:
                    print_results_new(PREFIX_SO + this_player, RDF_TYPE, PREFIX_SO + "PlayerInOwnHalf", timestamp_float_str, tmp_t_str)
                else:
                    print_results_new(PREFIX_SO + this_player, RDF_TYPE, PREFIX_SO + "PlayerNotInOwnHalf", timestamp_float_str, tmp_t_str)
                ###############################################


                # Compute second last player of the team
                second_last_player = sorted([(k, v) for (k, v) in players.items() if v["team"] == this_team], key=lambda p: min(abs(p[1]["left"][1] - teams[this_team]["goal-line"]), abs(p[1]["right"][1] - teams[this_team]["goal-line"])))[1][0]
                teams[this_team]["second-last-player"] = second_last_player


                # ###############################################
                # # Annotate second last player of his team, regardless ball in or out (if game_status:)
                # # **(Now we try to annotate this at every ball touch, not when player sensors update)
                # #
                # for teammate in [(k, v) for (k, v) in players.items() if v["team"] == this_team]:
                #     if teammate[0] == second_last_player:
                #         print_results_new(PREFIX_SO + teammate[0], RDF_TYPE, PREFIX_SO + "SecondLastPlayer", timestamp_float_str,  tmp_t_str)
                #     # else:
                #     #    print_results_new(PREFIX_SO + teammate[0], RDF_TYPE, PREFIX_SO + "NotSecondLastPlayer", timestamp_float_str,  tmp_t_str)
                # ##############################################


                # Compute if player challenges an opponent

                # A player must not challenge an opponent when the game is off or when he has ball possession:
                if game_status and (not players[this_player]["ball-possession"]):

                    # Compute the opponent that is the closest to the player
                    nearest_opponent = None
                    nearest_distance = 888888
                    for p in {k:v for (k,v) in players.items() if v["team"] != this_team}:
                        distance = get_distance(players[p]["location"], players[this_player]["location"])
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_opponent = p

                    # If the distance is close, then they are challengeing
                    if nearest_distance < 1500:
                        players[this_player]["challenging-opponent"] = nearest_opponent

                        ###############################################
                        # Annotate player challenge
                        #
                        print_results_new(PREFIX_SO + this_player, PREFIX_SO + "isInvolvedIn", PREFIX_SO + "opponent_challenge", timestamp_float_str, tmp_t_str)
                        if not players[nearest_opponent]["ball-possession"]:
                            players[nearest_opponent]["challenging-opponent"] = this_player
                            print_results_new(PREFIX_SO + nearest_opponent, PREFIX_SO + "isInvolvedIn", PREFIX_SO + "opponent_challenge", timestamp_float_str, tmp_t_str)
                        ###############################################

                    # Else, the distance is not close enough:
                    else:
                        # If the player was challenging someone previously, remove that previous opponnent
                        if players[this_player]["challenging-opponent"]:
                            players[players[this_player]["challenging-opponent"]]["challenging-opponent"] = None
                            players[this_player]["challenging-opponent"] = None




            elif tmp_type == "referee":
                # Update referee location
                this_referee = SID_MAP[words[0]]["label"]
                this_leg = SID_MAP[words[0]]["leg"]
                referees[this_referee][this_leg] = tmp_location
                referees[this_referee]["location"] = get_average(referees[this_referee]["left"], referees[this_referee]["right"])
                referees[this_referee]["position"] = this_referee + "position" + timestamp_raw_str
                ###############################################
                # and print
                print_results_new(PREFIX_SO + this_referee, PREFIX_SO + "hasPosition", PREFIX_SO + referees[this_referee]["position"], timestamp_float_str, tmp_t_str)
                ###############################################


            elif tmp_type == "glove":
                # Update glove position
                this_glove = SID_MAP[words[0]]["label"]
                gloves[this_glove]["location"] = tmp_location
                gloves[this_glove]["position"] = this_glove + "position" + timestamp_raw_str
                ###############################################
                # and print
                print_results_new(PREFIX_SO + this_glove, PREFIX_SO + "hasPosition", PREFIX_SO + gloves[this_glove]["position"], timestamp_float_str, tmp_t_str)
                #print_results_new(PREFIX_SO + gloves[this_glove]["position"], RDF_TYPE, PREFIX_LITERATE + "GlovePosition", timestamp_float_str, tmp_t_str)
                ###############################################

            else:
                exit(tmp_type)


        #print("Total computation time elapsed: " + str(time.time() - t) + " seconds")


if __name__ == "__main__":
    main()
