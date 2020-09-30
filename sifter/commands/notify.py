import re
from sifter.grammar.command import Command
from sifter.grammar.string import expand_variables
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Tag
from sifter.grammar.rule import RuleSyntaxError
from sifter.extensions import ExtensionRegistry


# RFC 5435
class CommandNotify(Command):

    RULE_IDENTIFIER = 'NOTIFY'
    TAGGED_ARGS = {
        'from': Tag('FROM', (StringList(1),)),
        'importance': Tag('IMPORTANCE', (StringList(1),)),
        'options': Tag('OPTIONS', (StringList(),)),
        'message': Tag('MESSAGE', (StringList(1),)),
    }
    POSITIONAL_ARGS = [
        StringList(length=1)
    ]

    def __init__(self, arguments=None, tests=None, block=None):
        super(CommandNotify, self).__init__(arguments, tests, block)

        self.notify_from = self.notify_importance = self.notify_message = None
        self.notify_options = []
        if 'from' in self.tagged_args:
            self.notify_from = self.tagged_args['from'][1][0]
        if 'importance' in self.tagged_args:
            self.notify_importance = self.tagged_args['importance'][1][0]
        if 'options' in self.tagged_args:
            self.notify_options = self.tagged_args['options'][1]
        if 'message' in self.tagged_args:
            self.notify_message = self.tagged_args['message'][1][0]  # type: ignore
        self.notify_method = self.positional_args[0][0]  # type: ignore

    def evaluate(self, message, state):
        state.check_required_extension('enotify', 'NOTIFY')
        notify_from = expand_variables(self.notify_from, state)
        notify_importance = expand_variables(self.notify_importance, state)
        notify_options = map(lambda s: expand_variables(s, state), self.notify_options)
        notify_message = expand_variables(self.notify_message, state)
        notify_method = expand_variables(self.notify_method, state)

        m = re.match('^([A-Za-z][A-Za-z0-9.+-]*):', notify_method)
        if not m:
            raise RuleSyntaxError("Notification method must be an URI, e.g. 'mailto:email@example.com'")
        if notify_importance and notify_importance not in ["1", "2", "3"]:
            raise RuleSyntaxError("Illegal notify importance '%s' encountered" % self.notify_importance)
        notify_method_cls = ExtensionRegistry.get_notification_method(m.group(1).lower())
        if not notify_method_cls:
            raise RuleSyntaxError("Unsupported notification method '%s'" % m.group(1))
        (res, msg) = notify_method_cls.test_valid(notify_method)
        if not res:
            raise RuleSyntaxError(msg)

        state.actions.append('notify', (notify_method, notify_from, notify_importance, notify_options, notify_message))
