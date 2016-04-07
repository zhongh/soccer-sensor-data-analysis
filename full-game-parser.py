__author__ = 'Hao'

import argparse
import time

PREFIX = "http://tw.rpi.edu/web/Courses/Ontologies/2016/OE_6_Soccer_Offside/"
HAS_SENSOR = "<" + PREFIX + "hasSensor> "
HAS_SAMPLING_TIME = "<" + PREFIX + "hasSamplingTime> "
HAS_X = "<" + PREFIX + "hasX> "
HAS_Y = "<" + PREFIX + "hasY> "
HAS_Z = "<" + PREFIX + "hasZ> "


INITIAL_TIME = 10629342490369879
APPROXIMATE_START_TIME = 119

BALLS = ["4", "8", "10"]

# We suggest to use the following coordinates if you opt for an approximation: (0,33965), (0,-33960),(52483,33965),(52483,-33960)

X_MIN = 0
X_MAX = 52483
Y_MIN = -33960
Y_MAX = 33965

# -33960--------0---y-->---33965
# |             |              |
# |             x              |
# |             |              |
# |             V              |
# |___________52483____________|


def toSID(x):
    return "SID" + "0"*(3-len(x)) + x



def print_list_with_linebreak(list):
    """
    Helper function to print out a list with line breaks for better display
    """
    for x in list:
        print(x)


def parse_line_to_triples(line):
    line = line.split(",")
    triples = []
    record = "<" + PREFIX + "Record1> "
    sensorID = "SID" + line[0]
    sensor = "<" + PREFIX + sensorID + "> "
    samplingTime = '"' + line[1] + '" '
    x = '"' + line[2] + '" '
    y = '"' + line[3] + '" '
    z = '"' + line[4] + '" '
    triples.append(record + HAS_SENSOR + sensor + ".")
    triples.append(sensor + HAS_SAMPLING_TIME + samplingTime + ".")
    triples.append(sensor + HAS_X + x + ".")
    triples.append(sensor + HAS_Y + y + ".")
    triples.append(sensor + HAS_Z + z + ".")
    return triples

def ball_out(x, y):
    return x < X_MIN or x > X_MAX or y < Y_MIN or y > Y_MAX

def main():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT', help='input file')
    args = parser.parse_args()

    with open(args.input, "r") as f:

        count = 0

        balls = {}
        for sid in BALLS:
            balls[sid] = {"ball-in": False, "location": (0, 0, 0)}

        ballIn = False

        for line in f:
            # triples = parse_line_to_triples(line)
            # print_list_with_linebreak(triples)

            words = line.strip().split(",")
            words[1] = (int(words[1]) - INITIAL_TIME)*1e-12 - 119
            if words[1] < 0: 
                continue
            if words[1] > 1809:
                break

            # Balls:
            if words[0] in BALLS:
                words[2] = int(words[2])
                words[3] = int(words[3])
                words[4] = int(words[4])
                if ball_out(words[2], words[3]) and balls[words[0]]["ball-in"] == True:
                    balls[words[0]]["ball-in"] = False
                    # print(words[0:5])
                    print("Ball " + str(words[0]) + " goes out of bounds at " + time.strftime('%M:%S', time.gmtime(words[1])))
                elif not ball_out(words[2], words[3]) and balls[words[0]]["ball-in"] == False:
                    balls[words[0]]["ball-in"] = True       
                    # print(words[0:5])
                    print("Ball " + str(words[0]) + " goes into the field at " + time.strftime('%M:%S', time.gmtime(words[1])))

            count += 1    
            if ++count > 5000000:
                break



if __name__ == "__main__":
    main()