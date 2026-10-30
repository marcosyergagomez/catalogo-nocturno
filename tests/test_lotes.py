import pytest

from practica.lotes import lotes


@pytest.mark.parametrize(
    "items, tamano, resultado",
    [
        ([1, 2, 3, 4, 5], 2, ([[1, 2], [3, 4], [5]])),
        ([], 3, []),
        (range(4), 4, [[0, 1, 2, 3]]),
    ],
)
def test_lotes(items, tamano, resultado):
    assert list(lotes(items, tamano)) == resultado


@pytest.mark.parametrize(
    "items, tamano",
    [
        ([1, 2, 3, 4, 5], 0),
        ([1, 2, 3, 4, 5], -1),
        ([1, 2, 3, 4, 5], 2.5),
        ([1, 2, 3, 4, 5], True),
    ],
)
def test_lotes_error(items, tamano):
    with pytest.raises(ValueError):
        lotes(items, tamano)
