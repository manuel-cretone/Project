import numpy as np
import math
from statistics import *

def average_value(values):
    average = np.mean(values, dtype=float)
    return average


def max_value(values):
    max = np.max(values)
    return max


def min_value(values):
    min = np.min(values)
    return min

def dataVariance(values):
    var = pvariance(values)
    return var

def standardDev(values):
    stdev = pstdev(values)
    return stdev


def count_occurrences(values, width):
    b = (abs(min_value(values)) + abs(max_value(values)))/width
    array, bins = np.histogram(values, bins=math.ceil(b))
    # print (bins)
    # print(array)
    return array, bins

def fit_distribution(x,y):
    v1,v2 = np.polyfit(x,y,3)
    print(v1)
    print(v2)


def getStatistic(values):
    min = min_value(values)
    max = max_value(values)
    average = average_value(values)
    var = dataVariance(values)
    stdev = standardDev(values)
    # hist, bins = count_occurrences(values, 1.5)
    data = {
        "min": min,
        "max": max,
        "average": average,
        "var": var,
        "stdev": stdev,
        # "hist": hist,
        # "bins": bins
    }
    return data