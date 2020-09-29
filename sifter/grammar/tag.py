from typing import Text


class Tag(str):

    def __str__(self) -> Text:
        return ":%s" % super().__str__()

    def __repr__(self) -> Text:
        return "%s('%s')" % ('Tag', super().__repr__())
