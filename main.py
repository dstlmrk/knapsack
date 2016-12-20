#!/usr/bin/python
# coding=utf-8

from __future__ import print_function
import click
import sys
import time
from knapsack.knapsack import File, SolutionFile
from knapsack.bruteforce import Bruteforce
from knapsack.ratio import Ratio
from knapsack.dynamic import Dynamic
from knapsack.branch_and_bound import BranchAndBound
from knapsack.fptas import FPTAS
from knapsack.simulated_annealing import SimulatedAnnealing


@click.command()
@click.option('--method', default="bruteforce",
              help="bruteforce / ratio / bb / dynamic / fptas / sa (simulated annealing) / all (without sa) [bruteforce]")
@click.option('--path', default="./inst/knap_4.inst.dat",
              help="Input file. [./inst/knap_4.inst.dat]")
@click.option('--relative-error', default=0.5,
              help="Relative error for FPTAS alg. [0.5]")
@click.option('--solution/--no-solution', default=True,
              help="If solution file is available or not. [True]")
@click.option('--time-test/--no-time-test', default=False,
              help="It returns avg time only. [False]")
@click.option('--error-test/--no-error-test', default=False,
              help="It returns avg relative error only. [False]")
@click.option('-v', '--verbose/--no-verbose', default=False,
              help="[False]")
@click.option('-t', '--temperature', default=1000,
              help="Init temperature for simulated annealing. [1000]")
@click.option('-c', '--cooling', default=0.9,
              help="Cooling for simulated annealing. [0.9]")
@click.option('-i', '--inner-loop', default=5,
              help="Number of iterations in inner loop for simulated annealing. [5]")
def main(method, path, relative_error, solution,
         time_test, error_test, verbose, temperature,
         cooling, inner_loop):

    if not 0 < relative_error <= 1:
        sys.exit("Relative error should be > 0 and <= 1")

    dataset = File(path)

    # if I don't have solution I have to count it
    if solution:
        solution_file = SolutionFile(path)
    else:
        # solution_file = None
        counted_solution = []

    # if I don't have solution, I have to count it by optimal alg
    # (bruteforce, dynamic or bb)
    if method == "all":
        methods = [
            "bruteforce",
            "bb",
            "dynamic",
            "ratio",
            "fptas"
        ]
    else:
        methods = [method]

    for method in methods:

        duration_sum = 0
        measured_relative_error_sum = 0
        measured_relative_error_max = 0

        for i, val in enumerate(dataset):

            if solution:
                sol = solution_file[i]
            else:
                sol = None

            if method == "bruteforce":
                knapsack = Bruteforce(dataset[i], sol)
            elif method == "ratio":
                knapsack = Ratio(dataset[i], sol)
            elif method == "bb":
                knapsack = BranchAndBound(dataset[i], sol)
            elif method == "dynamic":
                knapsack = Dynamic(dataset[i], sol)
            elif method == "fptas":
                knapsack = FPTAS(relative_error, dataset[i], sol)
            elif method == "sa":
                knapsack = SimulatedAnnealing(temperature, cooling, inner_loop, dataset[i], sol)

            stime = time.time()
            price, configuration = knapsack.evaluate
            duration = time.time() - stime

            if not solution:
                if method == methods[0] \
                and method in ["dynamic", "bb", "bruteforce"]:
                    # correct result
                    counted_solution.append(price)
                # one method if them counted correct result
                knapsack.expected_price = counted_solution[i]
                knapsack.expected_configuration = None

            duration_sum += duration
            measured_relative_error = \
                (knapsack.expected_price-price) / float(knapsack.expected_price)
            measured_relative_error_max = max(
                measured_relative_error_max, measured_relative_error
            )
            measured_relative_error_sum += measured_relative_error

            correct_result = knapsack.is_correct_result(price)
            # print(correct_result)
            # print(knapsack.bag_is_not_overload(configuration))
            if verbose:
                if correct_result and knapsack.bag_is_not_overload(configuration):
                    print("OK   {:6} {}".format(price, configuration))
                else:
                    print("FAIL {:6} {} != {} {}".format(
                        price, configuration,
                        knapsack.expected_price,
                        knapsack.expected_configuration
                    ))
            # break

        duration_avg = (duration_sum / len(dataset)) * 1000
        measured_relative_error_avg = (
            (measured_relative_error_sum / len(dataset)) * 100
        )

        if time_test:
            print("Duration avg [%s]: %.6f\t" % (method, duration_avg))
            # # pokud jde o posledni metodu -> novy radek
            # if method == methods[len(methods)-1]:
            #     print()
        elif error_test:
            if method == "ratio":
                print("Relative error avg [%s]: %.6f" %
                    (method, measured_relative_error_avg)
                )
        else:
            print(
                "----------------------------------\n"
                "= %s"
                "\n"
                "average duration       = %.6f ms\n"
                "average relative error = %.6f %%\n"
                "    max relative error = %.6f %%\n"
                "----------------------------------"
                % (
                    method,
                    duration_avg,
                    measured_relative_error_avg,
                    measured_relative_error_max*100
                )
            )

if __name__ == '__main__':
    main()
