# DD4HEP

A repository for work on SiD for use with the DD4hep toolkit, started by Gabriel Penn as a summer student in 2016. Please feel free to direct any queries to gp13181@bristol.ac.uk.

# Directories:
 - init: initialisation scripts for environment setup
 - compact: detector descriptions (adapted from the SiD description included with lcgeo)
 - particlegun: particle gun scripts for ddsim and the LCIO particle input files they generate
 - reco: reconstruction steering files for Marlin
 - analysis: pyLCIO analysis scripts, adapted from Josh Tingey's pixel studies (see pixelStudies repo)
 - auto: miscellaneous shell scripts for submitting multiple jobs

# Getting started
These instructions assume you are SSHing to a UoB SL6 machine (e.g. Soolin) with access to cvmfs. ILCSoft libraries are available on cvmfs, so you will not need to install DD4hep, LCIO, Marlin etc locally.

These instructions are based on [those provided by Dr Aidan Robson (Glasgow)](https://twiki.ppe.gla.ac.uk/bin/view/LinearCollider/GlaSiDGettingStarted), which you may find to be more up-to-date but less tailored to our setups.

## Installing lcgeo
Start by setting up your environment:
```
source /cvmfs/sft.cern.ch/lcg/releases/gcc/4.8.4/x86_64-slc6/setup.sh
source /cvmfs/ilc.desy.de/sw/x86_64_gcc48_sl6/v01-17-09/init_ilcsoft.sh
```

Navigate to the directory in which you wish to install lcgeo (I recommend your home directory) and checkout the source code:
```
cd ~
svn co https://svnsrv.desy.de/basic/ddsim/lcgeo/trunk lcgeo
```
Remove some unfinished(?) calorimeter files:
```
rm lcgeo/detector/calorimeter/SHcal*
rm lcgeo/detector/calorimeter/SEcal*
rm lcgeo/detector/CaloTB/CaloPrototype*
```
Create the build directory and move to it:
```
mkdir build
cd build
```
Make the installation:
```
cmake -DCMAKE_CXX_COMPILER=`which g++` -DCMAKE_C_COMPILER=`which gcc` -C /cvmfs/ilc.desy.de/sw/x86_64_gcc48_sl6/ILCSoft.cmake ..
make -j4
make install
```
If this runs without throwing any errors, you should now be able to run the example simulation.
## Running an example sim
In a clean login shell, navigate to your lcgeo directory and initialise your environment (see below):
```
cd ~/lcgeo
source __path to your local copy of this repository__/summer-student/init/init_master.sh
```
Run the example particle gun script:
```
python example/lcio_particle_gun.py
```
Run the simulation with the default geometry and the example input particles you have just generated:
```
ddsim --compactFile=SiD/compact/SiD_o1_v01/SiD_o1_v01.xml --runType=batch --inputFile mcparticles.slcio -N=1 --outputFile=testSiD_o1_v01.slcio
```
If this has worked, you will now have a file named testSiD_o1_v01.slcio. You can find out what data this output file contains in summary:
```
anajob testSiD_o1_v01.slcio
```
or in full detail:
```
dumpevent testSiD_o1_v01.slcio 1
```
You should now be ready to try running a reconstruction.

## Running an example reconstruction

Now navigate into your local summer-student repository and find SiDReconstruction_test160628.xml. You will need to edit this file so that the relevant file paths are correct for your local files. The LCIO input file is the 'testSiD_o1_v01.slcio' you just generated. For the compact files, you can use either those in lcgeo/SiD or in summer-student/compact. You can then run the reconstruction:
```
Marlin SiDReconstruction_test160628.xml
```
(Don't worry about the ECal errors: this part of the reconstruction is still under development.)

You should now have a file named 'sitracks.slcio' that you can run anajob on (as above) to check its contents.

# Running the chain

Here are some general instructions for running the simulatiom->reconstruction->analysis chain. First off, you will need to set up your environment: I have provided a master initialisation script for this purpose, init/init_master_new.sh.

## Generating input particles

For simple input events (e.g. test muons), modify a copy of lcio_particle_gun.py to generate the desired particles. It should be fairly straightforward to figure out how to change the particle type, momentum, angular distribution etc. You may wish to store your particle gun scripts and lcio files in summer-student/particles.

For more complicated events (e.g. an ILC collision), you may need to seek out ready-made input files. Older ones may use the .stdhep format, which should be compatible but may cause problems in some cases.

## Running a simulation

From within the summer-student directory, run the following:

```
ddsim --compactFile=compact/[GEOMETRY] --runType=batch --inputFile=[INPUT PATH] -N=[EVENTS] --outputFile=[OUTPUT PATH]
```
 - [GEOMETRY]: the path to the master .xml file for the chosen geometry
 - [INPUT PATH]: the path to the .slcio file containing the input particles
 - [EVENTS]: the desired number of events (you will of course need to have enough events in the input file!)
 - [OUTPUT PATH]: the path to the desired output file (must be .slcio)

This will simulate the events, which can then be reconstructed.

## Reconstructing events

You will need to write a .xml steering file for use with the Marlin reconstruction software. I recommend modifying reco/SiDReconstruction_test160628.xml by changing the following parameters:
 - LCIOInputFiles: path to the input file (the simulation output file)
 - DD4hepXMLFile: path to the master geometry file - this MUST be the same one that was used for the simulation
 - Under InnerPlanarDigiProcessor, ResolutionU and ResolutionV: the tracker's resolution in the u and v directions (change these e.g. to approximate pixels)
 - LCIOOutputFile: path to the desired output file.
 
Then run your reconstruction using Marlin, e.g.

```
Marlin example.xml
```

This will produce a final .slcio file containing the reconstructed tracks, which can then be analysed.

# Analysis

Analysis scripts written by Josh Tingey can be found in the analysis directory. See analysis/README.md for information and instructions. (Note: compatibility work on Josh's scripts is still a work in progress.)
