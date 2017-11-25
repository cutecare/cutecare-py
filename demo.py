#!/usr/bin/env python3

import argparse
import re
import logging

from cutecare.poller import CuteCarePoller
from cutecare.backends.gatttool import GatttoolBackend
from cutecare.backends.bluepy import BluepyBackend


def validate_device_mac(mac, pat=re.compile(r"C4:7C:8D:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}")):

    if not pat.match(mac):
        raise argparse.ArgumentTypeError('The MAC address "{}" seems to be in the wrong format'.format(mac))
    return mac

parser = argparse.ArgumentParser()
parser.add_argument('mac', type=validate_device_mac)
parser.add_argument('--backend', choices=['gatttool', 'bluepy'], default='gatttool')
parser.add_argument('-v', '--verbose', action='store_const', const=True)
args = parser.parse_args()

backend = None
if args.backend == 'gatttool':
    backend = GatttoolBackend
elif args.backend == 'bluepy':
    backend = BluepyBackend
else:
    raise Exception('unknown backend: {}'.format(args.backend))

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

poller = CuteCarePoller(args.mac, backend)

print("Getting data from CuteCare DIY sensor")
print("Name: {}".format(poller.name()))
print("Temperature: {}".format(poller.parameter_value()))
