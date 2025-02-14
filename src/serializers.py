from functools import cached_property
from typing import Any, Type

from exceptions import ValidationError
from fields import BaseField


class BaseSerializer:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._data = args[0] if len(args) > 0 else kwargs.get("data")
        self._many = kwargs.get("many", False)

        assert self._data is not None, "'data' cannot be None"
        if not self._many:
            assert isinstance(self._data, dict), "'data' must be a dict"
        else:
            assert isinstance(self._data, list), "'many=True so 'data' must be a list"

        self.errors = {}
        self._serialized_data = dict() if not self._many else list()

    @property
    def data(self) -> dict:
        return self._serialized_data

    def is_valid(self, raise_exception: bool = False) -> bool:
        try:
            if self._many:
                for data in self._data:
                    self._fields_validator(data)
            else:
                self._fields_validator(self._data)
        except ValidationError:
            if raise_exception:
                raise

        return bool(not self.errors)

    def validated_data(self) -> None:
        pass

    def _fields_validator(self, data: dict) -> None:
        serialized_data = {}

        for name, field in self._serializer_fields.items():
            value = data.get(name)
            try:
                serialized_data[name] = field(value)
            except ValidationError as e:
                self.errors[name] = e

        if self._many:
            self._serialized_data.append(serialized_data)
        else:
            self._serialized_data = serialized_data

        if self.errors:
            raise ValidationError(self.errors)

    @cached_property
    def _serializer_fields(self) -> dict[str, Type[BaseField]]:
        raw_fields = {**self.__class__.__dict__}
        fields = {}

        for name, field in raw_fields.items():
            if isinstance(field, BaseField):
                fields[name] = field

        return fields
