# type: ignore


import pytest

from sifter.grammar.tag import Tag as GrammarTag
from sifter.grammar.rule import Rule, RuleSyntaxError
from sifter.validators.number import Number
from sifter.validators.stringlist import StringList
from sifter.validators.tag import Tag as TagValidator


def test_too_many_args() -> None:
    class MockRuleNoArgs(Rule):
        HANDLER_TYPE = 'mock'
        HANDLER_ID = 'MOCKRULE'

    with pytest.raises(RuleSyntaxError):
        _ = MockRuleNoArgs([GrammarTag('IS'), 13, ])


def test_not_enough_args() -> None:
    class MockRuleTwoArgs(Rule):
        HANDLER_TYPE = 'mock'
        HANDLER_ID = 'MOCKRULE'
        TAGGED_ARGS = [
            Number(),
            StringList(),
        ]

    with pytest.raises(RuleSyntaxError):
        _ = MockRuleTwoArgs([13, ])


def test_allowed_tag() -> None:
    mock_validator = TagValidator(['MOCK', 'IS', ])
    assert mock_validator.validate([GrammarTag('IS')], 0) == 1


def test_allowed_single_tag() -> None:
    # test the case for a non-list single tag name
    mock_validator = TagValidator('IS')
    assert mock_validator.validate([GrammarTag('IS')], 0) == 1


def test_not_allowed_tag() -> None:
    mock_validator = TagValidator(['MOCK', 'FOO', ])
    assert mock_validator.validate([GrammarTag('IS')], 0) == 0


def test_not_allowed_single_tag() -> None:
    # test the case for a non-list single tag name. test when the tag is a
    # substring of the allowed tag.
    mock_validator = TagValidator('ISFOO')
    assert mock_validator.validate([GrammarTag('IS')], 0) == 0
