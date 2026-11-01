"""CSV loading for one-dimensional spectra."""

from pathlib import Path

import numpy as np
import pandas as pd


class Spectrum:
    """Validated x-axis and intensity arrays with lightweight metadata."""

    def __init__(self, x, intensity, *, x_label="Wavenumber", x_unit="cm⁻¹", signal_label="Intensity", source=None):
        x_array = np.asarray(x, dtype=float)
        y_array = np.asarray(intensity, dtype=float)

        if x_array.ndim != 1 or y_array.ndim != 1:
            raise ValueError("Spectrum data must be one-dimensional.")
        if x_array.size != y_array.size:
            raise ValueError("x and intensity must contain the same number of values.")
        if x_array.size < 3:
            raise ValueError("A spectrum must contain at least three data points.")
        if not np.all(np.isfinite(x_array)) or not np.all(np.isfinite(y_array)):
            raise ValueError("Spectrum data must contain only finite numeric values.")
        if np.unique(x_array).size != x_array.size:
            raise ValueError("The x-axis contains duplicate values.")

        order = np.argsort(x_array)
        self.x = x_array[order]
        self.intensity = y_array[order]
        self.x_label = x_label
        self.x_unit = x_unit
        self.signal_label = signal_label
        self.source = str(source) if source is not None else None

    def __len__(self):
        return self.x.size


def read_csv_spectrum(path, *, x_column="x", intensity_column="intensity"):
    """Read a CSV containing numeric x and intensity columns."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Spectrum file not found: {path}")

    frame = pd.read_csv(path)
    missing = [name for name in (x_column, intensity_column) if name not in frame.columns]
    if missing:
        raise ValueError(
            f"Missing required column(s): {', '.join(missing)}. "
            f"Available columns: {', '.join(map(str, frame.columns))}"
        )

    selected = frame[[x_column, intensity_column]].apply(pd.to_numeric, errors="coerce")
    if selected.isna().any().any():
        raise ValueError("The selected CSV columns contain missing or non-numeric values.")

    return Spectrum(
        selected[x_column].to_numpy(),
        selected[intensity_column].to_numpy(),
        x_label=x_column,
        source=path,
    )
