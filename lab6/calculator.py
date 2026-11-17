"""Модуль с бизнес-логикой для ЛР6: класс Calculator."""
import math


class Calculator:
    """Простой калькулятор с проверкой входных данных."""

    @staticmethod
    def _check_number(*values):
        for v in values:
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise TypeError(f"Ожидалось число, получено: {v!r}")

    def add(self, a, b):
        self._check_number(a, b)
        return a + b

    def subtract(self, a, b):
        self._check_number(a, b)
        return a - b

    def multiply(self, a, b):
        self._check_number(a, b)
        return a * b

    def divide(self, a, b):
        self._check_number(a, b)
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b

    def power(self, base, exp):
        self._check_number(base, exp)
        return base ** exp

    def sqrt(self, x):
        self._check_number(x)
        if x < 0:
            raise ValueError("Нельзя извлечь корень из отрицательного числа")
        return math.sqrt(x)

    def is_prime_number(self, n):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Проверка на простоту определена только для целых чисел")
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        for d in range(3, int(n ** 0.5) + 1, 2):
            if n % d == 0:
                return False
        return True

    def factorial(self, n):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Факториал определён только для целых чисел")
        if n < 0:
            raise ValueError("Факториал отрицательного числа не определён")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
