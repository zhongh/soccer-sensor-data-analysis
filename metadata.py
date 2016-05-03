__author__ = 'Hao'


# REFEREE_IDS = ["105", "106"]
# GLOVE_IDS = ["97", "98", "99", "100"]
# BALL_SIDS = ["4", "8", "10", "12"]
# NOT_NEEDED_IDS = REFEREE_IDS + GLOVE_IDS

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
    "97": {"type": "glove", "team": "A", "label": "goalkeeper_A_left_glove", "name": "Nick Gertje", "arm": "left"},
    "98": {"type": "glove", "team": "A", "label": "goalkeeper_A_right_glove", "name": "Nick Gertje", "arm": "right"},
    "13": {"type": "player", "team": "A", "label": "goalkeeper_A", "name": "Nick Gertje", "leg": "left"},
    "14": {"type": "player", "team": "A", "label": "goalkeeper_A", "name": "Nick Gertje", "leg": "right"},
    "47": {"type": "player", "team": "A", "label": "player_A1", "name": "Dennis Dotterweich", "leg": "left"},
    "16": {"type": "player", "team": "A", "label": "player_A1", "name": "Dennis Dotterweich", "leg": "right"},
    "49": {"type": "player", "team": "A", "label": "player_A2", "name": "Niklas Waelzlein", "leg": "left"},
    "88": {"type": "player", "team": "A", "label": "player_A2", "name": "Niklas Waelzlein", "leg": "right"},
    "19": {"type": "player", "team": "A", "label": "player_A3", "name": "Wili Sommer", "leg": "left"},
    "52": {"type": "player", "team": "A", "label": "player_A3", "name": "Wili Sommer", "leg": "right"},
    "53": {"type": "player", "team": "A", "label": "player_A4", "name": "Philipp Harlass", "leg": "left"},
    "54": {"type": "player", "team": "A", "label": "player_A4", "name": "Philipp Harlass", "leg": "right"},
    "23": {"type": "player", "team": "A", "label": "player_A5", "name": "Roman Hartleb", "leg": "left"},
    "24": {"type": "player", "team": "A", "label": "player_A5", "name": "Roman Hartleb", "leg": "right"},
    "57": {"type": "player", "team": "A", "label": "player_A6", "name": "Erik Engelhardt", "leg": "left"},
    "58": {"type": "player", "team": "A", "label": "player_A6", "name": "Erik Engelhardt", "leg": "right"},
    "59": {"type": "player", "team": "A", "label": "player_A7", "name": "Sandro Schneider", "leg": "left"},
    "28": {"type": "player", "team": "A", "label": "player_A7", "name": "Sandro Schneider", "leg": "right"},
    # Team B:
    "99": {"type": "glove", "team": "B", "label": "goalkeeper_B_left_glove", "name": "Leon Krapf", "arm": "left"},
    "100": {"type": "glove", "team": "B", "label": "goalkeeper_B_right_glove", "name": "Leon Krapf", "arm": "right"},
    "61": {"type": "player", "team": "B", "label": "goalkeeper_B", "name": "Leon Krapf", "leg": "left"},
    "62": {"type": "player", "team": "B", "label": "goalkeeper_B", "name": "Leon Krapf", "leg": "right"},
    "63": {"type": "player", "team": "B", "label": "player_B1", "name": "Kevin Baer", "leg": "left"},
    "64": {"type": "player", "team": "B", "label": "player_B1", "name": "Kevin Baer", "leg": "right"},
    "65": {"type": "player", "team": "B", "label": "player_B2", "name": "Luca Ziegler", "leg": "left"},
    "66": {"type": "player", "team": "B", "label": "player_B2", "name": "Luca Ziegler", "leg": "right"},
    "67": {"type": "player", "team": "B", "label": "player_B3", "name": "Ben Mueller", "leg": "left"},
    "68": {"type": "player", "team": "B", "label": "player_B3", "name": "Ben Mueller", "leg": "right"},
    "69": {"type": "player", "team": "B", "label": "player_B4", "name": "Vale Reitstetter", "leg": "left"},
    "38": {"type": "player", "team": "B", "label": "player_B4", "name": "Vale Reitstetter", "leg": "right"},
    "71": {"type": "player", "team": "B", "label": "player_B5", "name": "Christopher Lee", "leg": "left"},
    "40": {"type": "player", "team": "B", "label": "player_B5", "name": "Christopher Lee", "leg": "right"},
    "73": {"type": "player", "team": "B", "label": "player_B6", "name": "Leon Heinze", "leg": "left"},
    "74": {"type": "player", "team": "B", "label": "player_B6", "name": "Leon Heinze", "leg": "right"},
    "75": {"type": "player", "team": "B", "label": "player_B7", "name": "Leo Langhans", "leg": "left"},
    "44": {"type": "player", "team": "B", "label": "player_B7", "name": "Leo Langhans", "leg": "right"}
}


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
HALF_LINE = 0
HALF_LENGTH = (Y_MAX - Y_MIN) / 2