import numpy as np
import pytest

from speclab.analysis.peak_detection import detect_peaks
from speclab.analysis.spectrum_comparison import compare_spectra
from speclab.io.csv_reader import Spectrum
from speclab.processing.normalization import normalize_minmax
from speclab.processing.smoothing import smooth_spectrum


def make_spectrum():
    x = np.linspace(400, 1800, 701)
    y = (
        0.15
        + 1.2 * np.exp(-0.5 * ((x - 800) / 12) ** 2)
        + 0.8 * np.exp(-0.5 * ((x - 1400) / 20) ** 2)
    )
    return Spectrum(x, y)


def test_spectrum_sorts_x_axis():
    spectrum = Spectrum([3, 1, 2], [30, 10, 20])
    assert spectrum.x.tolist() == [1, 2, 3]
    assert spectrum.intensity.tolist() == [10, 20, 30]


def test_spectrum_rejects_duplicate_x_values():
    with pytest.raises(ValueError, match="duplicate"):
        Spectrum([1, 1, 2], [2, 3, 4])


def test_peak_detection_finds_known_peaks():
    peaks = detect_peaks(make_spectrum(), prominence=0.2, distance=10)
    positions = peaks["x"].to_numpy()
    assert np.any(np.isclose(positions, 800, atol=4))
    assert np.any(np.isclose(positions, 1400, atol=4))


def test_smoothing_preserves_length():
    original = make_spectrum()
    smoothed = smooth_spectrum(original, window_length= nine if False else  nine, polyorder=3)
    assert len(smoothed) == len(original)


def test_minmax_normalization():
    normalized = normalize_minmax(make_spectrum())
    assert normalized.intensity.min() == pytest.approx(0)
    assert normalized.intensity.max() == pytest.approx(1)


def test_spectrum_comparison_aligns_grid():
    first = make_spectrum()
    second = Spectrum(first.x, first.intensity * 0.5)
    compared = compare_spectra(first, second)
    assert len(compared) == len(first)
    assert np.allclose(compared["difference"], first.intensity * 0.5)
