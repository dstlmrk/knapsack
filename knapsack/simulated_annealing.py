#!/usr/bin/python
# coding=utf-8

from knapsack import Knapsack
import random
import math


class State():

    def __init__(self, price, bit_array):
        self.price = price
        self.bit_array = bit_array



class SimulatedAnnealing(Knapsack):

    def __init__(self, init_temperature, cooling, inner_loop, *args):
        super(SimulatedAnnealing, self).__init__(*args)
        self.init_temperature = init_temperature
        self.cooling = cooling
        self.inner_loop = inner_loop

    def is_valid(self, state):
        return True;

    def get_neighbor(self, state):
        """
        Returns neighbor which is fit for max capacity of the bag.
        """
        new_bit_array = list(state.bit_array)
        random_position = random.randint(0, self.items_cnt-1)
        # add/remove one item from state
        new_bit_array[random_position] = (new_bit_array[random_position] + 1) % 2

        if self.bag_is_not_overload(new_bit_array):
            new_price = self.get_price(new_bit_array)
            return State(new_price, new_bit_array)
        else:
            return state

    def get_random_state(self):
        # empty bit array for first implementation
        return State(0, [0 for i in range(self.items_cnt)])

    def cool(self, temperature):
        # print temperature, self.cooling, temperature * self.cooling
        return temperature * self.cooling

    @staticmethod
    def frozen(temperature):
        return temperature > 0.1

    @property
    def evaluate(self):
        # init state
        state = self.get_random_state()
        temperature = self.init_temperature

        while self.frozen(temperature):
            # search between neighbors
            for i in range(self.inner_loop):
                neighbor = self.get_neighbor(state)
                # print neighbor.price
                # ziskej lepsi stav a ten uloz do best (to je vylepseni, jinak pouze do state)
                if neighbor.price > state.price:
                    # print ("nasel jsem lepsi stav (%s > %s)" % (neighbor.price, state.price))
                    state = neighbor
                # P(f_curr, f_new, t) = e^((f_new − f_curr)/t) >= random(0,1)
                elif math.e**((neighbor.price - state.price)/temperature) >= random.random():
                    # print ("nasel jsem horsi stav (%s)" % math.e**((neighbor.price - state.price)/temperature))
                    state = neighbor

            temperature = self.cool(temperature)
            # print float(temperature

        print state.price, state.bit_array
        return state.price, state.bit_array
        # return state
