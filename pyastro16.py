# This file contains the functions required for the parallelization tutorial
# given at the python-in-astronomy 2016 meeting. The examples are not optimial
# but have voluntarily been kept as simple as possible in order to make them
# easily understandstable.

import numpy as np


def scaled_sin(theta, scale):
    # Simple scaling of a sinus.
    return scale * np.sin(theta)


def counter_init(counter):
    # Initializer to demonstrate how to share a counter between processes.
    global gbl_counter

    # Make the counter globally available to the children process
    gbl_counter = counter


def counter(arg):
    # We need to get the lock to modify the counter and prevent other processes
    # from accessing it.
    with gbl_counter.get_lock():
        gbl_counter.value += 1


def counter_nolock(arg):
    # We modify the counter without locking it, which can yield erroneous
    # results.
    gbl_counter.value += 1


def random_init(output, counter):
    # Initializer to transform a RawArray into a 2D Numpy array used to store
    # the results of a computation.
    global gbl_output, gbl_counter, gbl_noutput

    # Make the counter globally available to the children process
    gbl_counter = counter

    # Convert the RawArray into a Numpy array with the right shape
    gbl_output = np.ctypeslib.as_array(output[0])
    gbl_output = gbl_output.reshape(output[1])

    # We can also create global variables to avoid recomputing some quantities
    gbl_noutput = output[1][1]


def random(idx, par):
    # Compute random values, store them in the output arrays, and increase the
    # counter.
    gbl_output[idx, :] = np.random.zipf(par, gbl_noutput)
    with gbl_counter.get_lock():
        gbl_counter.value += 1
