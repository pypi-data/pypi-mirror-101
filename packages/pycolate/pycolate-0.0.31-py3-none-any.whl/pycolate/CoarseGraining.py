# TODO Make interactions possible.
from Percolation import Percolation
import numpy as np
from scipy.ndimage import measurements
import scipy.ndimage as ndimage
import itertools
from sympy import solveset, S
from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr
from sympy import N

generated_arrays = []
percolated_arrays = []

grain_size = 2

p = [
    np.reshape(np.array(i), (grain_size, grain_size))
    for i in itertools.product([0, 1], repeat=grain_size * grain_size)
]

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

percolated_arrays = []

passed_arrays = []

amount_of_each = {}

# The percolation step.
for configuration in p:

    if percolates(configuration):

        percolated_arrays.append(configuration)

passed_arrays = percolated_arrays

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

print(equation_to_solve)

p = Symbol("p")

solutions = solveset(parse_expr(equation_to_solve), p, domain=S.Reals)

for solution in solutions:

    tmp = N(solution)

    if tmp < 1 and tmp > 0:

        print(tmp)