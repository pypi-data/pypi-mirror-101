import abc
import typing

import Microsoft.Win32.SafeHandles
import System
import System.Security.Authentication.ExtendedProtection


class ChannelBindingKind(System.Enum):
    """This class has no documentation."""

    Unknown = 0

    Unique = ...

    Endpoint = ...


class ChannelBinding(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def Size(self) -> int:
        ...

    @typing.overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def __init__(self, ownsHandle: bool) -> None:
        """This method is protected."""
        ...


