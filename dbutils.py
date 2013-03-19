#!/usr/bin/env python
import argparse
from trx.utilities import db
from trx.seedDB import seed

parser = argparse.ArgumentParser(description='T-Rx database utility tool')
#Reset
parser.add_argument('-r', '--reset', action='store_true', default=False, \
                    help="Reset entire database. Use wisely.")
#Verbose
parser.add_argument('-v', '--verbose', action='store_true', default=False, \
                    help="Verbose mode")
#Input File
#parser.add_argument('-i', '--input', action='store_const')

args = parser.parse_args()
verbose = args.verbose

def reset():
    if verbose:
        print("Dropping tables...")
    #Destroy and recreate database
    db.drop_all()
    if verbose:
        print("Creating all tables...")
    db.create_all()
    if verbose:
        print ("Reset is complete.")


if args.reset:
    reset()
