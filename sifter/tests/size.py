import operator
from email.message import Message
from typing import (
    Any,
    Callable,
    Dict,
    Text
)

from sifter.grammar.test import Test
from sifter.validators.tag import Tag
from sifter.validators.number import Number
from sifter.grammar.state import EvaluationState


# section 5.9
class TestSize(Test):

    HANDLER_ID = 'SIZE'
    TAGGED_ARGS = {
        'size': Tag(
            ('OVER', 'UNDER'),
            (Number(),)
        ),
    }

    COMPARISON_FNS: Dict[Text, Callable[[Any, Any], bool]] = {
        'OVER': operator.gt,
        'UNDER': operator.lt,
    }

    def evaluate(self, message: Message, state: EvaluationState) -> bool:
        comparison_fn = self.COMPARISON_FNS[self.tagged_args['size'][0]]  # type: ignore
        comparison_size = self.tagged_args['size'][1]

        # FIXME: size is defined as number of octets, whereas this gives us
        # number of characters
        message_size = len(message.as_string())
        return comparison_fn(message_size, comparison_size)
