"""
# Flapi > Context

Code for keeping track of the Flapi context, so that commands can be forwarded
to the FL Studio API correctly.
"""
from dataclasses import dataclass
from mido.ports import BaseOutput, BaseInput
from types import FunctionType
from typing import Optional
from flapi.errors import FlapiContextError


@dataclass
class FlapiContext:
    outgoing_messages: BaseOutput
    """
    The Mido port that Flapi uses to send messages to FL Studio
    """

    incoming_messages: BaseInput
    """
    The Mido port that Flapi uses to receive messages from FL Studio
    """

    functions_backup: dict[str, dict[str, FunctionType]]
    """
    References to all the functions we replaced in the FL Studio API, so that
    we can set them back as required.
    """


context: Optional[FlapiContext] = None
"""
The current context for Flapi
"""


def setContext(new_context: FlapiContext):
    """
    Set the context for Flapi
    """
    global context
    context = new_context


def getContext() -> FlapiContext:
    """
    Get a reference to the Flapi context
    """
    if context is None:
        raise FlapiContextError(
            "Could not find Flapi context. Perhaps you haven't initialised "
            "Flapi by calling `flapi.enable()`."
        )
    return context


def popContext() -> FlapiContext:
    """
    Clear the Flapi context, returning its value so that clean-up can be
    performed
    """
    global context
    if context is None:
        raise FlapiContextError(
            "Could not find Flapi context. Perhaps you haven't initialised "
            "Flapi by calling `flapi.enable()`."
        )
    ret = context
    context = None
    return ret
