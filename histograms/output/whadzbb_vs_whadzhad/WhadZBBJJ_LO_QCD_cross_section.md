# WhadZBBJJ_LO_QCD — cross section

Documents how the production cross section of this sample was obtained and
cross-checked, and the final recommended number to use for normalization.

- **Process:** p p → W(→jj) Z(→bb̄) jj
- **Coupling order:** QED=2, QCD=99 (QCD-induced)
- **Gridpack:** `crab_submit_files/WhadZBBJJ_LO_QCD_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz`
- **CRAB task:** `crab_submit_files/crab_projects/crab_WhadZBBJJ_LO_QCD-NanoGEN/`

## Result

| Quantity | Value |
|---|---|
| **σ (recommended, genXsecAnalyzer)** | **1.4656 ± 0.0019 pb** (stat., ≈ 0.13%) |
| σ (MadGraph, inclusive p p → W Z j j) | 14.53 ± 0.0276 pb (stat., ≈ 0.19%) |
| BR(W→jj) × BR(Z→bb̄) (MadSpin filter) | 0.101471 (same filter as the EWK sample) |
| σ (propagated cross-check) | 14.53 × 0.101471 = 1.474 pb |

The genXsecAnalyzer and propagated values agree within < 0.6% — consistent within
uncertainties.

**Use the genXsecAnalyzer value (1.4656 ± 0.0019 pb) for any physics normalization**
(luminosity weighting, yield predictions, etc.) — it's the CMS-recommended number
because it's measured directly on the events that were actually produced and
distributed, and correctly accounts for the MadSpin decay filter.

## Calculation scheme

Same scheme as [`WhadZBBJJ_LO_EWK_cross_section.md`](WhadZBBJJ_LO_EWK_cross_section.md);
summarized here for this sample.

### 1. MadGraph inclusive cross section (gridpack build time)

From `gridpack_generation.log` (`survey` step, `--accuracy=0.01 --points=2000
--iterations=8`):

```
=== Results Summary for run: pilotrun tag: tag_1 ===
Cross-section :   14.53 +- 0.02756 pb
```

This is the cross section of the *inclusive* QCD-induced p p → W Z j j production,
before MadSpin restricts the W/Z decay channels.

### 2. MadSpin decay branching ratio

Same decay filter as the EWK companion sample (W → jj hadronic, Z → bb̄), reported in
the same log:

```
INFO: Branching ratio to allowed decays: 0.101471
```

Propagated exclusive cross section:

```
14.53 pb × 0.101471 = 1.474 pb
```

### 3. genXsecAnalyzer (CMSSW, measured on produced events)

Added automatically by `Configuration/DataProcessing/Utils.addMonitoring` in
`configs/WhadZBBJJ_LO_QCD_NanoGEN_cfg.py`, runs once per CRAB job
(`filterEfficiency = 1.0`, no additional generator-level filter). Example single-job
result:

```
After filter: final cross section = 1.411e+00 +- 1.674e-02 pb   (example, single job)
```

### 4. Combining across all CRAB jobs

Inverse-variance weighted mean over the 100 retrieved job logs
(`results/cmsRun_*.log.tar.gz`, ~10,000 events total):

```
σ_combined = Σ(σᵢ / δσᵢ²) / Σ(1 / δσᵢ²)
δσ_combined = 1 / √(Σ(1 / δσᵢ²))
```

| Method | Result |
|---|---|
| Inverse-variance weighted mean (100 jobs) | 1.46563 ± 0.00187 pb |
| Simple mean ± standard error on the mean (cross-check) | 1.46967 ± 0.00772 pb |

The simple-mean uncertainty is larger than the weighted one because job-to-job spread
is larger here than for the EWK sample — expected, since the QCD-induced process
carries genuine extra real-emission/radiation contributions (more gluons/light quarks
in the final state per event), giving a broader per-job weight distribution than the
QCD=0 EWK sample. Both methods still agree with the MadGraph × BR propagation
(1.474 pb).

## Comparison to the EWK companion sample

| Sample | σ genXsecAnalyzer (final, exclusive W had × Z→bb̄) |
|---|---|
| [WhadZBBJJ_LO_EWK](WhadZBBJJ_LO_EWK_cross_section.md) | 0.05573 ± 0.00010 pb |
| WhadZBBJJ_LO_QCD | 1.4656 ± 0.0019 pb |

QCD/EWK ratio ≈ 26.3, consistent with the ratio already visible at the MadGraph level
(14.53 / 0.5512 ≈ 26.4) — the coupling-order restriction (QED=2,QCD=99 vs QED=4,QCD=0)
is the only thing driving the difference, not the decay filter (identical BR for both).

## How to reproduce

```sh
# Extract the per-job cross section lines from the CRAB job logs
RESULTS=crab_submit_files/crab_projects/crab_WhadZBBJJ_LO_QCD-NanoGEN/results
for f in "$RESULTS"/cmsRun_*.log.tar.gz; do
  tar -xzOf "$f" | grep "After filter: final cross section"
done > all_xsec_qcd.txt

# Combine with inverse-variance weighting (see script logic above)
```

If job logs aren't yet retrieved locally, fetch them first with:

```sh
crab getlog -d crab_submit_files/crab_projects/crab_WhadZBBJJ_LO_QCD-NanoGEN
```
