__author__ = 'Hao'

# TO RUN: python3 chop_input.py > full-game-1


START_TIME_STAMP = 10748342427955588
END_TIME_STAMP = None


def main():

    # Open input file
    with open("full-game", "r") as f:
        start_found = False
        for line in f:
            if not start_found:
                words = line.strip().split(",")[0:5]
                if int(words[1]) >= START_TIME_STAMP:
                    start_found = True
                    continue
                else:
                    continue
            else:
                print(line, end="")

if __name__ == "__main__":
    main()
