#!/bin/bash
#################################################################################
#
#  Environment script for DD4hep examples - initializes DD4hep (and ROOT)
#  for package: lcgeo
# 
#  @author F.Gaede, DESY, 2013
#  @author M.Frank, CERN, 2015
#
#################################################################################
# Default of DD4hep is the primary installation directory
if [ ! ${DD4hep_DIR} ]; then
    export DD4hep_DIR=/cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/v02-00-01/DD4hep/v01-07-01;
fi;
if [  ]; then
    export CLHEP_DIR=;
fi;
source ${DD4hep_DIR}/bin/thisdd4hep.sh;
#
dd4hep_parse_this ${BASH_ARGV[0]} lcgeo;
#
#----PATH---------------------------------------------------------------------
dd4hep_add_path    PATH ${THIS}/bin;
#----PYTHONPATH---------------------------------------------------------------
dd4hep_add_path    PYTHONPATH ${THIS}/lib/python;
#----ROOT_INCLUDE_PATH--------------------------------------------------------
dd4hep_add_path    ROOT_INCLUDE_PATH ${THIS}/include;
#----LIBRARY_PATH-------------------------------------------------------------
dd4hep_add_library_path ${THIS}/lib;
# -- need to extend dynamic search path for all external libraries:
if [  ]; then
    for lp in ; do
	dd4hep_add_library_path ${lp};
    done;
fi;
