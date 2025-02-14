from abc import ABCMeta, abstractmethod
from typing import Any

from exceptions import ValidationError


class BaseValidator(metaclass=ABCMeta):
    def __call__(self, value: Any) -> None:
        self.validate(value)

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class MinValueValidator(BaseValidator):
    def __init__(self, min_value: int) -> None:
        self.min_value = min_value

    def validate(self, value: int) -> None:
        if value < self.min_value:
            raise ValidationError(f"Value {value} is less than {self.min_value}")


class MaxValueValidator(BaseValidator):
    def __init__(self, max_value: int) -> None:
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if value > self.max_value:
            raise ValidationError(f"Value {value} is greater than {self.max_value}")


class MinMaxValueValidator(BaseValidator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(f"Value {value} is not in range from {self.min_value} to {self.max_value}")
