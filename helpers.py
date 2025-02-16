__author__ = 'Hao'


from math import *

from metadata import *

def display_seconds_as_minutes(t):
    return str(floor(t / 60)) + ":" + str(round(t % 60, 4))


def print_results_new(s, p, o, b, ts):
    print(",".join([s, p, o, b, ts]))


def get_average(a, b):
    return (
        (a[0] + b[0]) / 2,
        (a[1] + b[1]) / 2,
        (a[2] + b[2]) / 2
    )


def get_distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def is_out(loc):
    return loc[0] < X_MIN or loc[0] > X_MAX or loc[1] < Y_MIN or loc[1] > Y_MAX

