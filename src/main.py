from netflow import FlowNetwork
from strategy import RandomStrategy, ConsecutiveStrategy
from scheduler import Parser
import time
import os


def main(rel_path):
    filepath = os.path.join(
        os.path.dirname(__file__),
        rel_path
    )
    p = Parser(filepath)
    net = FlowNetwork(
        p.get_vertices().values(),
        p.get_arcs(),
        strategy=RandomStrategy
    )
    net.solve(iterations=2)
    # print(net)

    net.strategy = ConsecutiveStrategy(net)
    net.solve(iterations=100)
    print(net)

    assignments = list(filter(lambda x: x.flow > 0 and x.source_vert.name in p.clinicians,net.arcs))
    assignments.sort(key=lambda x: int(x.dest_vert.name))
    for a in assignments:
        print(a.source_vert.name)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('relative_path')
    args = parser.parse_args()

    start_time = time.clock()
    main(args.relative_path)
    print('time =', time.clock() - start_time, 'seconds')
