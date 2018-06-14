from netflow import FlowNetwork
from strategy import RandomStrategy, ConsecutiveStrategy
from scheduler import Scheduler
import time
import os


def main(rel_path):
    sched = Scheduler(build_path('../settings.json'))
    sched.read_clinic_conf()
    sched.populate_weeks_off_from_file(build_path(rel_path))
    sched.build_net()

    sched.network.set_strategy(RandomStrategy())
    sched.network.solve(iterations=2)

    sched.network.set_strategy(ConsecutiveStrategy(consecutive_allowed=2))
    sched.network.solve(iterations=50)
    # print(sched.network)
    sched.assign_weeks()
    print(sched.network)

def build_path(rel_path):
    return os.path.join(
        os.path.dirname(__file__),
        rel_path
    )

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('relative_path')
    args = parser.parse_args()

    start_time = time.clock()
    main(args.relative_path)
    print('time =', time.clock() - start_time, 'seconds')
