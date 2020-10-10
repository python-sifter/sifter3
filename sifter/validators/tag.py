from typing import (
    TYPE_CHECKING,
    Union,
    Optional,
    Text,
    List,
    Tuple,
    SupportsInt
)

from sifter.grammar.validator import Validator
from sifter.grammar.rule import RuleSyntaxError
from sifter.grammar import tag
from sifter.validators.stringlist import StringList
from sifter.extensions import ExtensionRegistry

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String


class Tag(Validator):

    def __init__(
        self,
        allowed_tags: Optional[Union[Text, Tuple[Text, ...]]] = None,
        tag_arg_validators: Optional[Tuple[Validator, ...]] = None
    ) -> None:
        self.tag_arg_validators: Tuple[Validator, ...]
        super().__init__()
        self.allowed_tags: Optional[Tuple[Text, ...]] = None
        if isinstance(allowed_tags, str):
            self.allowed_tags = (allowed_tags, )
        else:
            self.allowed_tags = allowed_tags
        if tag_arg_validators is None:
            self.tag_arg_validators = ()
        else:
            self.tag_arg_validators = tag_arg_validators

    def validate(
        self,
        arg_list: List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]],
        starting_index: int
    ) -> Optional[int]:
        if starting_index >= len(arg_list):
            return 0
        if not isinstance(arg_list[starting_index], tag.Tag):
            return 0

        if self.allowed_tags is not None:
            if arg_list[starting_index] not in self.allowed_tags:
                return 0
        validated_args = 1

        for arg_validator in self.tag_arg_validators:
            num_valid_args = arg_validator.validate(
                arg_list,
                starting_index + validated_args
            )
            if num_valid_args and num_valid_args > 0:
                validated_args += num_valid_args
            else:
                return 0

        return validated_args


class MatchType(Tag):

    def __init__(self) -> None:
        super().__init__(('IS', 'CONTAINS', 'MATCHES', 'REGEX'))


class Comparator(Tag):

    def __init__(self) -> None:
        super().__init__(
            ('COMPARATOR',),
            (StringList(1),),
        )

    def validate(
        self,
        arg_list: List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]],
        starting_index: int
    ) -> Optional[int]:
        validated_args = super().validate(
            arg_list,
            starting_index
        )
        if isinstance(arg_list, list):
            if validated_args and validated_args > 0:
                val = arg_list[starting_index + 1]
                if not isinstance(val, list):
                    raise RuleSyntaxError(
                        "'%s' comparator is unknown/unsupported"
                        % arg_list[starting_index + 1]
                    )
                if not ExtensionRegistry.get_comparator(val[0]):
                    raise RuleSyntaxError(
                        "'%s' comparator is unknown/unsupported"
                        % val[0]
                    )
        return validated_args


class BodyTransform(Tag):

    def __init__(self) -> None:
        super(BodyTransform, self).__init__(('RAW', 'CONTENT', 'TEXT',))

    def validate(
        self,
        arg_list: List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]],
        starting_index: int
    ) -> Optional[int]:
        validated_args = super(BodyTransform, self).validate(arg_list, starting_index)
        if validated_args is None:
            raise ValueError('unexpected return value from super in BodyTransform')

        if validated_args > 0 and arg_list[starting_index] == 'CONTENT':
            content_args = StringList().validate(arg_list, starting_index + validated_args)
            if content_args is None:
                raise ValueError('unexpected return value from StringList.validate')
            if content_args > 0:
                return validated_args + content_args
            raise RuleSyntaxError("body :content requires argument")
        return validated_args
