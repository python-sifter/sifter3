import re
from sifter.grammar.test import Test
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Comparator, MatchType
import sifter.grammar.notificationmethod

__all__ = ('TestValidNotifyMethod',)


# RFC 5435
class TestValidNotifyMethod(Test):

    RULE_IDENTIFIER = 'VALID_NOTIFY_METHOD'
    POSITIONAL_ARGS = [
        StringList(),
    ]

    def evaluate(self, message, state):
        notify_methods = self.positional_args[0]
        state.check_required_extension('enotify', 'NOTIFY')
        notify_methods = map(lambda s: sifter.grammar.string.expand_variables(s, state), notify_methods)

        for notify_method in notify_methods:
            m = re.match('^([A-Za-z][A-Za-z0-9.+-]*):', notify_method)
            if not m:
                return False
            notify_method_cls = sifter.grammar.notificationmethod.get_cls(m.group(1).lower())
            if not notify_method_cls:
                return False
            (res, _) = notify_method_cls.test_valid(notify_method)
            return res


# RFC 5435
class TestNotifyMethodCapability(Test):

    RULE_IDENTIFIER = 'NOTIFY_METHOD_CAPABILITY'
    TAGGED_ARGS = {
        'comparator': Comparator(),
        'match_type': MatchType(),
    }
    POSITIONAL_ARGS = [
        StringList(1),
        StringList(1),
        StringList(),
    ]

    def evaluate(self, message, state):
        state.check_required_extension('enotify', 'NOTIFY')

        if 'comparator' in self.tagged_args:
            comparator = self.tagged_args['comparator'][1][0]
        else:
            comparator = 'i;ascii-casemap'
        if 'match_type' in self.tagged_args:
            match_type = self.tagged_args['match_type'][0]
        else:
            match_type = 'IS'
        notification_uri = self.positional_args[0][0]
        notification_capability = self.positional_args[1][0]
        key_list = self.positional_args[2]

        notification_uri = sifter.grammar.string.expand_variables(notification_uri, state)
        notification_capability = sifter.grammar.string.expand_variables(notification_capability, state)
        key_list = map(lambda s: sifter.grammar.string.expand_variables(s, state), key_list)

        m = re.match('^([A-Za-z][A-Za-z0-9.+-]*):', notification_uri)
        if not m:
            return False
        notify_method_cls = sifter.notificationmethod.get_cls(m.group(1).lower())
        if not notify_method_cls:
            return False
        (success, result) = notify_method_cls.test_capability(notification_uri, notification_capability)
        if not success:
            return False
        for key in key_list:
            if sifter.grammar.string.compare(result, key, state, comparator, match_type):
                return True
        return False
