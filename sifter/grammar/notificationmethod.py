from typing import (
    Text,
    Tuple,
    Optional
)


class NotificationMethod(object):

    NOTIFICATION_METHOD_ID: Optional[Text] = None

    @classmethod
    def handler_type(cls) -> Text:
        return 'notification_method'

    @classmethod
    def handler_id(cls) -> Text:
        if cls.NOTIFICATION_METHOD_ID is None:
            raise NotImplementedError(
                'NotificationMethod must be implemented as subclass as NOTIFICATION_METHOD_ID must be set'
            )
        return cls.NOTIFICATION_METHOD_ID

    @classmethod
    def test_valid(cls, notification_uri: Text) -> Tuple[bool, Text]:
        raise NotImplementedError

    @classmethod
    def test_capability(cls, notification_uri: Text, notification_capability: Text) -> Tuple[bool, Text]:
        raise NotImplementedError
