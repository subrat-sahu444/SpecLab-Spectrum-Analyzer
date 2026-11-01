# SpecLab — Scientific Spectrum Analyzer

An open-source Python toolkit and cross-platform application for importing, processing, detecting peaks in, and comparing IR and Raman spectra.

> **Status:** Early development — shared scientific engine and first Streamlit web interface (v0.2.0). Results are intended for research assistance and must be checked against experimental context and validated methods.

## Current capabilities

- Read and validate CSV spectra with selectable x-axis and intensity columns.
- Savitzky–Golay smoothing and AsLS baseline correction.
- Min–max normalization.
- Configurable local-maximum peak detection.
- Streamlit web interface with spectrum plotting.
- Download processed spectra, detected peak tables, and PNG graphs.
- Compare spectra on their overlapping x-axis range through the Python engine.

## Run the web application

Python 3.10 or newer is recommended.

```powershell
cd C:\Users\subra\SpecLab-Spectrum-Analyzer
.\.venv\Scripts\python.exe -m pip install -e ".[web,dev]"
.\.venv\Scripts\python.exe -m streamlit run apps/web/app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser.

To run the tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## CSV format

The first row contains headers. The web app lets you choose the x-axis and intensity columns.

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
- `apps/web/`: Streamlit web interface.
- `apps/desktop/`: planned PySide6 interface.
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
