from email.message import Message
import re
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    SupportsInt,
    Text,
    Union
)


from sifter.grammar.test import Test
from sifter.grammar.string import expand_variables, compare as string_compare
from sifter.grammar.state import EvaluationState
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Comparator, MatchType

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String


# section 5.7
class TestHeader(Test):

    HANDLER_ID = 'HEADER'
    TAGGED_ARGS = {
        'comparator': Comparator(),
        'match_type': MatchType(),
    }
    POSITIONAL_ARGS = [
        StringList(),
        StringList(),
    ]

    _newline_re = re.compile(r'\n+\s+')

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None
    ) -> None:
        super().__init__(arguments, tests)

        self.headers = self.positional_args[0]
        self.keylist = self.positional_args[1]
        self.match_type: Optional['TagGrammar'] = None
        self.comparator: Optional[Union[Text, 'TagGrammar']] = None
        if 'comparator' in self.tagged_args:
            self.comparator = self.tagged_args['comparator'][1][0]  # type: ignore
        if 'match_type' in self.tagged_args:
            self.match_type = self.tagged_args['match_type'][0]  # type: ignore

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        if not isinstance(self.headers, list):
            raise ValueError("TestHeader.headers is not a list")
        if not isinstance(self.keylist, list):
            raise ValueError("TestHeader.keylist is not a list")
        for header in self.headers:
            header = expand_variables(header, state)
            for value in message.get_all(header, []):
                value = self._newline_re.sub(" ", value)
                for key in self.keylist:
                    key = expand_variables(key, state)
                    if string_compare(
                        str(value),
                        key,
                        state,
                        self.comparator,
                        self.match_type
                    ):
                        return True
        return False
