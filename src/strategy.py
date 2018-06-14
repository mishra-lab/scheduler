import random
import itertools


class Strategy:
    """
    Abstract class. Represents a strategy for adjusting costs
    in minflow network.
    """

    def __init__(self, network=None):
        self.network = network

    def adjustCosts(self):
        raise NotImplementedError

    def set_network(self, network):
        self.network = network


class RandomStrategy(Strategy):
    """
    A strategy to adjust costs by randomly choosing which arcs to adjust.

    Each arc has a 50% chance of being adjusted
    """

    def __init__(self, network=None):
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

    def __init__(self, network=None, consecutive_allowed=2):
        Strategy.__init__(self, network)
        self.consecutive_allowed = consecutive_allowed

    def groupby_source_vert(self, arc):
        return arc.source_vert.name

    def adjustCosts(self):
        """
        Adjust costs by counting number of consecutive weeks assigned
        to each clincian, discouraging > consecutive_allowed weeks in a row
        """
        # group arcs by clinician
        grouped_arcs = {}
        adjustable_arcs = filter(lambda x: not x.fixed_cost, self.network.arcs)
        for key, arc_iter in itertools.groupby(adjustable_arcs, key=self.groupby_source_vert):
            grouped_arcs[key] = list(arc_iter)

        for key in grouped_arcs:
            consec = 0
            arcs = grouped_arcs[key]
            for arc in arcs:
                # keep an incrementing count when we encounter consecutive
                # weeks
                if arc.flow == 1:
                    consec += 1
                elif arc.flow == 0:
                    consec = 0

                # increase the cost of the arc when we go over the threshold
                if consec > self.consecutive_allowed:
                    arc.cost += 1
                    consec = 0
