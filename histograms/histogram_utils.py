"""Utility functions for working with weight histograms from NanoAOD files."""

import math
import numpy as np
import awkward as ak
import hist
import matplotlib.pyplot as plt
import uproot


def build_weight_histograms(weights, multiplicities, weight_name, valid_multiplicities=None):
    """
    Build histograms for weights by index.

    Args:
        weights: Array of weight values
        multiplicities: Array of weight multiplicities (number of weights per event)
        weight_name: Name of the weight type (e.g., "LHEScaleWeight")
        valid_multiplicities: Optional set of allowed multiplicity values (default: all > 0)

    Returns:
        Dictionary of histograms keyed by weight_name_index
    """
    if valid_multiplicities is None:
        event_mask = multiplicities > 0
    else:
        event_mask = ak.zeros_like(multiplicities, dtype=bool)
        for count in valid_multiplicities:
            event_mask = event_mask | (multiplicities == count)

    selected_weights = weights[event_mask]
    selected_multiplicities = multiplicities[event_mask]
    selected_events = int(ak.sum(event_mask))

    if selected_events == 0:
        print(f"No events selected for {weight_name}")
        return {}

    max_multiplicity = int(ak.max(selected_multiplicities))
    print(f"{weight_name}: selected events = {selected_events}")
    print(f"{weight_name}: multiplicity max = {max_multiplicity}")

    histograms = {}
    for index in range(max_multiplicity):
        index_mask = selected_multiplicities > index
        values = ak.to_numpy(selected_weights[index_mask, index])
        hist_name = f"{weight_name}_{index}"
        axis_name = f"{weight_name.lower()}_{index}"
        histograms[hist_name] = hist.Hist(
            hist.axis.Regular(100, 0.0, 2.0, name=axis_name, label=f"{weight_name}[{index}]")
        )
        histograms[hist_name].fill(**{axis_name: values})

    return histograms


def make_lhe_scale_weight_histograms(events):
    """
    Create LHEScaleWeight histograms from NanoAOD events.

    Args:
        events: NanoAOD events object

    Returns:
        Dictionary of LHEScaleWeight histograms
    """
    multiplicities = ak.num(events.LHEScaleWeight, axis=1)
    return build_weight_histograms(
        events.LHEScaleWeight,
        multiplicities,
        "LHEScaleWeight",
        valid_multiplicities={8, 9},
    )


def make_ps_weight_histograms(events):
    """
    Create PSWeight histograms from NanoAOD events.

    Args:
        events: NanoAOD events object

    Returns:
        Dictionary of PSWeight histograms (empty if branch not found)
    """
    if "PSWeight" not in events.fields:
        print("PSWeight branch not found, skipping PSWeight histograms")
        return {}

    if "nPSWeight" in events.fields:
        multiplicities = events.nPSWeight
    else:
        multiplicities = ak.num(events.PSWeight, axis=1)

    return build_weight_histograms(events.PSWeight, multiplicities, "PSWeight")


def save_histograms_to_root(histograms, output_path):
    """
    Save histograms to a ROOT file.

    Args:
        histograms: Dictionary of histograms
        output_path: Output ROOT file path
    """
    with uproot.recreate(output_path) as root_file:
        for name, histogram in histograms.items():
            root_file[name] = histogram


def build_log10_weight_histograms(weights, multiplicities, weight_name, valid_multiplicities=None):
    """
    Build histograms for log10(weights) by index.

    Args:
        weights: Array of weight values
        multiplicities: Array of weight multiplicities (number of weights per event)
        weight_name: Name of the weight type (e.g., "LHEReweightingWeight")
        valid_multiplicities: Optional set of allowed multiplicity values (default: all > 0)

    Returns:
        Dictionary of histograms keyed by weight_name_index
    """
    if valid_multiplicities is None:
        event_mask = multiplicities > 0
    else:
        event_mask = ak.zeros_like(multiplicities, dtype=bool)
        for count in valid_multiplicities:
            event_mask = event_mask | (multiplicities == count)

    selected_weights = weights[event_mask]
    selected_multiplicities = multiplicities[event_mask]
    selected_events = int(ak.sum(event_mask))

    if selected_events == 0:
        print(f"No events selected for {weight_name}")
        return {}

    max_multiplicity = int(ak.max(selected_multiplicities))
    print(f"{weight_name}: selected events = {selected_events}")
    print(f"{weight_name}: multiplicity max = {max_multiplicity}")

    histograms = {}
    for index in range(max_multiplicity):
        index_mask = selected_multiplicities > index
        values = ak.to_numpy(selected_weights[index_mask, index])
        # Filter out zero and negative weights before taking log10
        valid_mask = values > 0
        values = values[valid_mask]

        if len(values) == 0:
            print(f"Warning: No positive weights found for {weight_name}[{index}]")
            continue

        log_values = np.log10(values)
        hist_name = f"{weight_name}_{index}"
        axis_name = f"log10_{weight_name.lower()}_{index}"

        # # Auto-scale range based on data
        # log_min = float(np.min(log_values))
        # log_max = float(np.max(log_values))
        # # Add 10% padding
        # log_range = log_max - log_min
        # log_min -= 0.1 * log_range
        # log_max += 0.1 * log_range

        log_min = float(np.min(log_values))
        log_max = float(np.max(log_values))

        log_range = log_max - log_min

        if log_range == 0:
            log_min -= 0.5
            log_max += 0.5
        else:
            log_min -= 0.1 * log_range
            log_max += 0.1 * log_range

        histograms[hist_name] = hist.Hist(
            hist.axis.Regular(100, log_min, log_max, name=axis_name, label=f"log10({weight_name}[{index}])")
        )
        histograms[hist_name].fill(**{axis_name: log_values})

    return histograms


def make_lhe_reweighting_weight_histograms(events):
    """
    Create LHEReweightingWeight histograms (log10-scaled) from NanoAOD events.

    Args:
        events: NanoAOD events object

    Returns:
        Dictionary of LHEReweightingWeight histograms
    """
    if "LHEReweightingWeight" not in events.fields:
        print("LHEReweightingWeight branch not found")
        return {}

    if "nLHEReweightingWeight" in events.fields:
        multiplicities = events.nLHEReweightingWeight
    else:
        multiplicities = ak.num(events.LHEReweightingWeight, axis=1)

    return build_log10_weight_histograms(
        events.LHEReweightingWeight,
        multiplicities,
        "LHEReweightingWeight",
    )


def build_weighted_observable_histogram(observable, weights, weight_name, n_bins=50, x_min=0, x_max=500):
    """
    Build a histogram for an observable with event weights.

    Args:
        observable: Array of observable values (e.g., pt)
        weights: Array of event weights (1D, one per event)
        weight_name: Name of the histogram
        n_bins: Number of bins
        x_min: Minimum x value
        x_max: Maximum x value

    Returns:
        A histogram object
    """
    if len(observable) == 0:
        print(f"No events available for {weight_name}")
        return None

    axis_name = weight_name.lower()
    histogram = hist.Hist(
        hist.axis.Regular(n_bins, x_min, x_max, name=axis_name, label=weight_name)
    )
    histogram.fill(**{axis_name: observable}, weight=weights)

    return histogram


def get_z_boson_pt(events):
    """
    Get Z boson pt from GenPart.

    Args:
        events: NanoAOD events object

    Returns:
        Array of Z boson pt values
    """
    if "GenPart" not in events.fields:
        print("GenPart branch not found")
        return ak.Array([])

    # PDG ID for Z boson is 23
    gen_particles = events.GenPart
    z_mask = (gen_particles.pdgId == 23) & (gen_particles.status == 62)
    z_bosons = gen_particles[z_mask]

    # If no status 62 Z bosons, try status 2 (intermediate)
    if ak.sum(ak.num(z_bosons, axis=1)) == 0:
        z_mask = (gen_particles.pdgId == 23)
        z_bosons = gen_particles[z_mask]

    # Get pt of first Z boson per event
    z_pt = ak.fill_none(ak.firsts(z_bosons.pt), 0)

    return z_pt


def get_z_boson_mass(events):
    """
    Get Z boson mass from GenPart.

    Args:
        events: NanoAOD events object

    Returns:
        Array of Z boson mass values
    """
    if "GenPart" not in events.fields:
        print("GenPart branch not found")
        return ak.Array([])

    gen_particles = events.GenPart
    z_mask = (gen_particles.pdgId == 23) & (gen_particles.status == 62)
    z_bosons = gen_particles[z_mask]

    if ak.sum(ak.num(z_bosons, axis=1)) == 0:
        z_mask = (gen_particles.pdgId == 23)
        z_bosons = gen_particles[z_mask]

    # Get mass of first Z boson per event
    z_mass = ak.fill_none(ak.firsts(z_bosons.mass), 0)

    return z_mass


def plot_ratio_histograms(hist_numerator, hist_denominator, output_path, title="Observable"):
    """
    Plot histograms normalized to 1, with ratio panel below.

    Args:
        hist_numerator: Histogram for numerator
        hist_denominator: Histogram for denominator
        output_path: Output PNG file path
        title: Title for the plot
    """
    if hist_numerator is None or hist_denominator is None:
        print("Invalid histograms for ratio plot")
        return

    # Get values and variances
    num_values = hist_numerator.values()
    denom_values = hist_denominator.values()
    num_variances = hist_numerator.variances()
    denom_variances = hist_denominator.variances()

    # Handle None variances
    if num_variances is None:
        num_variances = num_values
    if denom_variances is None:
        denom_variances = denom_values

    # Normalize to 1.0 (divide by integral = sum of bin values * bin width)
    num_integral = np.sum(num_values)
    denom_integral = np.sum(denom_values)

    num_values_norm = num_values / num_integral if num_integral > 0 else num_values
    denom_values_norm = denom_values / denom_integral if denom_integral > 0 else denom_values

    num_variances_norm = num_variances / (num_integral ** 2) if num_integral > 0 else num_variances
    denom_variances_norm = denom_variances / (denom_integral ** 2) if denom_integral > 0 else denom_variances

    # Create figure with ratio panel
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.05)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    # Get bin edges for plotting
    axes = hist_numerator.axes
    bin_edges = axes[0].edges
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0]

    # Ensure same shape
    min_bins = min(len(num_values_norm), len(denom_values_norm))
    num_vals = num_values_norm[:min_bins]
    denom_vals = denom_values_norm[:min_bins]
    num_err = np.sqrt(num_variances_norm[:min_bins])
    denom_err = np.sqrt(denom_variances_norm[:min_bins])
    centers = bin_centers[:min_bins]

    # Top panel: normalized histograms
    ax1.step(bin_edges[:min_bins+1], np.concatenate([[num_vals[0]], num_vals]),
             where='mid', label='EFT (reweighted SM)', color='blue', linewidth=2)
    ax1.step(bin_edges[:min_bins+1], np.concatenate([[denom_vals[0]], denom_vals]),
             where='mid', label='EWK', color='orange', linewidth=2, alpha=0.7)
    ax1.errorbar(centers, num_vals, yerr=num_err, fmt='none', ecolor='blue', alpha=0.5, capsize=3)
    ax1.errorbar(centers, denom_vals, yerr=denom_err, fmt='none', ecolor='orange', alpha=0.5, capsize=3)

    ax1.set_ylabel('Events (normalized to 1.0)')
    ax1.set_title(f'{title} - Normalized to 1.0')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # Bottom panel: ratio with error bars
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio_vals = np.divide(num_vals, denom_vals, where=(denom_vals > 0), out=np.ones_like(num_vals))
        # Propagate errors: (A/B)^2 * (dA/A)^2 + (dB/B)^2
        ratio_err = np.where(
            denom_vals > 0,
            ratio_vals * np.sqrt((num_err / np.where(num_vals > 0, num_vals, 1)) ** 2 +
                                (denom_err / denom_vals) ** 2),
            0
        )

    ax2.errorbar(centers, ratio_vals, yerr=ratio_err, fmt='o', markersize=6,
                 ecolor='blue', color='blue', capsize=4, alpha=0.7)
    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax2.set_ylabel('Ratio')
    ax2.set_xlabel(title)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim(0.5, 2.0)

    # Hide top x label
    ax1.tick_params(labelbottom=False)

    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

def plot_histograms(histograms, output_prefix):
    """
    Plot all histograms and save them as individual PNG files.

    Args:
        histograms: Dictionary of histograms
        output_prefix: Base path for output files (without extension)
    """
    if not histograms:
        print("No histograms to plot")
        return

    for name, h in histograms.items():
        fig, ax = plt.subplots(figsize=(8, 6))

        # Extract histogram data
        values = h.values()
        variances = h.variances()

        if variances is None:
            variances = values

        errors = np.sqrt(variances)

        # Axis info
        axis = h.axes[0]
        edges = axis.edges
        centers = (edges[:-1] + edges[1:]) / 2

        ax.step(edges, np.append(values, values[-1]), where="post", label=name, linewidth=2)

        ax.errorbar(
            centers,
            values,
            yerr=errors,
            fmt='none',       
            capsize=2,
            linewidth=1.5
        )

        # Labels
        ax.set_xlabel(axis.label if axis.label else axis.name)
        ax.set_ylabel("Entries")
        ax.set_title(name)

        ax.grid(True, alpha=0.3)
        ax.legend()

        # Save per histogram
        output_file = f"{output_prefix}_{name}.png"
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        plt.close(fig)

        print(f"Saved plot: {output_file}")