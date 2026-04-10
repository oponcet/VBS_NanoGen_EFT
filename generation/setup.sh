#!/bin/bash

# Ensure this script runs inside a singularity/apptainer environment.
# If not, fail fast and suggest the expected cmssw-el8 entrypoint.
if [[ -z "${SINGULARITY_CONTAINER:-}" && -z "${APPTAINER_CONTAINER:-}" ]]; then
  echo "ERROR: This setup must be run inside singularity/apptainer."
  echo "Please start the cmssw-el8 environment first, then run this script again."
  echo "Example: cmssw-el8"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#if [ ! -d genproductions ]; then
#  git clone https://github.com/cms-sw/genproductions.git --depth 1
#fi

# in case this is not already done, setup cms packaging commands
. /cvmfs/cms.cern.ch/cmsset_default.sh
 export SCRAM_ARCH=el8_amd64_gcc11
if [ ! -d CMSSW_13_0_14 ]; then
  cmsrel CMSSW_13_0_14
  pushd CMSSW_13_0_14/src
  export SCRAM_ARCH=el8_amd64_gcc11
  cmsenv
  git cms-init

  git cms-addpkg PhysicsTools/NanoAOD
  cd PhysicsTools/NanoAOD/
  git remote add nanogen_EFT_CMSSW_13_0_X  git@github.com:mpresill/cmssw.git
  git fetch nanogen_EFT_CMSSW_13_0_X 
  git cherry-pick cf33242f486ae50977115efc66529b3da9108f42
  git cherry-pick 866e667dd33a332e93d9f22a43e592e8521d5d00
  git cherry-pick 4d651e49bb400dbe6a14778b8f03f8941097b4a4

  #cd ../../
  #git clone https://github.com/TopEFT/EFTGenReader.git
  #rm -rf EFTGenReader/GenReader/
  #rm -rf EFTGenReader/LHEReader/

  mkdir -p "${CMSSW_BASE}/src/Configuration/GenProduction/python/"
  cp -r "${SCRIPT_DIR}/fragments/"*.py "${CMSSW_BASE}/src/Configuration/GenProduction/python/"

  scram b -j 4
  popd
fi

# ensure environment if running again
pushd CMSSW_13_0_14/src && cmsenv && popd
