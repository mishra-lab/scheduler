from netflow import FlowArc, FlowNetwork, FlowVertex
from strategy import RandomStrategy
import time


def main():
    vertices = {
        'source': FlowVertex('source', 5),
        'a': FlowVertex('a', 0),
        'b': FlowVertex('b', 0),
        '1': FlowVertex('1', 0),
        '2': FlowVertex('2', 0),
        '3': FlowVertex('3', 0),
        '4': FlowVertex('4', 0),
        '5': FlowVertex('5', 0),
        'sink': FlowVertex('sink', -5)
    }

    arcs = [
        FlowArc(vertices['source'], vertices['a'], 0, 5, 0, fixed_cost=True),
        FlowArc(vertices['source'], vertices['b'], 0, 5, 0, fixed_cost=True),

        FlowArc(vertices['a'], vertices['1'], 0, 1, 1),
        FlowArc(vertices['a'], vertices['2'], 0, 1, 1),
        FlowArc(vertices['a'], vertices['3'], 0, 1, 1),
        FlowArc(vertices['a'], vertices['4'], 0, 1, 1),
        FlowArc(vertices['a'], vertices['5'], 0, 1, 1),

        FlowArc(vertices['b'], vertices['1'], 0, 1, 1),
        FlowArc(vertices['b'], vertices['2'], 0, 1, 1),
        FlowArc(vertices['b'], vertices['3'], 0, 1, 1),
        FlowArc(vertices['b'], vertices['4'], 0, 1, 1),
        FlowArc(vertices['b'], vertices['5'], 0, 1, 1),

        FlowArc(vertices['1'], vertices['sink'], 1, 1, 0, fixed_cost=True),
        FlowArc(vertices['2'], vertices['sink'], 1, 1, 0, fixed_cost=True),
        FlowArc(vertices['3'], vertices['sink'], 1, 1, 0, fixed_cost=True),
        FlowArc(vertices['4'], vertices['sink'], 1, 1, 0, fixed_cost=True),
        FlowArc(vertices['5'], vertices['sink'], 1, 1, 0, fixed_cost=True),
        # circulation edge
        FlowArc(vertices['sink'], vertices['source'], 0, 10, 0)
    ]

    net = FlowNetwork(vertices.values(), arcs, strategy=RandomStrategy)
    net.solve()


if __name__ == '__main__':
    start_time = time.clock()
    main()
    print('time =', time.clock() - start_time, 'seconds')
