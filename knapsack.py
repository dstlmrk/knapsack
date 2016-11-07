#!/usr/bin/python
# coding=utf-8

from __future__ import print_function
import click
import sys
import math
import time

MAX_INT = 99999


class File(list):
    """
    Represents file.
    """

    def __init__(self, path):
        self = [self.append(x) for x in self.load_file(path)]

    def load_file(self, path):
        with open(path) as f:
            return f.readlines()


class SolutionFile(File):
    """
    Represents file with solutions.
    """

    def __init__(self, path):
        path = "./sol/" + path.split('/')[-1].replace('inst', 'sol')
        super(SolutionFile, self).__init__(path)


class Item(object):
    """
    Represents one item.
    """

    def __init__(self, weight, price, index):
        self.weight = weight
        self.price = price
        self.ratio = price / float(weight)
        self.index = index
        # value for fptas alg
        self._price = self.price


class Knapsack(object):
    """
    This class includes all important methods for all algorithms.
    It loads input and expected output primarily.
    """

    def __init__(self, input, solution):
        self.load_input(input)
        self.load_solution(solution)

    def load_input(self, input):
        input = input.strip().split()
        self.id = int(input[0])
        self.items_cnt = int(input[1])
        self.capacity = int(input[2])
        items = []
        i = 0
        for j in range(3, (2*self.items_cnt)+3, 2):
            items.append(Item(int(input[j]), int(input[j+1]), i))
            i += 1
        self.items = items

    def load_solution(self, solution):
        solution = solution.strip().split('  ')
        solution[0] = solution[0].split()
        self.expected_price = int(solution[0][2])
        self.expected_configuration = [int(x) for x in solution[1].split()]

    def is_correct_result(self, price):
        return True if price == self.expected_price else False

    def bag_is_not_overload(self, configuration):
        used_capacity = 0
        for i, val in enumerate(configuration):
            used_capacity += val*self.items[i].weight
        # print(used_capacity, self.capacity)
        return True if used_capacity <= self.capacity else False

    def get_max_price(self):
        max_price = 0
        for item in self.items:
            max_price += item.price
        return max_price

    def evaluate(self):
        pass


class Bruteforce(Knapsack):
    """
    This alg enumerates all results and selects the best.
    """

    def __init__(self, input, solution):
        super(Bruteforce, self).__init__(input, solution)

    def evaluate(self):
        capacity, price, configuration = self._bruteforce(
            self.capacity, 0, self.items
        )
        return price, list(reversed(configuration))

    def _bruteforce(self, capacity, price, items):

        if len(items) == 1:
            item = items[0]
            if item.weight <= capacity:
                return (capacity-item.weight), (price+item.price), [1]
            else:
                return capacity, price, [0]

        item = items[0]

        # don't take the item
        c1, p1, cnf1 = self._bruteforce(
            capacity, price, items[1:]
        )
        # take the item
        c2, p2, cnf2 = self._bruteforce(
            capacity-item.weight, price+item.price, items[1:]
        )

        return self.choose_better_solution(c1, c2, p1, p2, cnf1, cnf2)

    def choose_better_solution(self, c1, c2, p1, p2, cnf1, cnf2):
        if p1 > p2 and c1 >= 0:
            cnf1.append(0)
            return c1, p1, cnf1
        elif p2 > p1 and c2 >= 0:
            cnf2.append(1)
            return c2, p2, cnf2
        elif p1 == p2:
            if c1 <= c2 and c1 >= 0:
                cnf1.append(0)
                return c1, p1, cnf1
            elif c2 <= c1 and c2 >= 0:
                cnf2.append(1)
                return c2, p2, cnf2
            elif c1 >= 0:
                cnf1.append(0)
                return c1, p1, cnf1
            elif c2 >= 0:
                cnf2.append(1)
                return c2, p2, cnf2
            else:
                return 0, 0, []
        elif c1 >= 0:
            cnf1.append(0)
            return c1, p1, cnf1
        else:
            return 0, 0, []


class Ratio(Knapsack):
    """
    Ratio sorts all items by ratio of price and weight and adds
    them into bag step by step, if is it possible.
    """

    def evaluate(self):
        price = 0
        capacity = self.capacity
        configuration = [0 for i, val in enumerate(self.items)]
        sorted_items = sorted(
            self.items, key=lambda item: item.ratio, reverse=True
        )
        for item in sorted_items:
            if item.weight <= capacity:
                capacity -= item.weight
                price += item.price
                configuration[item.index] = 1

        return price, configuration


class BranchAndBound(Bruteforce):
    """
    It enumerates almost all results and selects the best.
    """

    def evaluate(self):
        self.best_price = 0
        max_price = 0
        for item in self.items:
            max_price += item.price
        capacity, price, configuration = self._bruteforce(
            self.capacity, 0, self.items, max_price
        )
        return price, list(reversed(configuration))

    def _bruteforce(self, capacity, price, items, max_price):

        if len(items) == 1:
            item = items[0]
            if item.weight <= capacity:
                return (capacity-item.weight), (price+item.price), [1]
            else:
                return capacity, price, [0]

        if capacity <= 0 or price+max_price < self.best_price:
            return capacity, price, [0 for x in items]

        item = items[0]

        # take the item
        if capacity-item.weight >= 0 and self.best_price < price+item.price:
            self.best_price = price+item.price
        c2, p2, cnf2 = self._bruteforce(
            capacity-item.weight,
            price+item.price,
            items[1:],
            max_price-item.price
        )

        # don't take the item
        c1, p1, cnf1 = self._bruteforce(
            capacity,
            price,
            items[1:],
            max_price-item.price
        )

        return self.choose_better_solution(c1, c2, p1, p2, cnf1, cnf2)


class Dynamic(Knapsack):
    """
    It uses table of subresults.
    """

    def _evaluate(self):
        table_height = self.get_max_price()+1
        table_width = self.items_cnt+1
        self.subresults = [
            [{"weight": None, "used": None} for j \
                in range(table_height)] for i in range(table_width)
        ]
        # W(0,0) = 0
        self.subresults[0][0]['weight'] = 0
        # compute table of subresults
        self._compute_subresult(0, 0, None)
        # self._print_subresults()

        last_row = self.subresults[self.items_cnt]
        for index, val in reversed(list(enumerate(last_row))):
            # W(n, c) < M for biggest c
            if (val.get('weight') or MAX_INT) > self.capacity:
                continue
            price = index
            break

        configuration = self._detect_configuration(self.items_cnt, index)

        return price, configuration

    def evaluate(self):
        return self._evaluate()

    def _compute_subresult(self, i, j, used):
        # set configuration
        self.subresults[i][j]['used'] = used
        weight = self.subresults[i][j]['weight']
        # last row in the table of subresults or overloaded bag
        if i == self.items_cnt or weight > self.capacity:
            return

        # take the item
        next_subresult = self.subresults[i+1][j+self.items[i].price]["weight"]
        # if it does make sense
        if (next_subresult is None) or (
            next_subresult > weight+self.items[i].weight
        ):
            # set the next subresult with used item
            self.subresults[i+1][j+self.items[i].price]["weight"] = (
                weight+self.items[i].weight
            )
            # compute a next cell in the table of subresults
            self._compute_subresult(i+1, j+self.items[i].price, True)

        # don't take the item
        next_subresult = self.subresults[i+1][j]["weight"]
        # if it does make sense
        if next_subresult is None or next_subresult > weight:
            # set the next subresult with unused item
            self.subresults[i+1][j]["weight"] = weight
            # compute a next cell in the table of subresults
            self._compute_subresult(i+1, j, False)

    def _detect_configuration(self, i, j):
        """by recurse gets configuration"""
        if self.subresults[i][j]['used'] is None:
            return []
        elif self.subresults[i][j]['used']:
            cnf = self._detect_configuration(i-1, j-self.items[i-1].price)
            cnf.append(1)
            return cnf
        else:
            cnf = self._detect_configuration(i-1, j)
            cnf.append(0)
            return cnf

    def _print_subresults(self):
        """print full table of subresults"""
        for i in self.subresults:
            for j in i:
                print("({:4}, {:4}) ".format(j['weight'], j['used']), end="")
            print()


class FPTAS(Dynamic):
    """
    It uses dynamic alg. It converts all prices by relative error.
    """

    def __init__(self, relative_error, *args):

        super(FPTAS, self).__init__(*args)

        max_price = self.get_max_price()

        # number of neglected bits
        bits_cnt = math.floor(math.log(
            ((relative_error*max_price)/self.items_cnt), 2
        ))

        # set new price of items
        for item in self.items:
            item.price = int(math.floor(
                item.price / 2**bits_cnt
            ))

    def evaluate(self):
        price, configuration = self._evaluate()

        # get original price of used items
        price = 0
        for index, val in enumerate(configuration):
            if val:
                price += self.items[index]._price

        return price, configuration


@click.command()
@click.option('--method', default="bruteforce",
              help="bruteforce/ratio/bb/dynamic/fptas")
@click.option('--path', default="./inst/knap_4.inst.dat",
              help="Input file.")
@click.option('--relative-error', default=0.5,
              help="Relative error for FPTAS alg.")
def main(method, path, relative_error):

    if not 0 < relative_error <= 1:
        sys.exit("Relative error should be > 0 and <= 1")

    dataset = File(path)
    solution = SolutionFile(path)

    duration_sum = 0
    measured_relative_error_sum = 0
    measured_relative_error_max = 0

    for i, val in enumerate(dataset):

        # if i in [0,1,2,3,4]:
            # continue

        if method == "bruteforce":
            knapsack = Bruteforce(dataset[i], solution[i])
        elif method == "ratio":
            knapsack = Ratio(dataset[i], solution[i])
        elif method == "bb":
            knapsack = BranchAndBound(dataset[i], solution[i])
        elif method == "dynamic":
            knapsack = Dynamic(dataset[i], solution[i])
        elif method == "fptas":
            knapsack = FPTAS(relative_error, dataset[i], solution[i])

        # print(knapsack.id)
        # if knapsack.id != 9130:
            # continue
        # print(knapsack.id)

        # TODO: nebyl by tady dobry dekorator? NAHRADIT CPU TIME
        stime = time.time()
        price, configuration = knapsack.evaluate()
        duration = time.time() - stime

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

    print(
        "\n"
        "average duration       = %.6f ms\n"
        "average relative error = %.6f %%\n"
        "    max relative error = %.6f %%\n"
        % (
            duration_avg,
            measured_relative_error_avg,
            measured_relative_error_max*100
        )
    )

    # print("average relative error = %.6f" % relative_error_avg)
    # print("average relative error = %.6f" % relative_error_avg)

if __name__ == '__main__':
    main()
