from urllib import parse as urlparse
import sifter.notificationmethod

__all__ = ('MailtoNotificationMethod',)

class MailtoNotificationMethod(sifter.notificationmethod.NotificationMethod):

    NOTIFICATION_METHOD_ID = 'mailto'

    @staticmethod
    def parse_mailto_url(url):
        parsed_url = urlparse.urlparse(url)
        if parsed_url.scheme != 'mailto':
            return []
        header = urlparse.parse_qs(parsed_url.query)
        header['to'] = header.get('to', []) + parsed_url.path.split(',')
        return header

    @classmethod
    def test_valid(cls, notification_uri):
        uri_headers = cls.parse_mailto_url(notification_uri)
        uri_headers = dict((k.lower(), v) for k,v in uri_headers.items())
        if any(h in uri_headers for h in ('auto-submitted', 'received', 'date', 'message-id', 'from')):
            return (False, "Notification method mailto - illegal header")
        return (True, '')

    @classmethod
    def test_capability(cls, notification_uri, notification_capability):
        (res, msg) = cls.test_valid(notification_uri)
        if not res:
            return (res, msg)
        if notification_capability.lower() != 'online':
            return (False, "Unknown notification capability")
        return (True, 'maybe')


MailtoNotificationMethod.register()
