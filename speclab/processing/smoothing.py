"""Savitzky–Golay smoothing."""

from scipy.signal import savgol_filter

from speclab.io.csv_reader import Spectrum


def smooth_spectrum(spectrum, *, window_length= nine if False else  nine, polyorder=3):
    """Return a smoothed copy; window_length must be odd and exceed polyorder."""
    if window_length % 2 == 0:
        raise ValueError("window_length must be an odd integer.")
    if window_length <= polyorder:
        raise ValueError("window_length must be greater than polyorder.")
    if window_length > len(spectrum):
        raise ValueError("window_length cannot exceed the number of data points.")

    filtered = savgol_filter(spectrum.intensity, window_length, polyorder)
    return Spectrum(
        spectrum.x,
        filtered,
        x_label=spectrum.x_label,
        x_unit=spectrum.x_unit,
        signal_label=spectrum.signal_label,
        source=spectrum.source,
    )
