import os
import time

import scheduler
from netflow import FlowNetwork
from settings import SettingsManager
from strategy import ConsecutiveStrategy, RandomStrategy


def main(settings, config_path=None, publish=False):
    sched = scheduler.Scheduler(settings)
    if config_path: sched.config_file = config_path

    sched.read_config()
    if (not config_path): sched.read_calendar()
    sched.build_lp()
    
    if (sched.solve_lp()):
        sched.assign_schedule()
        if (publish): sched.publish_schedule()

        for division in sched.divisions.values():
            print('\n{}\n----'.format(division.name))
            for clinician in division.assignments:
                print(clinician.name)

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
    parser.add_argument('--blocks', type=int)
    parser.add_argument('--publish', action='store_true', default=False)
    parser.add_argument('--config')
    args = parser.parse_args()

    start_time = time.clock()
    with SettingsManager(build_path('../config/settings.json')) as settings:
        if args.blocks: 
            scheduler.NUM_BLOCKS = int(args.blocks)
        main(settings, args.config, args.publish)
    print('time =', time.clock() - start_time, 'seconds')
