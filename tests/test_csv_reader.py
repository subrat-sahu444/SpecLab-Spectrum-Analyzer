import pytest

from speclab.io.csv_reader import read_csv_spectrum


def test_read_csv_spectrum_sorts_values(tmp_path):
    path = tmp_path / "spectrum.csv"
    path.write_text("x,intensity\n3,30\n1,10\n2,20\n", encoding="utf-8")

    spectrum = read_csv_spectrum(path)

    assert spectrum.x.tolist() == [1, 2, 3]
    assert spectrum.intensity.tolist() == [10, 20, 30]


def test_read_csv_spectrum_rejects_missing_column(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("wavelength,signal\n1,2\n2,3\n3,4\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required"):
        read_csv_spectrum(path)
