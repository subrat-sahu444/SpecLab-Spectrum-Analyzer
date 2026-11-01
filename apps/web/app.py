"""Streamlit web interface for the SpecLab spectrum analysis engine."""

from __future__ import annotations

import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from speclab.analysis.peak_detection import detect_peaks
from speclab.io.csv_reader import Spectrum
from speclab.processing.baseline import correct_baseline
from speclab.processing.normalization import normalize_minmax
from speclab.processing.smoothing import smooth_spectrum


st.set_page_config(page_title="SpecLab Spectrum Analyzer", page_icon="🔬", layout="wide")
st.title("🔬 SpecLab — Spectrum Analyzer")
st.caption("A research-oriented workspace for processing and exploring IR/Raman spectra.")

with st.sidebar:
    st.header("1. Load spectrum")
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
    st.caption("Your CSV must contain numeric x-axis and intensity columns.")

if uploaded is None:
    st.info("Upload a spectrum CSV to begin.")
    st.markdown(
        """
        **Expected format**

        | x | intensity |
        |---:|---:|
        | 400 | 0.12 |
        | 402 | 0.15 |
        | 404 | 0.21 |

        The column names can be different; you will select them after uploading.
        """
    )
    st.stop()

try:
    frame = pd.read_csv(io.BytesIO(uploaded.getvalue()))
    if len(frame.columns) < 2:
        st.error("The CSV must contain at least two columns.")
        st.stop()

    with st.sidebar:
        st.header("2. Select columns")
        x_column = st.selectbox("X-axis column", options=list(frame.columns), index=0)
        y_column = st.selectbox("Intensity column", options=list(frame.columns), index=1)

    spectrum = Spectrum(
        pd.to_numeric(frame[x_column], errors="coerce").to_numpy(),
        pd.to_numeric(frame[y_column], errors="coerce").to_numpy(),
        x_label=str(x_column),
        source=uploaded.name,
    )
except Exception as exc:
    st.error(f"Could not load this spectrum: {exc}")
    st.stop()

with st.sidebar:
    st.header("3. Processing")
    apply_smoothing = st.checkbox("Savitzky–Golay smoothing", value=False)
    smoothing_window = st.number_input(
        "Smoothing window (odd number)",
        min_value=3,
        max_value=max(3, len(spectrum) if len(spectrum) % 2 else len(spectrum) - 1),
        value=min(9, len(spectrum) if len(spectrum) % 2 else len(spectrum) - 1),
        step=2,
        disabled=not apply_smoothing,
    )
    smoothing_order = st.number_input(
        "Polynomial order",
        min_value=1,
        max_value=min(5, int(smoothing_window) - 1),
        value=min(3, int(smoothing_window) - 1),
        disabled=not apply_smoothing,
    )

    apply_baseline = st.checkbox("AsLS baseline correction", value=False)
    baseline_lam = st.number_input(
        "Baseline smoothness (lambda)",
        min_value=100.0,
        max_value=10_000_000.0,
        value=100_000.0,
        step=10_000.0,
        disabled=not apply_baseline,
    )
    baseline_asymmetry = st.slider(
        "Baseline asymmetry",
        min_value=0.001,
        max_value=0.1,
        value=0.01,
        step=0.001,
        disabled=not apply_baseline,
    )

    apply_normalization = st.checkbox("Min-max normalization", value=False)

    st.header("4. Peak detection")
    run_peak_detection = st.checkbox("Detect local maxima", value=True)
    default_prominence = max(float(np.ptp(spectrum.intensity)) * 0.05, 0.0)
    peak_prominence = st.number_input(
        "Minimum prominence",
        min_value=0.0,
        value=default_prominence,
        disabled=not run_peak_detection,
        format="%.6g",
    )
    peak_distance = st.number_input(
        "Minimum peak distance (points)",
        min_value=1,
        value=5,
        disabled=not run_peak_detection,
    )

processed = spectrum
try:
    if apply_smoothing:
        processed = smooth_spectrum(
            processed,
            window_length=int(smoothing_window),
            polyorder=int(smoothing_order),
        )
    if apply_baseline:
        processed = correct_baseline(
            processed,
            lam=float(baseline_lam),
            asymmetry=float(baseline_asymmetry),
        )
    if apply_normalization:
        processed = normalize_minmax(processed)

    peaks = (
        detect_peaks(
            processed,
            prominence=float(peak_prominence),
            distance=int(peak_distance),
        )
        if run_peak_detection
        else pd.DataFrame(columns=["index", "x", "intensity", "prominence"])
    )
except Exception as exc:
    st.error(f"Processing could not be completed: {exc}")
    st.stop()

left, right = st.columns([3, 1])
with left:
    st.subheader("Processed spectrum")
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(processed.x, processed.intensity, linewidth=1.3, label="Processed spectrum")
    if not peaks.empty:
        ax.scatter(peaks["x"], peaks["intensity"], s=28, marker="o", label="Detected maxima")
    ax.set_xlabel(f"{processed.x_label} ({processed.x_unit})")
    ax.set_ylabel(processed.signal_label)
    ax.set_title(uploaded.name)
    ax.grid(True, alpha=0.25)
    ax.legend()
    ax.margins(x=0)
    st.pyplot(fig, clear_figure=False)
    image_buffer = io.BytesIO()
    fig.savefig(image_buffer, format="png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    st.download_button(
        "Download graph (PNG)",
        data=image_buffer.getvalue(),
        file_name="speclab_spectrum.png",
        mime="image/png",
    )

with right:
    st.subheader("Analysis summary")
    st.metric("Data points", len(processed))
    st.metric("Detected maxima", len(peaks))
    st.metric("Minimum intensity", f"{processed.intensity.min():.5g}")
    st.metric("Maximum intensity", f"{processed.intensity.max():.5g}")

st.subheader("Detected peaks")
if peaks.empty:
    st.write("No local maxima detected with the current settings.")
else:
    st.dataframe(peaks, use_container_width=True, hide_index=True)
    st.download_button(
        "Download peak table (CSV)",
        data=peaks.to_csv(index=False).encode("utf-8"),
        file_name="speclab_detected_peaks.csv",
        mime="text/csv",
    )

processed_frame = pd.DataFrame(
    {processed.x_label: processed.x, processed.signal_label: processed.intensity}
)
st.download_button(
    "Download processed spectrum (CSV)",
    data=processed_frame.to_csv(index=False).encode("utf-8"),
    file_name="speclab_processed_spectrum.csv",
    mime="text/csv",
)

st.warning(
    "Scientific note: peak detection identifies local maxima in the supplied signal. "
    "Absorption bands in transmittance data may appear as minima. Confirm the measurement "
    "mode and processing parameters before interpreting chemical assignments."
)
