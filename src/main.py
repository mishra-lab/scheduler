import os
import time

import scheduler
from netflow import FlowNetwork
from settings import SettingsManager
from strategy import ConsecutiveStrategy, RandomStrategy


def main(settings, config_path=None, no_read=False, no_write=False):
    sched = scheduler.Scheduler(settings)
    if config_path: sched.config_file = config_path

    sched.read_config()
    if (not no_read): sched.read_timeoff()
    sched.build_lp()
    
    if (sched.solve_lp()):
        sched.assign_schedule()
        if (not no_write): sched.publish_schedule()

        for division in sched.divisions.values():
            print('\n{}\n----'.format(division.name))
            for clinician in division.assignments:
                print(clinician.name)
                print(clinician.name)

        print('\nweekends\n----')
        weekend_assignments = [
            _ for clinician in sched.clinicians.values() 
                for _ in clinician.get_weekend_vars(
                    lambda x: x.get_value() == 1.0
                )
        ]
        weekend_assignments.sort(key=lambda x: x.week_num)
        for wa in weekend_assignments:
            if wa.week_num in sched.long_weekends:
                print(wa.clinician.name + "****")
            else:
            print(wa.clinician.name)
            

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
    parser.add_argument('-nr' '--no-read', action='store_true', default=False)
    parser.add_argument('-nw' '--no-write', action='store_true', default=False)
    parser.add_argument('--config')
    args = parser.parse_args()

    start_time = time.clock()
    with SettingsManager(build_path('../config/settings.json')) as settings:
        if args.blocks: 
            scheduler.NUM_BLOCKS = int(args.blocks)
            scheduler.NUM_WEEKENDS = scheduler.NUM_BLOCKS * scheduler.BLOCK_SIZE
        main(settings, args.config, args.nr__no_read, args.nw__no_write)
    print('time =', time.clock() - start_time, 'seconds')
