"""Asymmetric least-squares baseline estimation."""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

from speclab.io.csv_reader import Spectrum


def estimate_asls_baseline(intensity, *, lam=1e5, asymmetry=0.01, iterations=10):
    """Estimate a smooth baseline using asymmetric least squares.

    Parameters are algorithmic controls, not universal spectroscopy defaults.
    Tune and document them for the instrument and sample type.
    """
    y = np.asarray(intensity, dtype=float)
    if y.ndim != 1 or y.size < 3 or not np.all(np.isfinite(y)):
        raise ValueError("intensity must be a finite one-dimensional array of length >= 3.")
    if lam <= 0:
        raise ValueError("lam must be positive.")
    if not 0 < asymmetry < 1:
        raise ValueError("asymmetry must be between 0 and 1.")
    if iterations < 1:
        raise ValueError("iterations must be at least 1.")

    length = y.size
    difference = sparse.diags(
        [1.0, -2.0, 1.0],
        [0, 1, 2],
        shape=(length - 2, length),
        format="csc",
        dtype=float,
    )
    penalty = lam * (difference.T @ difference)
    weights = np.ones(length)

    for _ in range(iterations):
        weight_matrix = sparse.spdiags(weights, 0, length, length)
        baseline = spsolve(weight_matrix + penalty, weights * y)
        weights = asymmetry * (y > baseline) + (1 - asymmetry) * (y < baseline)

    return baseline


def correct_baseline(spectrum, *, lam=1e5, asymmetry=0.01, iterations=10):
    """Subtract an estimated AsLS baseline and return a new Spectrum."""
    baseline = estimate_asls_baseline(
        spectrum.intensity, lam=lam, asymmetry=asymmetry, iterations=iterations
    )
    corrected = spectrum.intensity - baseline
    return Spectrum(
        spectrum.x,
        corrected,
        x_label=spectrum.x_label,
        x_unit=spectrum.x_unit,
        signal_label="Baseline-corrected intensity",
        source=spectrum.source,
    )
