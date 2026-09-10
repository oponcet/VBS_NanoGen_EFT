# WhadZBBJJ_LO_EWK — cross section

Documents how the production cross section of this sample was obtained and
cross-checked, and the final recommended number to use for normalization.

- **Process:** p p → W(→jj) Z(→bb̄) jj
- **Coupling order:** QED=4, QCD=0 (pure EW)
- **Gridpack:** `crab_submit_files/WhadZBBJJ_LO_EWK_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz`
- **CRAB task:** `crab_submit_files/crab_projects/crab_WhadZBBJJ_LO_EWK-NanoGEN/`

## Result

| Quantity | Value |
|---|---|
| **σ (recommended, genXsecAnalyzer)** | **0.05573 ± 0.00010 pb** (stat., ≈ 0.19%) |
| σ (MadGraph, inclusive p p → W Z j j) | 0.5512 ± 0.0012 pb (stat., ≈ 0.21%) |
| BR(W→jj) × BR(Z→bb̄) (MadSpin filter) | 0.101471 |
| σ (propagated cross-check) | 0.5512 × 0.101471 = 0.05593 pb |

The genXsecAnalyzer and propagated values agree within < 0.5% — consistent within
uncertainties.

**Use the genXsecAnalyzer value (0.05573 ± 0.00010 pb) for any physics normalization**
(luminosity weighting, yield predictions, etc.) — it's the CMS-recommended number
because it's measured directly on the events that were actually produced and
distributed, and correctly accounts for the MadSpin decay filter.

## Calculation scheme

### 1. MadGraph inclusive cross section (gridpack build time)

The gridpack's own integration of the phase space for the *inclusive* process
p p → W Z j j (before any forced decay) is computed once, when the gridpack is built,
via MadGraph's `survey` step (`--accuracy=0.01 --points=2000 --iterations=8`). This
number is stored in the LHE `<init>` block and is what appears in
`gridpack_generation.log`:

```
=== Results Summary for run: pilotrun tag: tag_1 ===
Cross-section :   0.5512 +- 0.001179 pb
```

This is **not** the cross section of the final state actually present in the produced
events — it's the cross section for W Z j j production *before* MadSpin restricts the
W and Z decay channels.

### 2. MadSpin decay branching ratio

MadSpin then forces W → jj (hadronic) and Z → bb̄ on top of the inclusive production,
discarding all other decay channels. The achieved branching fraction is reported once,
also in `gridpack_generation.log`:

```
INFO: Branching ratio to allowed decays: 0.101471
```

This matches the expected product of SM branching ratios:
BR(W→jj, hadronic) ≈ 0.676 × BR(Z→bb̄) ≈ 0.151 ≈ 0.102.

Multiplying the inclusive MadGraph cross section by this branching ratio gives the
expected *exclusive* cross section for the final state that ends up in the LHE/NanoGEN
events:

```
0.5512 pb × 0.101471 = 0.05593 pb
```

### 3. genXsecAnalyzer (CMSSW, measured on produced events)

`genXsecAnalyzer` (`process.genXSecAnalyzer = cms.EDAnalyzer("GenXSecAnalyzer")`) is
added to the NanoGEN cfg automatically by the
`Configuration/DataProcessing/Utils.addMonitoring` customization used in
`configs/WhadZBBJJ_LO_EWK_NanoGEN_cfg.py`. It runs once per CRAB job, re-derives the
cross section from the LHE weights of the events actually generated in that job, and
(where applicable) corrects for any generator-level filter efficiency — here
`filterEfficiency = 1.0`, so it's expected to converge to the same "exclusive" number as
step 2 above. Its result is printed at the end of each job's stdout log (not stored in
the ROOT output):

```
After filter: final cross section = 5.573e-02 +- 1.174e-03 pb   (example, single job)
```

### 4. Combining across all CRAB jobs

The recommended value is obtained by combining the per-job `genXsecAnalyzer` results
(one measurement per 100-event job, 100 jobs retrieved via
`results/cmsRun_*.log.tar.gz` → `crab getlog`) as an inverse-variance weighted mean:

```
σ_combined = Σ(σᵢ / δσᵢ²) / Σ(1 / δσᵢ²)
δσ_combined = 1 / √(Σ(1 / δσᵢ²))
```

| Method | Result |
|---|---|
| Inverse-variance weighted mean (100 jobs) | 0.055732 ± 0.000104 pb |
| Simple mean ± standard error on the mean (cross-check) | 0.055874 ± 0.000230 pb |

Both agree with each other and with the MadGraph × BR propagation (0.05593 pb),
confirming the chain is internally consistent (no hidden filter, no unit mismatch).

## How to reproduce

```sh
# Extract the per-job cross section lines from the CRAB job logs
RESULTS=crab_submit_files/crab_projects/crab_WhadZBBJJ_LO_EWK-NanoGEN/results
for f in "$RESULTS"/cmsRun_*.log.tar.gz; do
  tar -xzOf "$f" | grep "After filter: final cross section"
done > all_xsec.txt

# Combine with inverse-variance weighting (see script logic above)
```

If job logs aren't yet retrieved locally, fetch them first with:

```sh
crab getlog -d crab_submit_files/crab_projects/crab_WhadZBBJJ_LO_EWK-NanoGEN
```
