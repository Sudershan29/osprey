"""Osprey Client API."""
import requests
import sys, argparse
import json

SERVER_ADDRESS = '192.5.86.226:5001'
SERVER_URL = f"http://{SERVER_ADDRESS}/osprey/api/v1.0/"


def all_sources() -> None:
    """Get the dictionary of all the sources.

    Returns:
        a list containing all available sources data
    """
    req = requests.get(f'{SERVER_URL}/source')
    resp = json.loads(req.content)
    print(json.dumps(resp, indent=4))

def all_proxies() -> None:
    """Get the dictionary of all the sources.

    Returns:
        a list containing all available sources data
    """
    req = requests.get(f'{SERVER_URL}/proxies')
    resp = json.loads(req.content)
    print(json.dumps(resp, indent=4))

def create_source(name: str, url: str, timer: int = None, description: str = None, verifier: str = None, modifier: str = None) -> None:
    data = {'name': name, 'url': url}
    if timer is not None:
        data['timer'] = timer
    if description is not None:
        data['description'] = description
    if verifier is not None:
        data['verifier'] = verifier
    if modifier is not None:
        data['modifier'] = modifier
    req = requests.post(f'{SERVER_URL}/source', json=data)
    print(json.loads(req.content))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Osprey client to create sources',
    )

    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument('-list_sources', action='store_true')
    command_group.add_argument('-list_proxies',  action='store_true')
    command_group.add_argument('-create_source',  action='store_true')
    parser.add_argument(
            '-n',
            '--name',
            required='-create_source' in sys.argv,
            help='Name for the source',
        )
    parser.add_argument(
        '-u',
        '--url',
        required='-create_source' in sys.argv,
        help='url for the source',
    )
    parser.add_argument(
        '-t',
        '--timer',
        help='timer (in s) how often to refresh source',
    )
    parser.add_argument(
        '-d',
        '--description',
        help='description for the source',
    )
    parser.add_argument(
        '-v',
        '--verifier',
        help='globus-compute function uuid for the verifier',
    )
    parser.add_argument(
        '-m',
        '--modifier',
        help='globus-compute function uuid for the modifier',
    )
    args = parser.parse_args()
    if args.list_sources:
        all_sources()
    elif args.list_proxies:
        all_proxies()
    elif args.create_source:
        create_source(name=args.name,
                    url=args.url,
                    timer=args.timer,
                    description=args.description,
                    verifier=args.verifier,
                    modifier=args.modifier)
