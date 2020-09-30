from sifter.extensions import ExtensionRegistry


def register(notification_method_name, notification_method_cls):
    ExtensionRegistry.register('notification_method', notification_method_name, notification_method_cls)


def get_cls(notification_method_name):
    return ExtensionRegistry.get('notification_method', notification_method_name)


class NotificationMethod(object):

    @classmethod
    def register(cls):
        try:
            register(cls.NOTIFICATION_METHOD_ID, cls)
        except AttributeError:
            # this method should only be called on sub-classes that define an
            # identifier
            raise NotImplementedError

    @classmethod
    def test_valid(cls, notification_uri):
        raise NotImplementedError

    @classmethod
    def test_capability(cls, notification_uri, notification_capability):
        raise NotImplementedError
