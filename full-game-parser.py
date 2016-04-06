__author__ = 'Hao'

import argparse
import time

PREFIX = "http://tw.rpi.edu/web/Courses/Ontologies/2016/OE_6_Soccer_Offside/"
HAS_SENSOR = "<" + PREFIX + "hasSensor> "
HAS_SAMPLING_TIME = "<" + PREFIX + "hasSamplingTime> "
HAS_X = "<" + PREFIX + "hasX> "
HAS_Y = "<" + PREFIX + "hasY> "
HAS_Z = "<" + PREFIX + "hasZ> "


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



def main():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT', help='input file')
    args = parser.parse_args()

    with open(args.input, "r") as f:
        for line in f:
            triples = parse_line_to_triples(line)
            print_list_with_linebreak(triples)



if __name__ == "__main__":
    main()