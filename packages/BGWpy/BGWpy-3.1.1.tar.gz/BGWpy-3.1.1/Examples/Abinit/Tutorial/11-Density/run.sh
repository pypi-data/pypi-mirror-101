#!/bin/bash



# Lines before execution
# can be multiple lines
# but they must be indented.
MPIRUN='mpirun -n 1 --npernode 1'
ABINIT='abinit'

$MPIRUN $ABINIT < GaAs.files &> GaAs.log


# Lines after execution
# can also be multiple lines.
