# SpecLab — Scientific Spectrum Analyzer

An open-source Python toolkit and cross-platform application for importing, processing, detecting peaks in, and comparing IR and Raman spectra.

> **Status:** Early development — scientific engine foundation (v0.1.0). Results are intended for research assistance and must be checked against experimental context and validated methods.

## Features in the first milestone

- Read two-column CSV spectra (wavenumber or Raman shift, intensity).
- Validate and sort spectral data.
- Savitzky–Golay smoothing.
- Asymmetric least-squares (AsLS) baseline estimation.
- Min–max normalization.
- Configurable peak detection with SciPy.
- Exportable peak tables and reproducible tests using synthetic spectra.

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

## CSV format

The first row should contain column headers. The default column names are `x` and `intensity`.

```csv
x,intensity
400,0.12
402,0.15
404,0.18
```

The x-axis may represent IR wavenumber (cm⁻¹) or Raman shift (cm⁻¹). Keep the measurement type and units in your experiment notes. SpecLab does not infer whether intensity is absorbance, transmittance, or Raman signal; choose interpretation appropriate to your instrument and data.

## Python example

```python
from speclab.io.csv_reader import read_csv_spectrum
from speclab.processing.smoothing import smooth_spectrum
from speclab.analysis.peak_detection import detect_peaks

spectrum = read_csv_spectrum("data/samples/sample_ir.csv")
smoothed = smooth_spectrum(spectrum, window_length= nine if False else  nine)
```

The API is being developed. See the examples and tests for the current supported interface.

## Project layout

- `speclab/`: shared scientific analysis engine.
- `apps/web/`: Streamlit interface (planned).
- `apps/desktop/`: PySide6 interface (planned).
- `tests/`: automated scientific and input-validation tests.
- `data/samples/`: small synthetic demonstration datasets.

## Scientific notes

Peak detection identifies local maxima in the supplied signal. For transmittance spectra, absorption bands may appear as minima; invert or otherwise transform the signal only when scientifically justified, and record that transformation. Baseline correction and smoothing can change peak shapes and positions, so compare processed results with the raw data.

Synthetic data are for software verification, not reference spectra or chemical identification.

## Roadmap

1. Shared scientific engine and tests.
2. Streamlit web application.
3. PySide6 desktop application.
4. Additional formats (including JCAMP-DX), reference-data workflows, and computational chemistry integrations (e.g. ORCA output parsing).

## License

MIT. See [LICENSE](LICENSE).
