from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from netCDF4 import Dataset, Variable  # pylint: disable=no-name-in-module
from numpy import ndarray
from numpy.ma import MaskedArray


class BaseField(ABC):

    entry: str | None
    record: str | None
    convert: Callable[..., Any]

    def __init__(
        self,
        record_name: str | None,
        entry: str | None,
        convert: Callable[..., Any] | None,
    ) -> None:
        self.record = record_name
        self.entry = entry

        def _identity(x: Any) -> Any:
            return x

        self.convert = convert or _identity

    @abstractmethod
    def __call__(self, dataset: Dataset, name: str) -> Any:
        pass


class ClassField:

    value: Any

    def __init__(self, value: Any) -> None:
        self.value = value


DIMENSION_ENTRY_NAME = "name"
DIMENSION_ENTRY_SIZE = "size"


class DimensionField(BaseField):

    def __call__(self, dataset: Dataset, name: str) -> Any:
        alias = self.record or name
        if alias not in dataset.dimensions:
            raise ValueError(f"Unknown dimension '{alias}'")
        dimension_ = dataset.dimensions[alias]
        if self.entry is None:
            return self.convert(dimension_)
        try:
            value_ = getattr(dimension_, self.entry)
            return self.convert(value_)
        except AttributeError as error:
            raise ValueError(
                f"Unknown dimension entry '{alias}:{self.entry}'"
            ) from error


class RecordField(BaseField):

    def __init__(
        self,
        record_name: str | None,
        convert: Callable[..., Any] | None,
    ) -> None:
        super().__init__(record_name, None, convert)

    def __call__(self, dataset: Dataset, name: str) -> Any:
        alias = self.record or name
        if not hasattr(dataset, alias):
            raise ValueError(f"Unknown record field '{name}'")
        value_ = getattr(dataset, alias)
        return self.convert(value_)


VARIABLE_ARRAY_PREFIX = "array:"
VARIABLE_ENTRY_ARRAY = "array:*"
VARIABLE_ENTRY_DATA = "array:data"
VARIABLE_ENTRY_FILL_VALUE = "array:fill_value"
VARIABLE_ENTRY_MASK = "array:mask"


class VariableField(BaseField):

    def __call__(self, dataset: Dataset, name: str) -> Any:
        alias = self.record or name
        if alias not in dataset.variables:
            raise ValueError(f"Unknown variable '{alias}'")
        variable_: Variable[Any] = dataset.variables[alias]
        if self.entry is None:
            return self.convert(variable_)
        try:
            if self.entry.startswith(VARIABLE_ARRAY_PREFIX):
                value_ = self._extract_array(variable_, self.entry)
            else:
                value_ = getattr(variable_, self.entry)
            return self.convert(value_)
        except AttributeError as error:
            raise ValueError(
                f"Unknown variable entry '{alias}:{self.entry}'"
            ) from error
        except TypeError as error:
            raise ValueError(
                f"Unexpected variable entry type '{alias}:{self.entry}'"
            ) from error

    def _extract_array(self, variable_: Any, alias: str) -> Any:
        array_value = variable_[:]
        if not isinstance(array_value, (MaskedArray, ndarray)):
            raise TypeError("Unsuported variable entry type")
        if isinstance(array_value, MaskedArray):
            if alias == VARIABLE_ENTRY_DATA:
                return array_value.data
            if alias == VARIABLE_ENTRY_MASK:
                return array_value.mask
            if alias == VARIABLE_ENTRY_FILL_VALUE:
                return array_value.fill_value
        if alias == VARIABLE_ENTRY_ARRAY:
            return array_value
        raise AttributeError("Unknown array entry")


ARRAY = VARIABLE_ENTRY_ARRAY
DATA = VARIABLE_ENTRY_DATA
FILL = VARIABLE_ENTRY_FILL_VALUE
MASK = VARIABLE_ENTRY_MASK
SIZE = DIMENSION_ENTRY_SIZE


def dimension(
    record_name: str | None = None,
    *,
    entry: str | None = SIZE,
    convert: Callable[..., Any] | None = None,
) -> Any:
    return DimensionField(record_name, entry, convert)


def field(value: Any) -> Any:
    return ClassField(value)


def record(
    record_name: str | None = None,
    *,
    convert: Callable[..., Any] | None = None,
) -> Any:
    return RecordField(record_name, convert)


def variable(
    record_name: str | None = None,
    *,
    entry: str | None = DATA,
    convert: Callable[..., Any] | None = None,
) -> Any:
    return VariableField(record_name, entry, convert)
