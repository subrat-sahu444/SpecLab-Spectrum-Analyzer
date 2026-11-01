# SpecLab — Scientific Spectrum Analyzer

An open-source Python toolkit and cross-platform application for importing, processing, detecting peaks in, and comparing IR and Raman spectra.

> **Status:** Early development — scientific engine foundation (v0.1.0). Results are intended for research assistance and must be checked against experimental context and validated methods.

## First milestone

- Read and validate two-column CSV spectra.
- Savitzky–Golay smoothing and AsLS baseline correction.
- Min–max normalization.
- Configurable peak detection with SciPy.
- Compare spectra on their overlapping x-axis range.
- Synthetic test data and automated scientific tests.

## Quick start

Python 3.10 or newer is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

## CSV format

The first row contains headers. Default column names are `x` and `intensity`.

```csv
x,intensity
400,0.12
402,0.15
404,0.18
```

The x-axis may represent IR wavenumber or Raman shift (cm⁻¹). SpecLab does not infer whether intensity is absorbance, transmittance, or Raman signal; record the measurement type and units in your experiment notes.

## Python example

```python
from speclab.io.csv_reader import read_csv_spectrum
from speclab.processing.smoothing import smooth_spectrum
from speclab.analysis.peak_detection import detect_peaks

spectrum = read_csv_spectrum("data/samples/sample_ir.csv")
smoothed = smooth_spectrum(spectrum, window_length=9, polyorder=3)
peaks = detect_peaks(smoothed, prominence=0.05, distance=3)
print(peaks)
```

## Project layout

- `speclab/`: shared scientific analysis engine.
- `apps/web/`: Streamlit interface (planned).
- `apps/desktop/`: PySide6 interface (planned).
- `tests/`: automated scientific and input-validation tests.
- `data/samples/`: synthetic demonstration datasets.

## Scientific notes

Peak detection identifies local maxima in the supplied signal. For transmittance spectra, absorption bands may appear as minima; transform the signal only when scientifically justified and document that choice. Smoothing and baseline correction can change peak shapes and positions, so always compare processed results with raw data.

Synthetic data are for software verification, not reference spectra or chemical identification.

## Roadmap

1. Shared scientific engine and tests.
2. Streamlit web application.
3. PySide6 desktop application.
4. JCAMP-DX support, documented reference-data workflows, and computational chemistry integrations such as ORCA output parsing.

## License

MIT. See [LICENSE](LICENSE).
