import uuid
from typing import Union

MULAMBDA = "\u03bc\u03bb"


def short_uid():
    return str(uuid.uuid4().hex[:8])


Number = Union[int, float]
