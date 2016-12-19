from knapsack import Knapsack


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
