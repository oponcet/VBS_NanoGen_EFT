# WhadZBBJJ_LO_QCD — validation report

Gridpack sanity check — QCD-induced companion to `WhadZBBJJ_LO_EWK`.

- **Process:** p p → W(→jj) Z(→bb̄) jj
- **Coupling order:** QED=2, QCD=99 (QCD-induced)
- **Date:** 2026-09-10
- **Source:** `/uscms_data/d3/oponcet1/VBS/gridpack_prod/genproductions_scripts/bin/MadGraph5_aMCatNLO/WhadZBBJJ_LO_QCD_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz`
- **CRAB task:** `crab_submit_files/crab_projects/crab_WhadZBBJJ_LO_QCD-NanoGEN/` (100/100 jobs completed)

## Verdict

**Go.** Cards, decay filter, stability and full-scale production all check out. The
proc card and run card are consistent with the already-validated EWK sample (same PDF,
same cuts, same scale choice), and correctly confirm the expected QCD-induced process.
The full CRAB production (100 jobs, 10,000 events) completed with 0% negative weights,
and the recommended cross section has been measured directly with `genXsecAnalyzer` on
the produced events: **1.4656 ± 0.0019 pb**. Kinematic and weight validation plots have
been produced and compared against the EWK companion sample.

| Item | Status | Note |
|---|---|---|
| PDF set | OK | lhaid 325300 — identical to WhadZBBJJ_LO_EWK and the rest of the chain |
| Scale (ren./fact.) | Consistent | Dynamical, `dynamical_scale_choice = -1` — same as the LO_EWK version |
| Generator-level cuts | Consistent | ptj/etaj/drjj/mmjj/ptb/mmbb identical to the LO_EWK version |
| Coupling order | OK | QED=2, QCD=99 — QCD-induced diagrams enabled (complementary to the EWK sample's QCD=0) |
| Full NanoGEN production | OK | 100/100 CRAB jobs completed, 10,000 events merged |
| Negative-weight fraction | OK | 0.0% on the full merged sample (unweighted LO events) |
| Cross section | OK | 1.4656 ± 0.0019 pb (genXsecAnalyzer, combined over 100 jobs) — see [cross-section doc](WhadZBBJJ_LO_QCD_cross_section.md) |
| Validation plots | Produced | 19 kinematic observables (vs. WhadZBBJJ_LO_EWK) + LHEScaleWeight/PSWeight |

## 1. Run card

Source: `process/madevent/Cards/run_card.dat`, extracted from
`WhadZBBJJ_LO_QCD_..._tarball.tar.xz`.

### PDF set & scales

```
pdlabel / lhaid          = lhapdf / 325300   (= LO_EWK)
fixed_ren_scale          = False
fixed_fac_scale          = False
dynamical_scale_choice   = -1                (= LO_EWK)
```

Same PDF/scale settings as the already-validated LO_EWK version — internal consistency
between the two complementary samples (needed to add or compare EWK and QCD-induced
contributions without a convention bias).

### Generator-level cuts

```
ptj    = 10.0 GeV      ptb    = 10.0 GeV
etaj   = -1.0 (no cut)
drjj   =  0.0 (no cut)
mmjj   = 100.0 GeV      mmbb   = 100.0 GeV
xqcut  =  0.0
```

Identical, value for value, to the LO_EWK version. Same caveat as before: `etaj`/`drjj`
are unbounded — consistent between the two samples, but still worth confirming as an
intentional choice.

## 2. Proc card

Source: `process/madevent/Cards/proc_card_mg5.dat`.

```
import model sm-ckm_no_b_mass
generate    p p > w- z j j $ t t~ QED=2 QCD=99 @ 1
add process p p > w+ z j j $ t t~ QED=2 QCD=99 @ 2
output WhadZBBJJ_LO_QCD
```

`QED=2 QCD=99` (instead of `QED=4 QCD=0` for the EWK version): minimal EW coupling
(just enough for W/Z), QCD unrestricted — this is indeed the complementary QCD-induced
sample, not a duplicate of the EWK one. Top vetoed (`$ t t~`) as in the EWK version.

**Check from the pilot run (1000 events, build log):** the explicit decays `w+ > j j`,
`w- > j j`, `z > b b~` appear in the MadSpin log
(`generate p p > w- z j j ... , w+ > j j, w- > j j, z > b b~ ...`) — confirmed too by
PDG-code counting on the final-state particles: b-quark (pdg 5) present ~2×/event
(Z→bb̄), plus light quarks/gluons from W→jj and genuine QCD radiation. MadSpin-reported
branching ratio: 0.1015, consistent with BR(W→jj)≈0.676 × BR(Z→bb̄)≈0.151.

## 3. Stability

### Gridpack build pilot run (1000 events)

```
Cross-section (survey)   : 14.53 ± 0.028 pb
Pilot events              : 1000 (unweighted_events_decayed.lhe.gz)
Negative-weight fraction  : 0.0%
MadSpin — weights > max   : 0 events
```

### Full CRAB production (10,000 events)

```
Jobs completed             : 100 / 100
Events                     : 10,000 (unweighted, genWeight = 1.0 for all)
Negative-weight fraction   : 0.0%
```

0% negative weights on both the pilot run and the full production — healthy behavior,
same as the LO_EWK version, as expected for an unweighted LO sample.

## 4. Cross section

Measured directly with `genXsecAnalyzer` on the full production (100 job logs,
inverse-variance weighted combination):

```
σ = 1.4656 ± 0.0019 pb   (stat., ≈ 0.13%)
```

Cross-checked against the MadGraph inclusive cross section × MadSpin branching ratio:
`14.53 pb × 0.101471 = 1.474 pb` — agreement within 0.6%.

Full derivation, per-job breakdown and reproduction commands:
[`WhadZBBJJ_LO_QCD_cross_section.md`](WhadZBBJJ_LO_QCD_cross_section.md).

## 5. Validation plots

### Kinematics (vs. WhadZBBJJ_LO_EWK)

Produced with `histograms/compare_two_samples.py`, comparing the QCD-induced and
EWK-induced samples for the *same* final state (W had × Z→bb̄), to isolate the effect
of the coupling-order restriction rather than compare to a different process. 19
observables: VBS jet kinematics (pT, η), m<sub>jj</sub>, Δη<sub>jj</sub>, Δφ<sub>jj</sub>,
W and Z pT/η/mass, GenJet multiplicity, GenMET, cos(θ*).

![mjj](QCD_vs_EWK/mjj.png)
![deta_jj](QCD_vs_EWK/deta_jj.png)
![dphi_jj](QCD_vs_EWK/dphi_jj.png)
![leading jet pT](QCD_vs_EWK/leading_jet_pt.png)
![VBS jet1 pT](QCD_vs_EWK/vbs_jet1_pt.png)
![VBS jet1 eta](QCD_vs_EWK/vbs_jet1_eta.png)
![VBS jet2 pT](QCD_vs_EWK/vbs_jet2_pt.png)
![VBS jet2 eta](QCD_vs_EWK/vbs_jet2_eta.png)
![W pT](QCD_vs_EWK/w_pt.png)
![W eta](QCD_vs_EWK/w_eta.png)
![W mass](QCD_vs_EWK/w_mass.png)
![Z pT](QCD_vs_EWK/z_pt.png)
![Z eta](QCD_vs_EWK/z_eta.png)
![Z mass](QCD_vs_EWK/z_mass.png)
![n_genjet](QCD_vs_EWK/n_genjet.png)
![genjet pT](QCD_vs_EWK/genjet_pt.png)
![genjet eta](QCD_vs_EWK/genjet_eta.png)
![GenMET pT](QCD_vs_EWK/genmet_pt.png)
![costheta_star](QCD_vs_EWK/costheta_star.png)

**Visual inspection findings:**

- **`mjj.png`** — the QCD-induced sample peaks sharply at low m<sub>jj</sub>
  (~150–350 GeV) and falls off quickly, while the EWK sample keeps a broad tail out to
  high mass — exactly the expected signature (central QCD production vs. the
  large-separation, high-mass VBS topology).
- **`deta_jj.png`** — textbook VBS discriminant: the QCD sample falls steeply from
  Δη<sub>jj</sub>=0, while the EWK sample stays nearly flat out to Δη<sub>jj</sub>≈4
  before falling — the classic large-Δη VBS signature, cleanly reproduced.
- **`vbs_jet1_pt.png` / `vbs_jet2_pt.png`** — both samples rise smoothly from the 10 GeV
  `ptj` threshold with no artificial spike or discontinuity right above the cut (would
  indicate an overly aggressive generator cut) — the EWK jets are visibly harder
  (longer tail) than the softer QCD-radiation jets, as expected.
- **`w_mass.png` / `z_mass.png`** — clean, identical resonance peaks at ≈80 GeV (W) and
  ≈91 GeV (Z) for both samples (decay kinematics don't depend on the production
  mechanism) — confirms the resonances are generated correctly.
- **`n_genjet.png`** — no divergent tail at high jet multiplicity in either sample.

No shape anomaly, discontinuity, or artificial cutoff spike found in any of the 19
plots.

### Event weights

Produced with the same approach as for the EWK sample (`histograms/lhescale_plot.py`
logic, split into separate LHEScaleWeight/PSWeight plots for readability):

![LHEScaleWeight](weights_qcd/WhadZBBJJ_LO_QCD_lhescaleweight_all.png)
![PSWeight](weights_qcd/WhadZBBJJ_LO_QCD_psweight_all.png)

- **LHEScaleWeight** (8 μR/μF variations): broader spread than the EWK sample
  (roughly 0.75–1.35 vs. a tight peak around 1.0), consistent with QCD couplings being
  more scale-sensitive than the pure-EW process — no extreme outlier or divergent tail.
- **PSWeight** (44 ISR/FSR variations): same healthy pattern as the EWK sample, all
  grouped around 1.0 with symmetric tails, no anomaly.

## 6. Next steps

- [x] Check PDF/scale/cut consistency with the LO_EWK version
- [x] Check the coupling-order restriction (QED=2, QCD=99) and the forced W→jj/Z→bb̄
      decay
- [x] Check negative weights on the pilot run (1000 events) and the full production
      (10,000 events)
- [x] Launch and complete the full NanoGEN production (CRAB, 100/100 jobs)
- [x] Measure the official cross section with `genXsecAnalyzer`
- [x] Produce the kinematic and weight validation plots
- [x] Visual inspection of the 19 kinematic plots (shape, continuity, resonance peaks)
      — no anomaly found, see findings above

---
*NanoGEN files were merged from the 100 CRAB job outputs via `uproot`/`awkward`
directly (`hadd`/ROOT were not available in this environment) —
`nanogen_files/hadronic/WhadZBBJJ_LO_QCD/WhadZBBJJ_LO_QCD.root`, verified to load
correctly with `NanoAODSchema`.*
