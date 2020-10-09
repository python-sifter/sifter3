from typing import (
    Dict,
    Text,
    Optional,
    List,
    Tuple,
    Union,
    TYPE_CHECKING,
    SupportsInt
)

from sifter.grammar.sieveobject import SieveObject
from sifter.grammar.tag import Tag
from sifter.grammar.validator import Validator
import sifter.grammar
import sifter.utils

if TYPE_CHECKING:
    from sifter.grammar.test import Test
    from sifter.grammar.string import String


class RuleSyntaxError(Exception):
    pass


class Rule(SieveObject):

    TAGGED_ARGS: Optional[Union[List[Validator], Dict[Text, Validator]]] = None
    POSITIONAL_ARGS: Optional[List[Validator]] = None

    HAS_TESTS: bool = True
    TESTS_MIN: int = 0
    TESTS_MAX: Optional[int] = None

    def __init__(
        self,
        arguments: Optional[List[Union['Tag', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None,
        validate: bool = True
    ) -> None:
        if arguments is None:
            self.arguments = []
        else:
            self.arguments = arguments
        if tests is None:
            self.tests = []
        else:
            self.tests = tests
        if validate:
            self.tagged_args, self.positional_args = self.validate()

    def __str__(self) -> Text:
        s = ["%s" % self.HANDLER_ID, ]
        for arg in self.arguments:
            s.append(" %s" % arg)
        s.append('\n')
        for test in self.tests:
            s.append("(\n%s)\n" % sifter.utils.indent_string(str(test), 2))
        return ''.join(s)

    def validate_arguments(
        self,
        tagged_args: Optional[Union[List[Validator], Dict[Text, Validator]]] = None,
        positional_args: Optional[List[Validator]] = None
    ) -> Tuple[
        Dict[Text, List[Union[Tag, SupportsInt, List[Union[Text, 'String']]]]],
        List[Union[Tag, SupportsInt, List[Union[Text, 'String']]]]
    ]:
        if tagged_args is None:
            tagged_args = self.TAGGED_ARGS or {}
        if positional_args is None:
            positional_args = self.POSITIONAL_ARGS or []

        seen_args: Dict[Text, List[Union['Tag', SupportsInt, List[Union[Text, 'String']]]]] = {}
        i, n = 0, len(self.arguments)
        while i < n:
            if not isinstance(tagged_args, dict) or not isinstance(self.arguments[i], Tag):
                break
            num_valid_args: Optional[int] = 0
            for arg_name, arg_validator in tagged_args.items():
                num_valid_args = arg_validator.validate(self.arguments, i)
                if num_valid_args is not None and num_valid_args > 0:
                    if arg_name in seen_args:
                        raise RuleSyntaxError(
                            "%s argument to %s was already seen earlier: %s" %
                            (arg_name, self.HANDLER_ID, self.arguments[i])
                        )
                    seen_args[arg_name] = self.arguments[i:i + num_valid_args]
                    i += num_valid_args
                    break
            else:
                raise RuleSyntaxError(
                    "Unexpected tag argument '%s' to %s encountered" % (self.arguments[i], self.HANDLER_ID)
                )
        # TODO: make sure all non-optional tagged arguments were seen

        if len(positional_args) != (n - i):
            raise RuleSyntaxError(
                "%s requires %d positional arguments but %d were supplied"
                % (self.HANDLER_ID, len(positional_args), n - i)
            )

        for arg_position, arg_validator in enumerate(positional_args):
            if arg_validator.validate(self.arguments, i + arg_position) == 0:
                raise RuleSyntaxError(
                    "positional argument #%d to %s was not in the expected format"
                    % (arg_position + 1, self.HANDLER_ID)
                )

        return (seen_args, self.arguments[i:])

    def validate_tests_size(self, min_tests: int, max_tests: Optional[int] = None) -> None:
        if max_tests is None:
            max_tests = min_tests
        if len(self.tests) < min_tests or len(self.tests) > max_tests:
            if max_tests == min_tests:
                msg = "%d" % min_tests
            else:
                msg = "between %d and %d" % (min_tests, max_tests)
            raise RuleSyntaxError("%s takes %s tests" % (
                self.HANDLER_ID, msg))

    def validate(self) -> Tuple[
        Dict[Text, List[Union[Tag, SupportsInt, List[Union[Text, 'String']]]]],
        List[Union[Tag, SupportsInt, List[Union[Text, 'String']]]]
    ]:
        tagged_args, positional_args = self.validate_arguments()
        if self.HAS_TESTS:
            self.validate_tests_size(min_tests=self.TESTS_MIN, max_tests=self.TESTS_MAX)
        return tagged_args, positional_args
