from netflow import FlowNetwork
from strategy import RandomStrategy, ConsecutiveStrategy
from scheduler import Parser
import time
import os


def main():
    filepath = os.path.join(
        os.path.dirname(__file__),
        '../data/ab_test.txt'
    )
    p = Parser(filepath)
    net = FlowNetwork(
        p.get_vertices().values(),
        p.get_arcs(),
        strategy=ConsecutiveStrategy
    )
    net.solve(iterations=100)


if __name__ == '__main__':
    start_time = time.clock()
    main()
    print('time =', time.clock() - start_time, 'seconds')
