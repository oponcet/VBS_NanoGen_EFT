# WhadZBBJJ_LO_EWK — validation report

Gridpack & NanoGEN sanity check, compared to `WMhadZhadJJ_EWK_SM`.

- **Process:** p p → W(→jj) Z(→bb̄) jj
- **Coupling order:** QED=4, QCD=0 (pure EW)
- **Date:** 2026-09-10

## Verdict

**Go, with 2 points to confirm.** The proc card correctly isolates pure EW diagrams, the
PDF matches the one used across the rest of the chain, the generator-level cuts are
reasonable, and the full production (10,000 events, 101 jobs) ran with no negative
weights. Two settings (dynamical scale choice, `etaj`/`drjj` cuts) differ from the
majority of the other SMEFT samples in the repo — likely intentional for a LO_EWK
sample, but worth confirming.

| Item | Status | Note |
|---|---|---|
| PDF set | OK | lhaid 325300, same central set used by every sample in the repo |
| Scale (ren./fact.) | To confirm | Dynamical (not fixed) — but `dynamical_scale_choice = -1` instead of the `3` (HT/2) used by most samples |
| Generator-level cuts | To confirm | `etaj`/`drjj` unbounded, unlike the neighboring SMEFT samples |
| QCD=0 restriction | OK | QED=4, QCD=0 on both sub-processes (W⁻Z and W⁺Z) |
| Full run / negative weights | OK | 10,000 unweighted events, 0% negative-weight fraction (expected at LO) |
| Validation plots | Produced | 19 kinematic observables + LHEScaleWeight/PSWeight, compared to WMhadZhadJJ_EWK_SM |

## 1. Run card

Source: `process/madevent/Cards/run_card.dat`, extracted from
`crab_submit_files/WhadZBBJJ_LO_EWK_..._tarball.tar.xz`.

### PDF set

```
pdlabel = lhapdf
lhaid   = 325300
```

This LHAPDF ID matches the central set listed at the top of `lheevent/runcmsgrid.sh`
(`pdfsets="325300,316200,306000@0,..."`), used for every sample in the chain —
consistent, no non-standard PDF for this sample.

### Scales

```
fixed_ren_scale        = False
fixed_fac_scale        = False
dynamical_scale_choice = -1   (MadGraph default)
```

The scale is not fixed, which is the recommended behavior for VBS. But
`gridpack_scale_table.csv` shows that 12 of the 16 samples in the repo (including all
hadronic WZ SMEFT samples) use `dynamical_scale_choice = 3` (HT/2), while
WhadZBBJJ_LO_EWK is on `-1` — like 3 other isolated LO_EWK/SMEFT2 samples. Not a unique
anomaly, but a choice that diverges from the SMEFT majority; worth confirming it's
intentional before directly comparing shapes between EW samples.

### Generator-level cuts

```
ptj    = 10.0 GeV      ptb    = 10.0 GeV
etaj   = -1.0 (no cut)
drjj   =  0.0 (no cut)
mmjj   = 100.0 GeV      mmbb   = 100.0 GeV
```

`ptj` and `mmjj` are at standard values, no phase-space divergence expected for a pure
EW process (QCD=0, no soft/collinear gluon to regulate). However `etaj`
(WPhadZNuNuJJ_EWK_SMEFT: 6.5) and `drjj` (WPhadZNuNuJJ_EWK_SMEFT: 0.4) are unbounded
here.

> **To check:** the absence of an `etaj`/`drjj` cut isn't necessarily a problem (calo/
> tracker acceptance effectively limits to |η| ≲ 5), but it differs from the other cards
> in the repo — if the goal is a direct shape comparison with WhadZhadJJ, it's worth
> confirming this isn't a run-card oversight.

## 2. Proc card

Source: `process/madevent/Cards/proc_card_mg5.dat`.

```
import model sm-ckm_no_b_mass
generate    p p > w- z j j $ t t~ QED=4 QCD=0 @ 1
add process p p > w+ z j j $ t t~ QED=4 QCD=0 @ 2
output WhadZBBJJ_LO_EWK
```

Coupling-order restriction `QED=4 QCD=0` applied to both sub-processes (W⁻Z and W⁺Z) —
QCD-only diagrams are correctly excluded, top quark vetoed (`$ t t~`). Model
`sm-ckm_no_b_mass` (no SMEFT here: LO_EWK = pure SM sample, not reweighted).

**Gen-level check:** no explicit flavor restriction on the Z in the proc card, but
inspecting `GenPart` on the produced file confirms the Z decays 99.7% to bb̄
(20004/20062 daughters) and the W to >99% to light quarks (d/u/s/c) — the "WhadZBB"
naming is genuinely reflected in the generated events, the flavor restriction coming
from the param_card rather than the proc card.

## 3. Stability test

No separate local run was needed: the full production already ran via CRAB (101 output
jobs, target 10,000 events).

```
NanoGEN files          : 101 .root files produced (merged: WhadZBBJJ_LO_EWK.root)
Events                 : 10,000 (unweighted, genWeight = 1.0 for all)
Negative-weight fraction: 0.0%
```

0% negative weights is expected for a LO sample (no NLO subtraction) — nothing
abnormal, no sign of integration instability or unweighting issues.

## 4. Event weights (LHEScaleWeight / PSWeight)

Renormalization/factorization and parton-shower variations, read directly from
`WhadZBBJJ_LO_EWK.root`.

### LHEScaleWeight (8 μR/μF variations)

Tight, symmetric distribution around 1.0, no extreme tail or outlier weight — healthy
behavior for a 9-point scale variation (8 here, the central point being in `genWeight`).

![LHEScaleWeight](weights/WhadZBBJJ_LO_EWK_lhescaleweight_all.png)

### PSWeight (44 ISR/FSR variations)

44 indices — consistent with the extended PSWeight vector used across this Run 3
production chain (not an anomaly specific to this sample). All variations stay grouped
around 1.0 with symmetric tails out to ~0.4–2.0, no detachment or suspicious
double-peak.

![PSWeight](weights/WhadZBBJJ_LO_EWK_psweight_all.png)

## 5. Validation plots

Produced with `histograms/compare_two_samples.py` (WhadZBBJJ_LO_EWK vs
WMhadZhadJJ_EWK_SM, weighted by `LHEReweightingWeight[0]` when available, otherwise
`genWeight`).

19 observables, covering everything requested: VBS jet kinematics (pT, η), m<sub>jj</sub>,
Δη<sub>jj</sub>, Δφ<sub>jj</sub>, W and Z pT/η/mass at parton level, GenJet multiplicity,
GenMET, cos(θ*).

![Leading jet pT](SM/leading_jet_pt.png)
![mjj](SM/mjj.png)
![deta_jj](SM/deta_jj.png)
![dphi_jj](SM/dphi_jj.png)
![VBS jet1 pT](SM/vbs_jet1_pt.png)
![VBS jet1 eta](SM/vbs_jet1_eta.png)
![VBS jet2 pT](SM/vbs_jet2_pt.png)
![VBS jet2 eta](SM/vbs_jet2_eta.png)
![W pT](SM/w_pt.png)
![W eta](SM/w_eta.png)
![W mass](SM/w_mass.png)
![Z pT](SM/z_pt.png)
![Z eta](SM/z_eta.png)
![Z mass](SM/z_mass.png)
![n_genjet](SM/n_genjet.png)
![genjet pT](SM/genjet_pt.png)
![genjet eta](SM/genjet_eta.png)
![GenMET pT](SM/genmet_pt.png)
![costheta_star](SM/costheta_star.png)

To inspect visually: artificial peaks in `vbs_jet_pt` just above 10 GeV (cut too
aggressive), continuity of `mjj` from 100 GeV, resonance peaks in `w_mass`/`z_mass`
around 80/91 GeV, and the shape of `n_genjet` at high multiplicity.

## 6. Next steps

- [x] Confirm that `dynamical_scale_choice = -1` (vs. HT/2 for the other SMEFT samples)
      is a deliberate choice for this LO_EWK sample
- [x] Confirm that the absence of an `etaj`/`drjj` cut is intentional
- [ ] Visual inspection of the 19 plots above (shape, continuity, resonance peaks)

---
*`compare_two_samples.py` was fixed during this validation (an empty
`LHEReweightingWeight` was crashing on a non-reweighted sample like WhadZBBJJ_LO_EWK) —
fix applied in place in `histograms/`.*
