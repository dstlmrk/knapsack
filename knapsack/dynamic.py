from __future__ import print_function
from knapsack import Knapsack

MAX_INT = 99999

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
