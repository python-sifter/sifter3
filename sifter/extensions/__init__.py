from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Text,
    Optional,
    Union,
    Type
)
import pkg_resources

if TYPE_CHECKING:
    from sifter.grammar.rule import Rule
    from sifter.grammar.comparator import Comparator


class ExtensionRegistry():

    _HANDLERS_MAP: Dict[Text, Dict[Text, Union[bool, Type['Comparator'], Type['Rule']]]] = {}
    DEFAULT_EXTENSION: List[Text] = [
        'regex',
        'comparator-i;ascii-casemap',
        'comparator-i;octet',
        'fileinto',
    ]

    def __init__(self) -> None:
        for extension_name in self.DEFAULT_EXTENSION:
            self.register_extension(extension_name)

        for entry_point in pkg_resources.iter_entry_points('sifter_extensions'):
            self.register_handler(entry_point.load())

    @classmethod
    def register_extension(cls, extension_name: Text) -> None:
        cls.register('extension', extension_name, True)

    @classmethod
    def register_handler(cls, ext_cls: Union[Type['Comparator'], Type['Rule']]) -> None:
        cls.register(ext_cls.handler_type(), ext_cls.handler_id(), ext_cls)

    @classmethod
    def register(
        cls,
        handler_type: Text,
        handler_id: Text,
        value: Union[bool, Type['Comparator'], Type['Rule']]
    ) -> None:
        cls._HANDLERS_MAP.setdefault(handler_type, {})[handler_id] = value

    @classmethod
    def unregister(cls, handler_type: Text, handler_id: Text) -> Optional[Union[bool, Type['Comparator'], Type['Rule']]]:
        return cls._HANDLERS_MAP.get(handler_type, {}).pop(handler_id, None)

    @classmethod
    def get(cls, handler_type: Text, handler_id: Text) -> Optional[Union[bool, Type['Comparator'], Type['Rule']]]:
        return cls._HANDLERS_MAP.get(handler_type, {}).get(handler_id, None)
