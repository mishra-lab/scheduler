import json

def main(num_clin, num_services):
    divisions = {}
    for i in range(1, num_services + 1):
        divisions[str(i)] = {
            "min": 0, "max": 1000
        }

    data = {}
    for i in range(1, num_clin + 1):
        data[str(i)] = {
            "name": str(i),
            "email": "",
            "divisions": divisions
        }

    with open('./configs/sim_{}srv_{}clin.json'.format(num_services, num_clin), 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('num_clinicians', type=int)
    parser.add_argument('num_services', type=int)

    args = parser.parse_args()
    main(args.num_clinicians, args.num_services)