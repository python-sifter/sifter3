from typing import (
    TYPE_CHECKING,
    Dict,
    Text,
    Optional,
    Union,
    Type
)
import pkg_resources

if TYPE_CHECKING:
    from sifter.grammar.rule import Rule
    from sifter.grammar.comparator import Comparator


_HANDLERS_MAP: Dict[Text, Dict[Text, Union[bool, Type['Comparator'], Type['Rule']]]] = {}


def register(
    handler_type: Optional[Text],
    handler_id: Optional[Text],
    value: Union[bool, Type['Comparator'], Type['Rule']]
) -> None:
    from sifter.grammar.rule import Rule
    from sifter.grammar.comparator import Comparator
    if not handler_type or not handler_id:
        raise ValueError("handler_type and handler_id must not be None!")
    if not isinstance(value, Rule) and not (isinstance(value, type) and issubclass(value, (Rule, Comparator))):
        print(type(value))
        _HANDLERS_MAP.setdefault(handler_type, {})[handler_id] = value
    else:
        for entry_point in pkg_resources.iter_entry_points('sifter_extensions'):
            if entry_point.name not in _HANDLERS_MAP:
                ext_cls = entry_point.load()
                _HANDLERS_MAP.setdefault(ext_cls.get_mapkey(), {})[ext_cls.get_identifier()] = ext_cls
                _HANDLERS_MAP[entry_point.name] = entry_point.load()


def unregister(handler_type: Text, handler_id: Text) -> Optional[Union[bool, Type['Comparator'], Type['Rule']]]:
    return _HANDLERS_MAP.get(handler_type, {}).pop(handler_id, None)


def get(handler_type: Text, handler_id: Text) -> Optional[Union[bool, Type['Comparator'], Type['Rule']]]:
    return _HANDLERS_MAP.get(handler_type, {}).get(handler_id, None)
