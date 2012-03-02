#!/usr/bin/env python

import sys

UNIT = 1024.0

# Ensure command line arguments are given
if len(sys.argv) > 3:
    filename = sys.argv[1]
    heapsize = int(sys.argv[2]) * UNIT
    avg_key_size = int(sys.argv[3])
else:
    sys.stderr.write('Usage: <cfstats-output> <heapsize-in-GB> <avg-key-size-in-Bytes> [<memtable-total-space-in-MB>]\n')
    sys.exit(0)

if len(sys.argv) > 4:
    memtable_total_space_in_mb = int(sys.argv[4])
else:
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
key_cache_estimate *= 12 * (avg_key_size + 64)
row_cache_estimate *= 12 * (avg_key_size + 64)

# Bytes -> KiloBytes -> MegaBytes
key_cache_estimate = key_cache_estimate / UNIT / UNIT
row_cache_estimate = row_cache_estimate / UNIT / UNIT


# Print out the Calculated Heap Sizes
if caches_read:
    print 'Estimated Java Heap Size:'
    print '{0:.2f} GB'.format((memtable_total_space_in_mb + UNIT + key_cache_estimate) / UNIT)
else:
    print 'No caches found. Could not parse cfstats files.'

# Print another estimation if row cache is present
# May not be necessary since this by default off heap in 1.0+
if row_cache_estimate:
    print
    print 'Estimated Java Heap Size (w/Row Cache Sizes):'
    print '{0:.2f} GB'.format((memtable_total_space_in_mb + UNIT + key_cache_estimate + row_cache_estimate) / UNIT)
