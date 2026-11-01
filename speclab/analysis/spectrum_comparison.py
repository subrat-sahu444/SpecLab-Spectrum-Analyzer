"""Numerical comparison of two spectra on a shared x-axis."""

import numpy as np
import pandas as pd


def compare_spectra(first, second):
    """Interpolate the second spectrum onto the first spectrum's x-grid.

    Only the overlapping x-range is returned. Interpolation assumes both spectra
    represent comparable measurements and that linear interpolation is suitable.
    """
    lower = max(float(first.x.min()), float(second.x.min()))
    upper = min(float(first.x.max()), float(second.x.max()))
    mask = (first.x >= lower) & (first.x <= upper)
    x = first.x[mask]
    if x.size < 2:
        raise ValueError("The spectra do not have enough overlapping x-axis points.")

    first_y = first.intensity[mask]
    second_y = np.interp(x, second.x, second.intensity)
    difference = first_y - second_y
    return pd.DataFrame(
        {
            "x": x,
            "first_intensity": first_y,
            "second_intensity_interpolated": second_y,
            "difference": difference,
        }
    )
