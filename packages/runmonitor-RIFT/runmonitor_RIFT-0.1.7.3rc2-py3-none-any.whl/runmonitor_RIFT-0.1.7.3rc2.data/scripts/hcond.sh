#!/bin/bash

#1 is the process id (jobid.retry #, e.g. 67422382.1)
#prints the last remote host (usually slot@node)

condor_history $1 -af LastRemoteHost -limit 1
