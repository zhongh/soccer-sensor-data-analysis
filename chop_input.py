__author__ = 'Hao'

import sys

# TO RUN: python3 chop_input.py

# From my analysis
FIRST_HALF_PAPER_START = 10753295594424116
FIRST_HALF_VIDEO_START = 10749277974056600
FIRST_HALF_PAPER_STOP = 12557295594424116
SECOND_HALF_PAPER_START = 13086639146403495
SECOND_HALF_VIDEO_START = 13085193764021900
SECOND_HALF_PAPER_STOP = 14879639146403495

# Game sections and timestamps:
GAME_SECTIONS = [
    {"index": 1, "label": "1st", "start": min(FIRST_HALF_PAPER_START, FIRST_HALF_VIDEO_START), "stop": FIRST_HALF_PAPER_STOP},
    {"index": 2, "label": "2nd", "start": min(SECOND_HALF_PAPER_START, SECOND_HALF_VIDEO_START), "stop": SECOND_HALF_PAPER_STOP}
]

def main():

    game_sections_count = 0
    game_sections_count_max = len(GAME_SECTIONS) - 1
    output_file = open("full-game-" + GAME_SECTIONS[game_sections_count]["label"], "w+")
    sys.stdout = output_file
    start = GAME_SECTIONS[game_sections_count]["start"]
    stop = GAME_SECTIONS[game_sections_count]["stop"]

    # Open input file
    with open("full-game", "r") as f:

        for line in f:
            words = line.strip().split(",")[0:5]
            if int(words[1]) < start:
                continue
            elif int(words[1]) > stop:
                output_file.close()
                if game_sections_count < game_sections_count_max:
                    game_sections_count += 1
                    output_file = open("full-game-" + GAME_SECTIONS[game_sections_count]["label"], "w+")
                    sys.stdout = output_file
                    start = GAME_SECTIONS[game_sections_count]["start"]
                    stop = GAME_SECTIONS[game_sections_count]["stop"]
                    continue
                else:
                    break
            else:
                print(line, end="")


if __name__ == "__main__":
    main()
