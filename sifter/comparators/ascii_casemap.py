import string
from typing import Text
from sifter.comparators.octet import ComparatorOctet

maketrans = str.maketrans


class ComparatorASCIICasemap(ComparatorOctet):

    HANDLER_ID = 'i;ascii-casemap'

    @classmethod
    def sort_key(cls, s: Text) -> Text:
        return s.translate(
            str.maketrans(
                string.ascii_lowercase,
                string.ascii_uppercase
            )
        )


class ComparatorASCIICasemapnoi(ComparatorOctet):

    HANDLER_ID = ';ascii-casemap'

    @classmethod
    def sort_key(cls, s: Text) -> Text:
        return s.translate(
            str.maketrans(
                string.ascii_lowercase,
                string.ascii_uppercase
            )
        )
