from knapsack import Knapsack


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
