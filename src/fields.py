from abc import ABCMeta, abstractmethod
from typing import Any, Iterable, Union

from exceptions import ValidationError


class BaseField(metaclass=ABCMeta):
    _type = None
    _convert_value = True

    def __init__(self, **kwargs: Any) -> None:
        """
        :param kwargs:
        """
        self.default = kwargs.get("default")
        self.allow_null = kwargs.get("allow_null")
        self.validators = kwargs.get("validators")
        self._validate_base_params()
        self._validate_params(**kwargs)

        assert self._type is not None, "Field 'type' must be specified"

    def __call__(self, value: Any) -> None:
        converted_value = self.__convert_value_or_return_given(value)
        self.__process_validators(converted_value)
        return self.validate(converted_value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass

    def _validate_params(self, **kwargs: Any) -> None:
        pass

    def _validate_base_params(self) -> None:
        if self.allow_null is not None and not isinstance(self.allow_null, bool):
            raise ValueError("'allow_null' must be True or False")
        if self.validators is not None and not isinstance(self.validators, Iterable):
            raise ValueError("'allow_null' must be iterable")
        if self.default is not None and not isinstance(self.default, self._type):
            raise ValueError(f"The default value must be of type '{self._type.__name__}'")

    def __convert_value_or_return_given(self, value: Any) -> Any:
        if isinstance(value, self._type):
            return value
        if not self._convert_value:
            return value
        try:
            return self._type(value)
        except Exception:
            return value

    def __process_validators(self, value: Any) -> None:
        if self.validators:
            for validator in self.validators:
                validator(value)


class IntegerField(BaseField):
    _type = int

    def validate(self, value: Union[int, None]) -> Union[int, None]:
        if value is not None and not isinstance(value, self._type):
            raise ValidationError(f"The value must be of type '{self._type.__name__}'")

        if value is None and self.default is None and not self.allow_null:
            raise ValidationError("Field cannot be empty")
        if value is None and self.default is None and self.allow_null:
            return None
        elif value is None and self.default is not None:
            value = self.default

        return value


class CharField(BaseField):
    _type = str

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._max_length = kwargs.get("max_length")

    def validate(self, value: Union[int, None]) -> Union[int, None]:
        if value is not None and not isinstance(value, self._type):
            raise ValidationError(f"The value must be of type '{self._type.__name__}'")

        if value is None and self.default is None and not self.allow_null:
            raise ValidationError("Field cannot be empty")
        if value is None and self.default is None and self.allow_null:
            return None
        elif value is None and self.default is not None:
            value = self.default

        if self._max_length and len(value) > self._max_length:
            raise ValidationError(f"The length of the value must be less than {self._max_length} (or equal)")

        return value


class BooleanField(BaseField):
    _type = bool
    _convert_value = False

    def validate(self, value: Union[int, None]) -> Union[int, None]:
        if value is not None and not isinstance(value, self._type):
            raise ValidationError(f"The value must be of type '{self._type.__name__}'")

        if value is None and self.default is None and not self.allow_null:
            raise ValidationError("Field cannot be empty")
        if value is None and self.default is None and self.allow_null:
            return None
        elif value is None and self.default is not None:
            value = self.default

        return value
