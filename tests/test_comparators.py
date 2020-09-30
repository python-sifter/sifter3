# type: ignore

import pytest

import sifter.handler
import sifter.comparator
from sifter.grammar.comparator import Comparator


def test_mock_comparator() -> None:
    class MockComparator(Comparator):
        COMPARATOR_ID = 'i;vnd-mock'

    sifter.handler.ExtensionRegistry.register_handler(MockComparator)
    with pytest.raises(RuntimeError):
        sifter.comparator.get_match_fn('i;vnd-mock', 'IS')
