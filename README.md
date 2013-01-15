Description
-----------

Calculates the heap space used by Apache Cassandra.

Setup
-----

To run `heapspace_calculator1.1` you must first run:

    pip install pyyaml

heapspace_calculator
--------------------

Needed to run are:

* The path a file containing the `nodetool cfstats` output
* The path to cassandra.yaml
* The heapsize (in GB) for this cluster (can be found via `nodetool info`)
* The average key size (in bytes) (known by the user)

heapspace_calculator1.0
-----------------------

Needed to run are:

* The path a file containing the `nodetool cfstats` output
* The heapsize (in GB) for this cluster (can be found via `nodetool info`)
* The average key size (in bytes) (known by the user)
* The average row size (in bytes) (as found via `avg_row_size_calculator`)
* Optionally: The memtable size (in MB). Only to be set if changed from the
  defaults of 1/3 of the heap space. See `cassandra.yaml`.

avg_row_size_calculator
-----------------------

Takes the path to a file containing the
`nodetool cfhistograms <keyspace> <cfname>` output for all column familes.
