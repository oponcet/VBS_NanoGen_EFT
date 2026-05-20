"""Compare generator-level observables between EFT (all reweighting weights) and EWK samples."""

import argparse
import os
import awkward as ak
import numpy as np

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

from histogram_utils import (
    build_weighted_observable_histogram,
    get_z_boson_pt,
    plot_ratio_histograms,
    get_mVV,
    get_leading_jet_pt,
    get_mjj,
    get_deta_jj,
    get_costheta_star,
)


DEFAULT_INPUT_EFT = "/uscms_data/d3/oponcet1/VBS/VBS_NanoGen_EFT/generation/WMhadZlepJJ_EWK_SMEFT_nanogen_123.root"
# DEFAULT_INPUT_EWK = "/uscms_data/d3/oponcet1/VBS/VBS_NanoGen_EFT/generation/wpzjjdim6_ewk_99.root"
DEFAULT_INPUT_EWK = "root://eosuser.cern.ch//eos/cms/store/group/phys_smp/VJets_NLO_VBSanalyses/Samples/NanoAOD/SMEFT/wmzjj_dim6_ewk/2018/wmzjjdim6_ewk_0.root"


OBSERVABLES = {
    "z_pt": {
        "func": get_z_boson_pt,
        "bins": (50, 0, 500),
        "label": "Z pT (GeV)",
    },
    "mVV": {
        "func": get_mVV,
        "bins": (50, 0, 2000),
        "label": "mWW (GeV)",
    },
    "leading_jet_pt": {
        "func": get_leading_jet_pt,
        "bins": (50, 0, 1000),
        "label": "Leading jet pT (GeV)",
    },
    "mjj": {
        "func": get_mjj,
        "bins": (50, 0, 3000),
        "label": "mjj (GeV)",
    },
    "deta_jj": {
        "func": get_deta_jj,
        "bins": (50, 0, 8),
        "label": r"delta eta(jj)",
    },
    "cos_theta_star": {
        "func": get_costheta_star,
        "bins": (50, -1, 1),
        "label": r"cos theta*",
    },  
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare generator-level observables for all EFT reweighting weights.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--input-eft", default=DEFAULT_INPUT_EFT)
    parser.add_argument("--input-ewk", default=DEFAULT_INPUT_EWK)
    parser.add_argument("--tree", default="Events")
    parser.add_argument("--output", default="comparison_multiobs")

    return parser.parse_args()


def load_events(input_path, tree_name):
    if ":" in input_path and not input_path.startswith("root://"):
        filespec = input_path
    else:
        filespec = f"{input_path}:{tree_name}"

    return NanoEventsFactory.from_root(
        filespec,
        schemaclass=NanoAODSchema,
    ).events()


def get_output_paths(output_arg):
    return f"{output_arg}.root", output_arg


def main():

    print("\n" + "=" * 80)
    print("WARNING: assumes LHEReweightingWeight[0] = SM")
    print("=" * 80 + "\n")

    args = parse_args()

    print("Loading samples...")
    events_eft = load_events(args.input_eft, args.tree)
    events_ewk = load_events(args.input_ewk, args.tree)

    # EFT weights
    if "LHEReweightingWeight" not in events_eft.fields:
        raise RuntimeError("No LHEReweightingWeight found")

    lhe_weights = events_eft.LHEReweightingWeight
    n_weights = int(ak.num(lhe_weights, axis=1)[0])

    print(f"Number of LHE weights: {n_weights}")

    histograms_all = {}

    root_output, plot_base = get_output_paths(args.output)

    with __import__("uproot").recreate(root_output) as root_file:

        for obs_name, cfg in OBSERVABLES.items():

            print(f"\nProcessing observable: {obs_name}")

            func = cfg["func"]
            n_bins, x_min, x_max = cfg["bins"]
            label = cfg["label"]

            values_eft = ak.to_numpy(func(events_eft))
            values_ewk = ak.to_numpy(func(events_ewk))

            mask_eft = values_eft > 0
            mask_ewk = values_ewk > 0

            values_eft = values_eft[mask_eft]
            values_ewk = values_ewk[mask_ewk]

            weights_ewk = np.ones_like(values_ewk)

            lhe_weights_obs = lhe_weights[mask_eft]

            sm_weights = ak.to_numpy(
                ak.fill_none(lhe_weights_obs[:, 0], 1.0)
            )

            histograms = {}

            # SM
            hist_sm = build_weighted_observable_histogram(
                values_eft,
                sm_weights,
                f"{obs_name} (SM)",
                n_bins=n_bins,
                x_min=x_min,
                x_max=x_max,
            )

            # EWK
            hist_ewk = build_weighted_observable_histogram(
                values_ewk,
                weights_ewk,
                f"{obs_name} (EWK)",
                n_bins=n_bins,
                x_min=x_min,
                x_max=x_max,
            )

            histograms["SM"] = hist_sm
            histograms["EWK"] = hist_ewk

            # EFT weights
            for i in range(n_weights):
                weights_i = ak.to_numpy(
                    ak.fill_none(lhe_weights_obs[:, i], 1.0)
                )

                hist_i = build_weighted_observable_histogram(
                    values_eft,
                    weights_i,
                    f"{obs_name} (weight {i})",
                    n_bins=n_bins,
                    x_min=x_min,
                    x_max=x_max,
                )

                histograms[f"weight_{i}"] = hist_i

            # Save ROOT
            for name, hist in histograms.items():
                root_file[f"{obs_name}_{name}"] = hist
            print("Saved root histo")
            
            # Ratio plots n_weights or 5 first 
            for i in range(1):
                output_file = f"{plot_base}_{obs_name}_weight_{i}.png"

                plot_ratio_histograms(
                    histograms[f"weight_{i}"],
                    hist_ewk,
                    output_file,
                    title=f"{label} (weight {i} / SM)",
                    hist_numerator_title=f"{obs_name}_weight_{i}",
                )

            print(f"Finished {obs_name}")

    print("\nAll observables processed.")


if __name__ == "__main__":
    main()