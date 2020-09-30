# type: ignore

import pytest

from sifter.handler import ExtensionRegistry
from sifter.grammar.state import EvaluationState


def test_grammar():
    ExtensionRegistry.register_extension('ext1')
    ExtensionRegistry.register_extension('ext2')
    state = EvaluationState()

    state.require_extension('ext1')

    assert state.check_required_extension('ext1', 'ext1') is True

    with pytest.raises(RuntimeError):
        state.check_required_extension('ext2', 'ext2')
