__author__ = 'Hao'


from math import *



def display_seconds_as_minutes(t):
    return str(floor(t / 60)) + ":" + str(round(t % 60, 4))


def print_results(s, p, o, b, t):
    print(",".join([":" + s, ":" + p, ":" + o, b, t]))