from email.message import Message

from sifter.grammar.state import EvaluationState
from sifter.extensions import ExtensionRegistry

from sifter.grammar.test import Test
from sifter.validators.stringlist import StringList


# RFC 5463
class TestIHave(Test):

    HANDLER_ID = 'IHAVE'
    EXTENSION_NAME = 'ihave'
    POSITIONAL_ARGS = [
        StringList(),
    ]

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        state.check_required_extension('ihave', 'conditions on installed extensions')
        extension_list = self.positional_args[0]

        ret_val = True
        for ext_name in extension_list:  # type: ignore
            if ExtensionRegistry.has_extension(ext_name):
                state.require_extension(ext_name)
            else:
                ret_val = False
        return ret_val
