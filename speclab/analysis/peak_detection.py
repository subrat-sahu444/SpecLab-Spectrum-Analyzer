"""Configurable local-maximum peak detection."""

import pandas as pd
from scipy.signal import find_peaks


def detect_peaks(spectrum, *, prominence=None, distance=None, height=None):
    """Return detected maxima as a DataFrame.

    The supplied signal is analyzed as-is. For transmittance spectra, absorption
    bands can be minima; transform the signal only when that interpretation is
    appropriate for the measurement and document the choice.
    """
    indices, properties = find_peaks(
        spectrum.intensity,
        prominence=prominence,
        distance=distance,
        height=height,
    )
    result = pd.DataFrame(
        {
            "index": indices,
            "x": spectrum.x[indices],
            "intensity": spectrum.intensity[indices],
        }
    )
    if "prominences" in properties:
        result["prominence"] = properties["prominences"]
    return result
