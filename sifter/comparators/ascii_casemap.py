import string

from sifter.comparators.octet import ComparatorOctet

__all__ = ('ComparatorASCIICasemap',)

class ComparatorASCIICasemap(ComparatorOctet):

    COMPARATOR_ID = 'i;ascii-casemap'
    maketrans = None

    @classmethod
    def sort_key(cls, s):
        if cls.maketrans is None:
            try:
                cls.maketrans = str.maketrans
            except AttributeError:
                cls.maketrans = string.maketrans
        return s.translate(cls.maketrans(string.ascii_lowercase,
            string.ascii_uppercase))

ComparatorASCIICasemap.register()

class ComparatorASCIICasemapnoi(ComparatorOctet):

    COMPARATOR_ID = ';ascii-casemap'
    maketrans = None

    @classmethod
    def sort_key(cls, s):
        if cls.maketrans is None:
            try:
                cls.maketrans = str.maketrans
            except AttributeError:
                cls.maketrans = string.maketrans
        return s.translate(cls.maketrans(string.ascii_lowercase,
            string.ascii_uppercase))

ComparatorASCIICasemapnoi.register()
