import re
import sifter.grammar
import sifter.validators
import sifter.notificationmethod

__all__ = ('CommandNotify',)

# RFC 5435
class CommandNotify(sifter.grammar.Command):

    RULE_IDENTIFIER = 'NOTIFY'

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandNotify, self).__init__(arguments, tests, block)
        tagged_args, positional_args = self.validate_arguments(
                {
                    'from' : sifter.validators.Tag('FROM', (sifter.validators.StringList(1),)),
                    'importance' : sifter.validators.Tag('IMPORTANCE', (sifter.validators.StringList(1),)),
                    'options' : sifter.validators.Tag('OPTIONS', (sifter.validators.StringList(),)),
                    'message' : sifter.validators.Tag('MESSAGE', (sifter.validators.StringList(1),)),
                },
                [ 
                    sifter.validators.StringList(length=1),
                ],
            )
        self.validate_tests_size(0)
        self.validate_block_size(0)

        self.notify_from = self.notify_importance = self.notify_message = None
        self.notify_options = []
        if 'from' in tagged_args:
            self.notify_from = tagged_args['from'][1][0]
        if 'importance' in tagged_args:
            self.notify_importance = tagged_args['importance'][1][0]
        if 'options' in tagged_args:
            self.notify_options = tagged_args['options'][1]
        if 'message' in tagged_args:
            self.notify_message = tagged_args['message'][1][0]
        self.notify_method = positional_args[0][0]

    def evaluate(self, message, state):
        state.check_required_extension('enotify', 'NOTIFY')
        notify_from = sifter.grammar.string.expand_variables(self.notify_from, state)
        notify_importance = sifter.grammar.string.expand_variables(self.notify_importance, state)
        notify_options = map(lambda s: sifter.grammar.string.expand_variables(s, state), self.notify_options)
        notify_message = sifter.grammar.string.expand_variables(self.notify_message, state)
        notify_method = sifter.grammar.string.expand_variables(self.notify_method, state)
        
        m = re.match('^([A-Za-z][A-Za-z0-9.+-]*):', notify_method)
        if not m:
            raise sifter.grammar.RuleSyntaxError("Notification method must be an URI, e.g. 'mailto:email@example.com'")
        if notify_importance and not notify_importance in ["1", "2", "3"]:
            raise sifter.grammar.RuleSyntaxError("Illegal notify importance '%s' encountered" % self.notify_importance)
        notify_method_cls = sifter.notificationmethod.get_cls(m.group(1).lower())
        if not notify_method_cls:
            raise sifter.grammar.RuleSyntaxError("Unsupported notification method '%s'" % m.group(1))
        (res, msg) = notify_method_cls.test_valid(notify_method)
        if not res:
            raise sifter.grammar.RuleSyntaxError(msg)

        state.actions.append('notify', (notify_method, notify_from, notify_importance, notify_options, notify_message))        
        

CommandNotify.register()

