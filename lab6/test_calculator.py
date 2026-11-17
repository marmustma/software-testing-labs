"""Модульные тесты для класса Calculator (pytest)."""
import math

import pytest

from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-4, 1, -3),
    (0, 0, 0),
    (2.5, 0.5, 3.0),
    (10**12, 1, 10**12 + 1),
])
def test_add(calc, a, b, expected):
    assert calc.add(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (10, 4, 6),
    (4, 10, -6),
    (-3, -3, 0),
    (1.5, 0.25, 1.25),
])
def test_subtract(calc, a, b, expected):
    assert calc.subtract(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (3, 4, 12),
    (-2, 5, -10),
    (-2, -5, 10),
    (7, 0, 0),
    (0.5, 0.5, 0.25),
])
def test_multiply(calc, a, b, expected):
    assert calc.multiply(a, b) == expected


@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (7, 2, 3.5),
    (-9, 3, -3),
    (0, 5, 0),
    (1, 3, pytest.approx(0.3333333)),
])
def test_divide(calc, a, b, expected):
    assert calc.divide(a, b) == expected


@pytest.mark.parametrize("a", [1, -1, 0, 2.5])
def test_divide_by_zero_raises(calc, a):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль невозможно"):
        calc.divide(a, 0)


def test_divide_by_float_zero_raises(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(5, 0.0)


@pytest.mark.parametrize("base, exp, expected", [
    (2, 10, 1024),
    (5, 0, 1),
    (2, -1, 0.5),
    (9, 0.5, 3.0),
])
def test_power(calc, base, exp, expected):
    assert calc.power(base, exp) == expected


@pytest.mark.parametrize("x, expected", [(0, 0), (1, 1), (16, 4), (2, math.sqrt(2))])
def test_sqrt(calc, x, expected):
    assert calc.sqrt(x) == pytest.approx(expected)


def test_sqrt_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.sqrt(-4)


@pytest.mark.parametrize("n, expected", [
    (-7, False), (0, False), (1, False), (2, True), (3, True), (4, False),
    (9, False), (17, True), (25, False), (97, True), (7919, True), (7917, False),
])
def test_is_prime_number(calc, n, expected):
    assert calc.is_prime_number(n) is expected


@pytest.mark.parametrize("n, expected", [(0, 1), (1, 1), (5, 120), (10, 3628800)])
def test_factorial(calc, n, expected):
    assert calc.factorial(n) == expected


def test_factorial_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.factorial(-1)


@pytest.mark.parametrize("method, args", [
    ("add", ("2", 3)),
    ("subtract", (None, 1)),
    ("multiply", ([1], 2)),
    ("divide", (True, 1)),
    ("power", (2, "3")),
    ("sqrt", ("16",)),
    ("is_prime_number", (7.0,)),
    ("factorial", (5.5,)),
])
def test_invalid_types_raise_type_error(calc, method, args):
    with pytest.raises(TypeError):
        getattr(calc, method)(*args)
