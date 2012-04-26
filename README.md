Description
-----------

Calculates the heap space used by Apache Cassandra.

heapspace_calculator
--------------------

Needed to run are:

* The path a file containing the `nodetool cfstats` output
* The heapsize (in GB) for this cluster (can be found via `nodetool info`)
* The average key size (in bytes) (known by the user)
* The average row size (in bytes) (as found via `avg_row_size_calculator`)
* Optionally: The memtable size (in MB). Only to be set if changed from the
  defaults of 1/3 of the heap space. See `cassandra.yaml`.

avg_row_size_calculator
-----------------------

Takes the path to a file containing the `nodetool cfhistogram` output for all
column familes.
