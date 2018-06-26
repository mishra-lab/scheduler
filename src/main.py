import os
import time

from netflow import FlowNetwork
from scheduler import Scheduler
from settings import SettingsManager
from strategy import ConsecutiveStrategy, RandomStrategy


def main(settings, data_path=None):
    sched = Scheduler(settings)
    sched.read_clinic_conf()
    if data_path:
        sched.populate_blocks_off_from_file(build_path(data_path))
    else:
        sched.populate_blocks_off()
    sched.build_net()

    # sched.network.set_strategy(RandomStrategy())
    # sched.network.solve(iterations=2)

    sched.network.set_strategy(ConsecutiveStrategy(consecutive_allowed=1))
    sched.network.solve(iterations=50)
    # print(sched.network)
    if not data_path:
        sched.assign_weeks()
    # print(sched.network)

    net = sched.network
    assignments = list(filter(lambda x: x.flow > 0 and x.source_vert.name in sched.clinicians.keys(),net.arcs))
    assignments.sort(key=lambda x: int(x.dest_vert.name))
    for a in assignments:
        print(a.source_vert.name)
        print(a.source_vert.name)

def build_path(rel_path):
    return os.path.join(
        os.path.dirname(__file__),
        rel_path
    )

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    args = parser.parse_args()

    start_time = time.clock()
    with SettingsManager(build_path('../config/settings.json')) as settings:
        main(settings, args.file)
    print('time =', time.clock() - start_time, 'seconds')
