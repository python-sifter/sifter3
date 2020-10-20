import re
from email.message import Message
from typing import (
    Any,
    Text,
    List
)

from sifter.grammar.test import Test
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Comparator, MatchType
import sifter.grammar.notificationmethod
from sifter.extensions import ExtensionRegistry
from sifter.grammar.state import EvaluationState


# RFC 5435
class TestValidNotifyMethod(Test):

    HANDLER_ID = 'VALID_NOTIFY_METHOD'
    POSITIONAL_ARGS = [
        StringList(),
    ]

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        notify_methods = self.positional_args[0]
        state.check_required_extension('enotify', 'NOTIFY')
        notify_methods = list(map(lambda s: sifter.grammar.string.expand_variables(s, state), notify_methods))  # type: ignore

        for notify_method in notify_methods:
            m = re.match('^([A-Za-z][A-Za-z0-9.+-]*):', notify_method)
            if not m:
                return False
            notify_method_cls = ExtensionRegistry.get_notification_method(m.group(1).lower())
            if not notify_method_cls:
                return False
            (res, _) = notify_method_cls.test_valid(notify_method)
            return res
        return False


# RFC 5435
class TestNotifyMethodCapability(Test):

    HANDLER_ID = 'NOTIFY_METHOD_CAPABILITY'
    TAGGED_ARGS = {
        'comparator': Comparator(),
        'match_type': MatchType(),
    }
    POSITIONAL_ARGS = [
        StringList(1),
        StringList(1),
        StringList(),
    ]

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        state.check_required_extension('enotify', 'NOTIFY')

        match_type: Text

        if 'comparator' in self.tagged_args:
            comparator = self.tagged_args['comparator'][1][0]  # type: ignore
        else:
            comparator = 'i;ascii-casemap'
        if 'match_type' in self.tagged_args:
            match_type = self.tagged_args['match_type'][0]  # type: ignore
        else:
            match_type = 'IS'
        notification_uri = self.positional_args[0][0]  # type: ignore
        notification_capability = self.positional_args[1][0]  # type: ignore
        key_list: List[Any] = self.positional_args[2]  # type: ignore

        notification_uri = sifter.grammar.string.expand_variables(notification_uri, state)
        notification_capability = sifter.grammar.string.expand_variables(notification_capability, state)
        key_list = list(map(lambda s: sifter.grammar.string.expand_variables(s, state), key_list))

        m = re.match('^([A-Za-z][A-Za-z0-9.+-]*):', notification_uri)
        if not m:
            return False
        notify_method_cls = ExtensionRegistry.get_notification_method(m.group(1).lower())
        if not notify_method_cls:
            return False
        (success, result) = notify_method_cls.test_capability(notification_uri, notification_capability)
        if not success:
            return False
        for key in key_list:
            if sifter.grammar.string.compare(result, key, state, comparator, match_type):
                return True
        return False
