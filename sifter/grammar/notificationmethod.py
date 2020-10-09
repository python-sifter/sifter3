from typing import (
    Text,
    Tuple
)

from sifter.grammar.sieveobject import SieveObject


class NotificationMethod(SieveObject):

    HANDLER_TYPE = 'notification_method'

    @classmethod
    def test_valid(cls, notification_uri: Text) -> Tuple[bool, Text]:
        raise NotImplementedError

    @classmethod
    def test_capability(cls, notification_uri: Text, notification_capability: Text) -> Tuple[bool, Text]:
        raise NotImplementedError
