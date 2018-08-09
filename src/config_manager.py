import os
import json


def save_config(data, file):
    print('Saving data to configuration file \'{}\'...'.format(args.filename))
    file.seek(0)
    file.truncate()
    json.dump(data, file)


def create_new_config(args):
    data = {
        "CLINICIANS": {},
        "DIVISIONS": {}
    }

    try:
        if not os.path.isfile(args.filename):
            with open(args.filename, 'w') as f:
                save_config(data, f)
        else:
            print('ERROR: file \'{}\' already exists, please delete it or supply a different filename'.format(
                args.filename))
    except IOError as e:
        print('ERROR: {}'.format(e))


def add_clinician(args):
    try:
        with open(args.filename, 'r+') as f:
            data = json.load(f)

            data["CLINICIANS"][args.name] = {
                "email": args.email
            }

            ans = None
            first_time = True
            while ans != 'n':
                ans = input(
                    'Would you like to add this clinician to {} division? (y/n) '
                    .format('a' if first_time else 'another')
                )

                if ans == 'y':
                    div, min_, max_ = input(
                        'Please supply the name of the division, minimum and maximum values, separated by spaces (example: ID 3 5): ').split()
                    if div not in data["DIVISIONS"]:
                        data["DIVISIONS"][div] = {}
                    data["DIVISIONS"][div][args.name] = {
                        'min': int(min_),
                        'max': int(max_)
                    }
                    first_time = False

            save_config(data, f)

    except IOError as e:
        print('ERROR: {}'.format(e))
    except KeyError as e:
        print('ERROR: {}'.format(e))
        print('Make sure to use a configuration file created using the \'new\' command')


def remove_clinician(args):
    try:
        with open(args.filename, 'r+') as f:
            data = json.load(f)

            if args.name in data["CLINICIANS"]:
                print('Removing \'{}\' from the configuration file...'.format(args.name))
                del data["CLINICIANS"][args.name]
                for div in data["DIVISIONS"]:
                    if args.name in data["DIVISIONS"][div]:
                        del data["DIVISIONS"][div][args.name]
            else:
                print(
                    'Clinician \'{}\' was not found in the configuration file'.format(args.name))

            save_config(data, f)

    except IOError as e:
        print('ERROR: {}'.format(e))


def update_clinician(args):    
    try:
        with open(args.filename, 'r+') as f:
            data = json.load(f)

            if args.name in data["CLINICIANS"]:
                if args.email:
                    data["CLINICIANS"][args.name]["email"] = args.email
                else:
                    args.email = data["CLINICIANS"][args.name]["email"]
            else:
                print(
                    'Clinician \'{}\' was not found in the configuration file'.format(args.name))

            save_config(data, f)

        add_clinician(args)

    except IOError as e:
        print('ERROR: {}'.format(e))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_new = subparsers.add_parser(
        'new', help='create a new configuration file')
    parser_new.add_argument('filename', type=str,
                            help='configuration filename')
    parser_new.set_defaults(func=create_new_config)

    parser_add = subparsers.add_parser(
        'add', help='add a clinician to the configuration file')
    parser_add.add_argument('filename', type=str,
                            help='configuration filename')
    parser_add.add_argument('name', type=str, help='name of clinician')
    parser_add.add_argument('email', default='',
                            type=str, help='email of clinician')
    parser_add.set_defaults(func=add_clinician)

    parser_remove = subparsers.add_parser(
        'remove', help='remove a clinician from the configuration file')
    parser_remove.add_argument(
        'filename', type=str, help='configuration filename')
    parser_remove.add_argument(
        'name', type=str, help='name of clinician to remove')
    parser_remove.set_defaults(func=remove_clinician)

    parser_update = subparsers.add_parser(
        'update', help='update clinician information in the configuration file')
    parser_update.add_argument(
        'filename', type=str, help='configuration filename')
    parser_update.add_argument(
        'name', type=str, help='name of clinician')
    parser_update.add_argument(
        '--email', type=str, help='new email')
    parser_update.set_defaults(func=update_clinician)

    args = parser.parse_args()
    args.func(args)
