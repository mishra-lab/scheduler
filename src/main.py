import os
import time

import scheduler
from netflow import FlowNetwork
from settings import SettingsManager
from strategy import ConsecutiveStrategy, RandomStrategy


def main(settings, data_path=None, publish=False):
    sched = scheduler.Scheduler(settings)
    sched.read_clinic_conf()
    if data_path:
        sched.populate_blocks_off_from_file(build_path(data_path))
    else:
        sched.populate_blocks_off()
    sched.build_lp()
    
    if (sched.solve_lp()):
        if (publish): sched.assign_blocks()

        for j in range(scheduler.NUM_BLOCKS):
            for clin in sched.clinicians.values():
                if clin.get_value(j) == 1.0:
                    print(clin.name)
                    print(clin.name)
                    break
    else:
        print('could not find solution')
    

def build_path(rel_path):
    return os.path.join(
        os.path.dirname(__file__),
        rel_path
    )

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--blocks', type=int)
    parser.add_argument('--publish', action='store_true', default=False)
    args = parser.parse_args()

    start_time = time.clock()
    with SettingsManager(build_path('../config/settings.json')) as settings:
        if args.blocks: 
            scheduler.NUM_BLOCKS = int(args.blocks)
        main(settings, args.file, args.publish)
    print('time =', time.clock() - start_time, 'seconds')
