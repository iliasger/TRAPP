from __future__ import print_function

from subprocess import Popen

# this script is used to generate the data for the EPOS comparison baseline.

starting_index = 0

simulations_n = 5
iterations = 20

if __name__ == "__main__":

    k = starting_index

    for j in range(iterations):
        simulations = []

        for i in range(simulations_n):
            simulations.append(Popen(["python", "./run.py", str(k)]))
            print("Simulation " + str(k) + " started...")
            k += 1

        for p in simulations:
            p.wait()
