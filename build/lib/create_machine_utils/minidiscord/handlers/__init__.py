from . import CompleteHandler

from . import ArgumentErrors
from . import CooldownErrors
from . import ExtensionErrors
from . import NotFoundErrors
from . import PermissionErrors
from . import WrongPlaceErrors


def setup(handler):
    CompleteHandler.setup(handler)

    ArgumentErrors.setup(handler)
    CooldownErrors.setup(handler)
    ExtensionErrors.setup(handler)
    NotFoundErrors.setup(handler)
    PermissionErrors.setup(handler)
    WrongPlaceErrors.setup(handler)
