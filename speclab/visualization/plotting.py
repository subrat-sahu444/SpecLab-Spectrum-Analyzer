"""Matplotlib helpers for consistent spectrum plots."""

import matplotlib.pyplot as plt


def plot_spectrum(spectrum, *, ax=None, title="Spectrum", color=None):
    """Plot a spectrum and return the Matplotlib Axes for further customization."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5))

    ax.plot(spectrum.x, spectrum.intensity, color=color, linewidth=1.4)
    ax.set_title(title)
    ax.set_xlabel(f"{spectrum.x_label} ({spectrum.x_unit})")
    ax.set_ylabel(spectrum.signal_label)
    ax.grid(True, alpha=0.25)
    ax.margins(x=0)
    return ax
