from typing import (
    Optional, Text
)


class SieveObject():

    HANDLER_TYPE: Optional[Text] = None
    HANDLER_ID: Optional[Text] = None
    EXTENSION_NAME: Optional[Text] = None

    @classmethod
    def handler_type(cls) -> Text:
        if cls.HANDLER_TYPE is None:
            raise NotImplementedError('Rule must be implemented as subclass as HANDLER_TYPE must be set')
        return cls.HANDLER_TYPE

    @classmethod
    def handler_id(cls) -> Text:
        if cls.HANDLER_ID is None:
            raise NotImplementedError(
                'NotificationMethod must be implemented as subclass as HANDLER_ID must be set'
            )
        return cls.HANDLER_ID
