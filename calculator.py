#!/usr/bin/env python

import sys

UNIT = 1024.0

# Ensure command line arguments are given
if len(sys.argv) > 2:
    filename = sys.argv[1]
    heapsize = int(sys.argv[2]) * 1000
else:
    sys.stderr.write('Usage: <cfstats-output> <heapsize-in-GB>\n')
    sys.exit(0)


# Default memtable size is 1/3 of heapspace
memtable_total_space_in_mb = heapsize / 3.0


# Calculate Key Cache
with open(filename, 'r') as f:
    cfstats = f.read()

caches_read = False
key_cache_estimate = 0
row_cache_estimate = 0

for line in cfstats.split('\n'):
    needle = 'Key cache size:'
    if needle in line:
        caches_read = True
        key_cache_estimate += int(line.split(needle)[1])

    needle = 'Row cache size:'
    if needle in line:
        row_cache_estimate += int(line.split(needle)[1])

# For the difference in reported Java heap usage and actual size
key_cache_estimate *= 12
row_cache_estimate *= 12

# Bytes -> MegaBytes
key_cache_estimate /= UNIT
row_cache_estimate /= UNIT


# Print out the Calculated Heap Sizes
if caches_read:
    print 'Estimated Java Heap Size:'
    print '{0:.2f} GB'.format((memtable_total_space_in_mb + UNIT + key_cache_estimate) / UNIT)
else:
    print 'No caches found. Could not parse cfstats files.'

# Print another estimation if row cache is present
# May not be necessary since this off heap by default in 1.0+
if row_cache_estimate:
    print
    print 'Estimated Java Heap Size (w/Row Cache Sizes):'
    print '{0:.2f} GB'.format((memtable_total_space_in_mb + UNIT + key_cache_estimate + row_cache_estimate) / UNIT)
