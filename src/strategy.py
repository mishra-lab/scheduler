import random


class Strategy:
    """
    Abstract class. Represents a strategy for adjusting costs
    in minflow network.
    """

    def __init__(self, network):
        self.network = network

    def adjustCosts(self):
        raise NotImplementedError


class RandomStrategy(Strategy):
    """
    A strategy to adjust costs by randomly choosing which arcs to adjust.

    Each arc has a 50% chance of being adjusted
    """

    def __init__(self, network):
        Strategy.__init__(self, network)

    def adjustCosts(self):
        """
        Adjusts costs of the non-fixed arcs in the network by randomly
        choosing which edges to adjust
        """

        # TODO: make chance variable
        # find all arcs that can be adjusted and randomly increase
        # the cost of an arc with a 50% chance
        adjustable_arcs = filter(lambda x: not x.fixed_cost, self.network.arcs)
        for arc in adjustable_arcs:
            adjust = random.randint(0, 1)
            if adjust:
                arc.cost += random.randint(1, 5)


class ConsecutiveStrategy(Strategy):

    def __init__(self, network):
        Strategy.__init__(self, network)

    def adjustCosts(self):
        """
        Adjust costs by counting number of consecutive weeks assigned
        to each doctor, discouraging > k weeks in a row
        """
        # TODO: implement
        return
