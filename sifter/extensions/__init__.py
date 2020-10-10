from typing import (
    TYPE_CHECKING,
    cast,
    Dict,
    List,
    Text,
    Optional,
    Union,
    Type
)
import pkg_resources


from sifter.grammar.comparator import Comparator
from sifter.grammar.rule import Rule
from sifter.grammar.command import Command
from sifter.grammar.notificationmethod import NotificationMethod
from sifter.grammar.test import Test
if TYPE_CHECKING:
    from sifter.grammar.tag import Tag
    from sifter.grammar.sieveobject import SieveObject


class ExtensionRegistry():

    _HANDLERS_MAP: Dict[
        Text,
        Dict[
            Text,
            Union[
                bool,
                Type['SieveObject']
            ]
        ]
    ] = {}
    DEFAULT_EXTENSION: List[Text] = [
        'comparator-i;ascii-casemap',
        'comparator-i;octet'
        'regex'
    ]

    def __init__(self) -> None:
        for extension_name in self.DEFAULT_EXTENSION:
            self.register_extension(extension_name)

        for entry_point in pkg_resources.iter_entry_points('sifter_extensions'):
            sifter_extension_cls = cast(Type['SieveObject'], entry_point.load())
            self.register_handler(sifter_extension_cls)
            if sifter_extension_cls.EXTENSION_NAME is not None:
                self.register_extension(sifter_extension_cls.EXTENSION_NAME)

    @classmethod
    def register_extension(cls, extension_name: Text) -> None:
        cls.register('extension', extension_name, True)

    @classmethod
    def register_handler(cls, ext_cls: Type['SieveObject']) -> None:
        cls.register(ext_cls.handler_type(), ext_cls.handler_id(), ext_cls)

    @classmethod
    def get_comparator(cls, comparator: Union[Text, 'Tag']) -> Type['Comparator']:
        handler = cls.get('comparator', comparator)
        if not isinstance(handler, type) or not issubclass(handler, Comparator):
            raise ValueError('Wrong Comparator Type!')
        return handler

    @classmethod
    def get_command(cls, commandname: Text) -> Type['Command']:
        handler = cls.get('command', commandname)
        if not isinstance(handler, type) or not issubclass(handler, Command):
            raise ValueError('Wrong Command Type!')
        return handler

    @classmethod
    def get_test(cls, testname: Text) -> Type['Test']:
        handler = cls.get('test', testname)
        if not isinstance(handler, type) or not issubclass(handler, Test):
            raise ValueError('Wrong Test Type!')
        return handler

    @classmethod
    def get_notification_method(cls, methodname: Text) -> Type[NotificationMethod]:
        handler = cls.get('test', methodname)
        if not isinstance(handler, type) or not issubclass(handler, NotificationMethod):
            raise ValueError('Wrong Notification Method Type!')
        return handler

    @classmethod
    def has_extension(cls, ext_name: Text) -> bool:
        if cls.get('extension', ext_name):
            return True
        return False

    @classmethod
    def register(
        cls,
        handler_type: Text,
        handler_id: Text,
        value: Union[bool, Type['SieveObject']]
    ) -> None:
        cls._HANDLERS_MAP.setdefault(handler_type, {})[handler_id] = value

    @classmethod
    def unregister(
        cls, handler_type: Text, handler_id: Text
    ) -> Optional[Union[bool, Type['SieveObject']]]:
        return cls._HANDLERS_MAP.get(handler_type, {}).pop(handler_id, None)

    @classmethod
    def get(
        cls, handler_type: Text, handler_id: Text
    ) -> Optional[Union[bool, Type['SieveObject']]]:
        return cls._HANDLERS_MAP.get(handler_type, {}).get(handler_id, None)
