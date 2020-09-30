from typing import (
    Text,
    TextIO
)


from sifter.grammar.grammar import SieveParser
from sifter.grammar.command_list import CommandList


def parse_file(filehandle: TextIO, tracking: int = 0) -> CommandList:
    return parse_string(filehandle.read(), tracking=tracking)


def parse_string(rules: Text, tracking: int = 0) -> CommandList:
    p = SieveParser()
    return p.parse(rules, tracking)
