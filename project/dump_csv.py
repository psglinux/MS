#!/usr/bin/env python3
# Utility to dump out a CSV file

import csv
import pprint
import sys

if len(sys.argv) != 2:
    print("Usage" + sys.argv[0] + " < Path to CSV file >")
    exit(-1) 

with open(sys.argv[1], 'r') as csvFile:
    count = 0
    records_per_page = 4
    reader = csv.reader(csvFile)
    for row in reader:
        pprint.pprint(row)
        if count == records_per_page:
            input("Press Enter to continue...")
            count  = 0
        else:
            count += 1

csvFile.close()

