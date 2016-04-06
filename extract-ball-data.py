__author__ = 'Hao'

import argparse
import time

INITIAL_TIME = 10629342490369879

def toSID(x):
    return "SID" + "0"*(3-len(x)) + x

def main():

    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='INPUT', help='input file')
    args = parser.parse_args()

    with open(args.input, "r") as f:
        count = 0
        for line in f:
            words = line.strip().split(",")
            if words[0] == "4":
             # or line[0:2] == "8," or line[0:3] == "10,":
                # print(line[0:2])
                words[0] = toSID(words[0])
                words[1] = (int(words[1]) - INITIAL_TIME)*1e-12
                print(words)
                # print(line, end="")
            count += 1    
            if ++count > 2000000:
                break


if __name__ == "__main__":
    main()