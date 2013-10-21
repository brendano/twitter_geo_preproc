#!/bin/bash
#Local testing versions
# export LD_LIBRARY_PATH=$HOME/geo2/occ_env/lib
# export PYTHONPATH=$HOME/geo2/preproc8:$HOME/geo2/geocode
# export PYTHONPATH=..

set -eux
export LD_LIBRARY_PATH=occ_env/lib
#Worker node setup
tar xf stuff.tar
source profile
hadoop dfs -get /user/brendano/geodata.tar .
hadoop dfs -get /user/brendano/occ_env.tar .
tar xf occ_env.tar
tar xf geodata.tar

occ_env/bin/python do_geocoding.py
