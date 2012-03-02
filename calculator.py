#!/usr/bin/env python

import sys

# Ensure command line arguments are given
if len(sys.argv) > 2:
    filename = sys.argv[1]
    heapsize = int(sys.argv[2]) * 1000
else:
    sys.stderr.write('Usage: <filename> <heapsize-in-GB>\n')
    sys.exit(0)


# Default memtable size is 1/3 of heapspace
memtable_total_space_in_mb = heapsize / 3


# Calculate Key Cache
with open(filename, 'r') as f:
    cfstats = f.read()

key_cache_estimate = 0
row_cache_estimate = 0
for line in cfstats.split('\n'):
    needle = 'Key cache size:'
    if needle in line:
        key_cache_estimate += int(line.split(needle)[1])

    needle = 'Row cache size:'
    if needle in line:
        row_cache_estimate += int(line.split(needle)[1])

# For the difference in reported Java heap usage and actual size
key_cache_estimate *= 12
row_cache_estimate *= 12


# Print out the Calculated Heap Sizes
print 'Estimated Java Heap Size:'
print memtable_total_space_in_mb + 1000 + 0 + key_cache_estimate

# Print another estimation if row cache is present
# May not be necessary since this off heap by default in 1.0+
if row_cache_estimate:
    print
    print 'Estimated Java Heap Size (w/Row Cache Sizes):'
    print memtable_total_space_in_mb + 1000 + 0 + key_cache_estimate + row_cache_estimate
