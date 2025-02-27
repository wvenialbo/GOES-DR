from abc import ABC, abstractmethod
from types import NoneType
from typing import Any, cast, get_args, get_origin

from netCDF4 import Dataset, Variable  # pylint: disable=no-name-in-module
from numpy import float32, ndarray, result_type
from numpy.ma import MaskedArray
from numpy.typing import NDArray


class Recordfield(ABC):

    entry: str | NoneType
    record: str | NoneType
    value_class: type | NoneType
    item_type: type | NoneType

    def __init__(
        self,
        record: str | NoneType,
        entry: str | NoneType,
        value_class: type | NoneType,
        item_type: type | NoneType,
    ) -> NoneType:
        self.record = record
        self.entry = entry
        self.value_class = value_class
        self.item_type = item_type

    @abstractmethod
    def __call__(self, record: Dataset, entry: str) -> Any:
        pass


class Datarecord:

    def __init__(self, record: Dataset) -> NoneType:
        self._init_class_attributes()
        self._init_record_attributes(record)
        self._init_field_attributes(record)
        self._validate_class_attributes()
        self._validate_instance_attributes()
        self._validate_field_attributes()

    def __str__(self) -> str:
        return _to_str(self)

    def _get_annotations(self) -> dict[str, type]:
        all_attributes: dict[str, type] = {}
        mro_classes = self.__class__.__mro__
        for cls in mro_classes:
            if not issubclass(cls, Datarecord) or cls is Datarecord:
                continue
            all_attributes |= {
                key: value
                for key, value in cls.__annotations__.items()
                if key not in all_attributes
            }
        return all_attributes

    def _init_class_attributes(self) -> NoneType:
        # Copy class attributes to the instance provided they are not
        # field attributes, do not overwrite an existing instance
        # attributes
        for name in self._get_annotations():
            if hasattr(self, name):
                value = getattr(self, name)
                if isinstance(value, Recordfield):
                    continue
                if name in self.__dict__:
                    vtype = str(type(value))[8:-2]
                    message = f"Attribute '{name}: {vtype}' is already defined"
                    raise AttributeError(message)
                setattr(self, name, value)

    def _init_record_attributes(self, record: Dataset) -> NoneType:
        # Copy record attributes to the instance, do not overwrite
        # existing instance attributes
        for name in self._get_annotations():
            if not hasattr(self, name) and hasattr(record, name):
                value = getattr(record, name)
                setattr(self, name, value)

    def _init_field_attributes(self, record: Dataset) -> NoneType:
        # Copy record field attributes to the instance, do not overwrite
        # existing instance attributes
        for name in self._get_annotations():
            if hasattr(self, name):
                value = getattr(self, name)
                if not isinstance(value, Recordfield):
                    continue
                if name in self.__dict__:
                    vtype = str(type(value))[8:-2]
                    message = f"Attribute '{name}: {vtype}' is already defined"
                    raise AttributeError(message)
                setattr(self, name, value(record, name))

    def _validate_class_attributes(self) -> NoneType:
        all_annotations = self._get_annotations()
        for name, annotation in all_annotations.items():
            if hasattr(self, name):
                classtype = get_origin(annotation) or annotation
                value = getattr(self, name)
                if isinstance(value, classtype) or issubclass(
                    annotation, Recordfield
                ):
                    continue
                stype = str(annotation)[8:-2]
                vtype = str(type(value))[8:-2]
                raise TypeError(f"Attribute '{name}: {stype}' got '{vtype}'")
            stype = str(annotation)[8:-2]
            raise AttributeError(f"Attribute '{name}: {stype}' is undefined")

    def _validate_instance_attributes(self) -> NoneType:
        all_annotations = self._get_annotations()
        for name in self.__dict__:
            if name in all_annotations:
                continue
            value = getattr(self, name)
            vtype = str(type(value))[8:-2]
            raise AttributeError(f"Attribute '{name}: {vtype}' is unknown")

    def _validate_field_attributes(self) -> NoneType:
        all_annotations = self._get_annotations()
        for name in self.__dict__:
            field_class = all_annotations[name]
            if not issubclass(field_class, Recordfield):
                continue
            field: Recordfield = getattr(self.__class__, name)
            if not field.value_class and not field.item_type:
                continue
            value_class = field.value_class or ndarray
            value = getattr(self, name)
            if not isinstance(value, value_class):
                stype = str(field.value_class)[8:-2]
                vtype = str(type(value))[8:-2]
                raise TypeError(f"Attribute '{name}: {stype}' got '{vtype}'")
            if not field.item_type:
                continue
            value = cast(NDArray[Any], value)
            if not issubclass(value_class, ndarray()):
                raise ValueError("'item_type' is only supported for arrays")
            if issubclass(value.dtype, field.item_type):
                continue
            stype = str(field.item_type)[8:-2]
            utype = str(type(value))[8:-2]
            vtype = str(value.dtype)[8:-2]
            raise TypeError(
                f"Attribute '{name}: {utype}[{stype}]' got '{utype}[{vtype}]'"
            )

    @classmethod
    def _validate_type(cls, value: Any, annotation: type):
        classtype = get_origin(annotation) or annotation
        if classtype is not annotation:
            return cls._validate_container(value, classtype, annotation)
        return isinstance(value, classtype)

    @staticmethod
    def _validate_container(
        value: Any, classtype: type, annotation: type
    ) -> bool:
        return False

    @classmethod
    def _validate_array(cls, container: ndarray, annotation: type) -> bool:
        array_type = get_origin(annotation) or annotation

        inter = get_args(annotation)[1]
        inner = get_args(inter)
        dtype = inner[0] if inner else inter
        data_type = type(result_type(dtype))

        value_type = type(container.dtype)

        return cls._validate_generic(
            container, value_type, array_type, data_type
        )

    @staticmethod
    def _validate_generic(
        container: Any, value: type, origin: type, target: type
    ) -> bool:
        return isinstance(container, origin) and issubclass(value, target)


DIMENSION_ENTRY_NAME = "name"
DIMENSION_ENTRY_SIZE = "size"


class DimensionField(Recordfield):

    def __call__(self, record: Dataset, name: str) -> Any:
        alias = self.record or name
        if alias not in record.dimensions:
            raise ValueError(f"Unknown record '{alias}'")
        try:
            dimension_ = record.dimensions[alias]
            return getattr(dimension_, self.entry)
        except AttributeError as error:
            raise ValueError(
                f"Unknown record entry '{alias}:{self.entry}'"
            ) from error


VARIABLE_ARRAY_PREFIX = "array:"
VARIABLE_ENTRY_ARRAY = "array:*"
VARIABLE_ENTRY_DATA = "array:data"
VARIABLE_ENTRY_FILL_VALUE = "array:fill_value"
VARIABLE_ENTRY_MASK = "array:mask"


class VariableField(Recordfield):

    def __call__(self, record: Dataset, name: str) -> Any:
        alias = self.record or name
        if alias not in record.variables:
            raise ValueError(f"Unknown record '{alias}'")
        try:
            variable_: Variable[Any] = record.variables[alias]
            if self.entry.startswith(VARIABLE_ARRAY_PREFIX):
                return self._extract_array(variable_, self.entry)
            return getattr(variable_, self.entry)
        except AttributeError as error:
            raise ValueError(
                f"Unknown record entry '{alias}:{self.entry}'"
            ) from error
        except TypeError as error:
            raise ValueError(
                f"Unexpected record entry type '{alias}:{self.entry}'"
            ) from error

    def _extract_array(
        self, variable_: Variable, alias: str
    ) -> MaskedArray | ndarray:
        array_value = variable_[:]
        if not isinstance(array_value, (MaskedArray, ndarray)):
            raise TypeError("Unsuported entry type")
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
    record: str | NoneType = None,
    *,
    entry: str | NoneType = SIZE,
    value_class: type | NoneType = None,
    item_type: type | NoneType = None,
) -> Any:
    return DimensionField(record, entry, value_class, item_type)


def variable(
    record: str | NoneType = None,
    *,
    entry: str | NoneType = DATA,
    value_class: type | NoneType = None,
    item_type: type | NoneType = None,
) -> Any:
    return VariableField(record, entry, value_class, item_type)


def _get_attribute_names(this: Any) -> list[str]:
    all_attributes: list[str] = []
    mro_classes = this.__class__.__mro__
    for cls in mro_classes:
        if (
            issubclass(cls, Datarecord)
            and cls != Datarecord
            and hasattr(cls, "__annotations__")
        ):
            all_attributes.extend(
                [
                    key
                    for key in cls.__annotations__.keys()
                    if key not in all_attributes
                ]
            )
    return all_attributes


def _get_attribute_value(attribute_value: Any, indent: str) -> str:
    if attribute_value is None:
        attribute_value = "'not available'"
    elif isinstance(attribute_value, ndarray):
        attribute_value = _str_ndarray(attribute_value)
    elif isinstance(attribute_value, float):
        attribute_value = f"{attribute_value:.6f}"
    elif isinstance(attribute_value, str):
        attribute_value = f"'{attribute_value}'"
    elif isinstance(attribute_value, bool):
        attribute_value = f"{attribute_value}".lower()
    elif isinstance(attribute_value, Datarecord):
        attribute_value = _to_str(attribute_value, f"{indent}    ")
    return attribute_value


def _str_ndarray(array: NDArray[float32]) -> str:
    shape: str = f"({array.size})" if array.ndim == 1 else f"{array.shape}"
    dtype = f"{array.dtype}"
    value = f"{type(array)}, shape={shape}, dtype={dtype}>"
    return value.replace(">,", ",")


def _to_str(this: Any, indent: str = "    ") -> str:
    attributes = [str(this.__class__)]
    all_attributes = _get_attribute_names(this)
    for attribute_name in all_attributes:
        attribute_value = getattr(this, attribute_name, None)
        attribute_value = _get_attribute_value(attribute_value, indent)
        attributes.append(f"{indent}{attribute_name}: {attribute_value}")
    for attribute_name in dir(this.__class__):
        attribute_value = getattr(this.__class__, attribute_name)
        if isinstance(attribute_value, property):
            attribute_value = getattr(this, attribute_name, None)
            attribute_value = _get_attribute_value(attribute_value, indent)
            attributes.append(f"{indent}{attribute_name}: {attribute_value}")
    return "\n".join(attributes)

def _value_type(value:Any) ->str:
    if isinstance(value, ndarray):
        return value.__name__
    type_string = str(type(value))
    if type_string.startswith("<class '"):
        return type_string[8:-2]