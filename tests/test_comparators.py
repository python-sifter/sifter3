# type: ignore

import pytest

from sifter.extensions import ExtensionRegistry
import sifter.comparator
from sifter.grammar.comparator import Comparator


def test_mock_comparator() -> None:
    class MockComparator(Comparator):
        HANDLER_ID = 'i;vnd-mock'

    ExtensionRegistry.register_handler(MockComparator)
    with pytest.raises(RuntimeError):
        sifter.comparator.get_match_fn('i;vnd-mock', 'IS')
