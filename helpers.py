__author__ = 'Hao'


from math import *

# PREFIX = "http://tw.rpi.edu/web/Courses/Ontologies/2016/OE_6_Soccer_Offside/"
PREFIX = "so:"



def display_seconds_as_minutes(t):
    return str(floor(t / 60)) + ":" + str(round(t % 60, 4))


def print_results(s, p, o, b, t):
    print(",".join([PREFIX + s, PREFIX + p, PREFIX + o, b, t]))


def print_results_new(s, p, o, b, ts):
    print(",".join([s, p, o, b, ts]))