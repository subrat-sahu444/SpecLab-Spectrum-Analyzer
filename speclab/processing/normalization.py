"""Intensity normalization utilities."""

import numpy as np

from speclab.io.csv_reader import Spectrum


def normalize_minmax(spectrum):
    """Scale intensities to [0, 1]; constant signals are rejected."""
    values = spectrum.intensity
    low = float(np.min(values))
    high = float(np.max(values))
    if np.isclose(high, low):
        raise ValueError("Cannot min-max normalize a constant spectrum.")

    normalized = (values - low) / (high - low)
    return Spectrum(
        spectrum.x,
        normalized,
        x_label=spectrum.x_label,
        x_unit=spectrum.x_unit,
        signal_label="Normalized intensity",
        source=spectrum.source,
    )
