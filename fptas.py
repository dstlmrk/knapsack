import math
from dynamic import Dynamic


class FPTAS(Dynamic):
    """
    It uses dynamic alg. It converts all prices by relative error.
    """

    def __init__(self, relative_error, *args):

        super(FPTAS, self).__init__(*args)

        max_price = self.get_max_price()

        # number of neglected bits
        bits_cnt = int(math.floor(math.log(
            ((relative_error*max_price)/self.items_cnt), 2
        )))

        # print(str(
        #     float(self.items_cnt)*(2**bits_cnt)/float(max_price)
        # ).replace(".",","))
        # print(bits_cnt)

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
