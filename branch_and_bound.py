from bruteforce import Bruteforce


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
