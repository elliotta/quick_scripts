#!/usr/bin/env python

import random
import copy
import argparse
import sys
import time

parser = argparse.ArgumentParser()
parser.description = 'Secret Santa!'
parser.add_argument('people', nargs='+', help='List of people')

args = parser.parse_args()

receivers = copy.copy(args.people)
random.seed(str(time.time()))

for person in args.people:
    rec = random.choice(receivers)
    if len(receivers) == 1 and person == rec:
        print 'Last person got stuck with themself. Try again...'
        sys.exit(1)
    while rec == person:
        rec = random.choice(receivers)
    receivers.remove(rec)
    print '%s will recieve from %s' % (rec, person)

