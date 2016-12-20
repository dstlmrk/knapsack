#!/usr/bin/python
# coding=utf-8


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
        path = "./data/sol/" + path.split('/')[-1].replace('inst', 'sol')
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

    def __init__(self, input, solution=None):
        self.load_input(input)
        if solution:
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

    def get_price(self, configuration):
        price = 0
        for i, val in enumerate(configuration):
            price += val*self.items[i].price
        return price

    def evaluate(self):
        pass
