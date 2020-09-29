from typing import Text

import sifter.handler


def register(extension_name: Text) -> None:
    sifter.handler.register('extension', extension_name, True)
