# TODO Make interactions possible.
from pycolate.Percolation import Percolation
import numpy as np
from scipy.ndimage import measurements
import scipy.ndimage as ndimage
import itertools
from sympy import solveset, S
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr
from sympy import N, latex

def percolates(config):

    percolated = False

    labeledConfig, num = measurements.label(config)

    sizes = ndimage.sum(config, labeledConfig, range(num + 1))

    sizeConfig = sizes[labeledConfig]

    sizes = sizes[sizes != 0]

    percolatedSize = 0

    labels = np.unique(labeledConfig)

    labelsToCheck = labels[labels != 0]

    leftColumn = labeledConfig[:, 0]

    rightColumn = labeledConfig[:, -1]

    topRow = labeledConfig[0]

    bottomRow = labeledConfig[-1]

    for label in labelsToCheck:

        left = label in leftColumn

        right = label in rightColumn

        bottom = label in bottomRow

        top = label in topRow

        if (left and right) or (bottom and top):

            percolated = True

            break

    return percolated

def majority(config):
    
    if np.sum(config) > (config.size / 2):

        return True
    
    else:

        return False

def coarse_graining_estimate(grain_size, method=percolates):

    if grain_size <= 1 or (type(grain_size) != int):

        raise ValueError('grain_size must be an interger greater then 1.')

    generated_arrays = []
    passed_arrays = []
    amount_of_each = {}

    #There must be a faster way of generating this array?
    p = [
        np.reshape(np.array(i), (grain_size, grain_size))
        for i in itertools.product([0, 1], repeat=grain_size * grain_size)
    ]

    for configuration in p:

        if method(configuration):

            passed_arrays.append(configuration)

    for current_array in passed_arrays:

        number_of_occupied = np.sum(current_array)

        try:
            amount_of_each[number_of_occupied] += 1
        except KeyError:
            amount_of_each[number_of_occupied] = 1

    items_in_computation = []

    for key in amount_of_each:

        tmp = "({})*(p**{})*((1-p)**{})".format(
            amount_of_each[key], key, (grain_size ** 2) - key
        )

        items_in_computation.append(tmp)

        equation_to_solve = "+".join(items_in_computation)

    equation_to_solve = "(" + equation_to_solve + ")"

    equation_to_solve = equation_to_solve + " - p"

    p = Symbol("p")

    solutions = solveset(parse_expr(equation_to_solve), p, domain=S.Reals)

    for solution in solutions:

        tmp = N(solution)

        if tmp < 1 and tmp > 0:

            return(tmp)


if __name__ == '__main__':

    result = coarse_graining_estimate(5,method=majority)

    print(result)