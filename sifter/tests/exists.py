from email.message import Message

from sifter.grammar.state import EvaluationState
from sifter.grammar.test import Test
from sifter.validators.stringlist import StringList
from sifter.grammar.string import expand_variables


# section 5.9
class TestExists(Test):

    HANDLER_ID = 'EXISTS'
    POSITIONAL_ARGS = [StringList()]

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        headers = self.positional_args[0]
        if not isinstance(headers, list):
            raise ValueError("TestExists.headers must be a list")
        for header in headers:
            header = expand_variables(header, state)
            if header not in message:
                return False
        return True
