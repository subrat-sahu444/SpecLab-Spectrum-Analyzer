import numpy as np

from speclab.processing.baseline import correct_baseline, estimate_asls_baseline
from speclab.io.csv_reader import Spectrum


def test_asls_baseline_returns_finite_values():
    x = np.linspace(400, 1800, 201)
    baseline = 0.1 + 0.0001 * (x - 400)
    signal = baseline + np.exp(-0.5 * ((x - 1000) / 25) ** 2)
    estimated = estimate_asls_baseline(signal, lam=1e5, asymmetry=0.01, iterations=10)
    assert estimated.shape == signal.shape
    assert np.all(np.isfinite(estimated))


def test_baseline_correction_preserves_axis():
    x = np.linspace(400, 1800, 201)
    y = 0.2 + 0.0001 * x + np.exp(-0.5 * ((x - 1000) / 25) ** 2)
    spectrum = Spectrum(x, y)
    corrected = correct_baseline(spectrum)
    assert np.array_equal(corrected.x, spectrum.x)
    assert np.all(np.isfinite(corrected.intensity))
