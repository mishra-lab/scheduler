import os
import time

from netflow import FlowNetwork
from scheduler import Scheduler, NUM_WEEKS
from settings import SettingsManager
from strategy import ConsecutiveStrategy, RandomStrategy


def main(settings, data_path=None):
    sched = Scheduler(settings)
    sched.read_clinic_conf()
    if data_path:
        sched.populate_weeks_off_from_file(build_path(data_path))
    else:
        sched.populate_weeks_off()
    sched.build_lp()
    sched.solve_lp()

    for j in range(NUM_WEEKS):
        for clin in sched.clinicians.values():
            if clin.get_var(j).solution_value() == 1.0:
                print(clin.name)
                break
    

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
