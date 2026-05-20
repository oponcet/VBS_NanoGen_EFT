# CRAB submission

## Run-3 NanoGEN from gridpack (SMP-Run3Summer23wmLHEGS-00186 style)

This repository now includes:

- CRAB submit file: `crab_submit_SMP-Run3Summer23wmLHEGS-00186_NanoGEN.py`
- CMSSW cfg used by CRAB: `../configs/SMP-Run3Summer23wmLHEGS-00186_NanoGEN_cfg.py`

### 1) Setup your CMSSW environment

Use the same patched setup described in the main README. From repo root:

```bash
cd generation
cmssw-el8
. setup.sh
```

This prepares the patched CMSSW area needed to keep EFT/LHE weights as expected.

### 2) Update site/user specific settings in the CRAB submit file

Edit:

- `config.General.requestName`
- `config.Data.outLFNDirBase`
- `config.Site.storageSite`
- optionally `unitsPerJob`/`NJOBS` depending on your target statistics

If needed, update the gridpack path in:

- `configs/SMP-Run3Summer23wmLHEGS-00186_NanoGEN_cfg.py`
  (`process.externalLHEProducer.args`)

### 3) Submit

From `crab_submit_files/`:

```bash
crab submit -c crab_submit_SMP-Run3Summer23wmLHEGS-00186_NanoGEN.py
```

### 4) Monitor and retrieve outputs

```bash
crab status -d crab_projects/SMP-Run3Summer23wmLHEGS-00186-NanoGEN
crab resubmit -d crab_projects/SMP-Run3Summer23wmLHEGS-00186-NanoGEN
crab getoutput -d crab_projects/SMP-Run3Summer23wmLHEGS-00186-NanoGEN
```
