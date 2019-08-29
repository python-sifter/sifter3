import re
import sifter.grammar
import sifter.validators
import sifter.notificationmethod

__all__ = ('TestValidNotifyMethod',)

# RFC 5435
class TestValidNotifyMethod(sifter.grammar.Test):

    RULE_IDENTIFIER = 'VALID_NOTIFY_METHOD'

    def __init__(self, arguments=None, tests=None):
        super(TestValidNotifyMethod, self).__init__(arguments, tests)
        _, positional_args = self.validate_arguments(
                {
                },
                [ 
                    sifter.validators.StringList(),
                ],
            )
        self.validate_tests_size(0)
        self.notify_methods = positional_args[0]

    def evaluate(self, message, state):
        state.check_required_extension('enotify', 'NOTIFY')
        notify_methods = map(lambda s: sifter.grammar.string.expand_variables(s, state), self.notify_methods)

        for notify_method in notify_methods:
            m = re.match('^([A-Za-z][A-Za-z0-9.+-]*):', notify_method)
            if not m:
                return False
            notify_method_cls = sifter.notificationmethod.get_cls(m.group(1).lower())
            if not notify_method_cls:
                return False
            (res, _) = notify_method_cls.test_valid(notify_method)
            return res


# RFC 5435
class TestNotifyMethodCapability(sifter.grammar.Test):

    RULE_IDENTIFIER = 'NOTIFY_METHOD_CAPABILITY'

    def __init__(self, arguments=None, tests=None):
        super(TestNotifyMethodCapability, self).__init__(arguments, tests)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'comparator' : sifter.validators.Comparator(),
                    'match_type' : sifter.validators.MatchType(),
                },
                [ 
                    sifter.validators.StringList(1),
                    sifter.validators.StringList(1),
                    sifter.validators.StringList(),
                ],
            )
        self.validate_tests_size(0)

        if 'comparator' in tagged_args:
            self.comparator = tagged_args['comparator'][1][0]
        else:
            self.comparator = 'i;ascii-casemap'
        if 'match_type' in tagged_args:
            self.match_type = tagged_args['match_type'][0]
        else:
            self.match_type = 'IS'
        self.notification_uri = positional_args[0][0]
        self.notification_capability = positional_args[1][0]
        self.key_list = positional_args[2]

    def evaluate(self, message, state):
        state.check_required_extension('enotify', 'NOTIFY')
        notification_uri = sifter.grammar.string.expand_variables(self.notification_uri, state)
        notification_capability = sifter.grammar.string.expand_variables(self.notification_capability, state)
        key_list = map(lambda s: sifter.grammar.string.expand_variables(s, state), self.key_list)

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
            if sifter.grammar.string.compare(result, key, state, self.comparator, self.match_type):
                return True
        return False


TestValidNotifyMethod.register()
TestNotifyMethodCapability.register()

