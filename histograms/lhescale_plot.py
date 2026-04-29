"""Plot LHEScaleWeight histograms by index from NanoAOD files."""

import argparse
import os
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

from histogram_utils import (
    make_lhe_scale_weight_histograms,
    make_ps_weight_histograms,
    save_histograms_to_root,
    plot_histograms,
)

DEFAULT_INPUT = "/eos/cms/store/mc/RunIII2024Summer24NanoAODv15/WWJJto2L2Nu-SS-noTop-EWK_TuneCP5_13p6TeV_madgraph-pythia8/NANOAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/8cf320a1-9366-4c73-be61-e61c85c7f93e.root"


def parse_args():
    """Parse command-line arguments."""
    examples = (
        "Examples:\n"
        "  python lhescale_plot.py\n"
        "  python lhescale_plot.py --input /eos/cms/store/.../file.root\n"
        "  python lhescale_plot.py --input root://xrootd-cms.infn.it///store/.../file.root\n"
        "  python lhescale_plot.py --input /path/to/custom.root --tree Events\n"
        "  python lhescale_plot.py --output my_lheweights"
    )
    parser = argparse.ArgumentParser(
        description="Plot LHEScaleWeight histograms by index from NanoAOD files.",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Input ROOT file path (local, /eos/..., or root://...)",
    )
    parser.add_argument(
        "--tree",
        default="Events",
        help="TTree name to read (default: Events)",
    )
    parser.add_argument(
        "--output",
        default="lhescaleweight_by_index",
        help="Output basename for files (writes <name>.root and <name>.png)",
    )
    return parser.parse_args()


def load_events(input_path, tree_name):
    """Load NanoAOD events from a ROOT file."""
    if ":" in input_path and not input_path.startswith("root://"):
        filespec = input_path
    else:
        filespec = f"{input_path}:{tree_name}"

    try:
        return NanoEventsFactory.from_root(
            filespec,
            schemaclass=NanoAODSchema,
        ).events()
    except ImportError as exc:
        if input_path.startswith("root://"):
            raise SystemExit(
                "Missing xrootd dependencies for root:// access. Install in your env: "
                "pip install fsspec-xrootd XRootD"
            ) from exc
        raise
    except OSError as exc:
        msg = str(exc)
        if input_path.startswith("root://") and "Operation expired" in msg:
            raise SystemExit(
                "XRootD open timed out, usually due to missing/expired credentials. "
                "Run `voms-proxy-init -voms cms` (or renew your proxy), then retry."
            ) from exc
        raise


def get_output_paths(output_arg):
    """Parse output argument and return .root and .png paths."""
    output_base, output_ext = os.path.splitext(output_arg)
    if output_ext in (".root", ".png"):
        output_base = output_base or "lhescaleweight_by_index"
    else:
        output_base = output_arg

    return f"{output_base}.root", f"{output_base}.png"


def main():
    """Main entry point."""
    args = parse_args()
    events = load_events(args.input, args.tree)
    root_output, png_output = get_output_paths(args.output)

    all_hists = {}
    all_hists.update(make_lhe_scale_weight_histograms(events))
    all_hists.update(make_ps_weight_histograms(events))

    save_histograms_to_root(all_hists, root_output)
    print(f"Saved histograms to '{root_output}'")

    # plot_histograms(all_hists, png_output)


if __name__ == "__main__":
    main()
