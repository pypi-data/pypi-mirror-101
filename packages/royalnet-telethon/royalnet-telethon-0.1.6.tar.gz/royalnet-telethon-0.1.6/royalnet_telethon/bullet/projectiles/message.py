from __future__ import annotations
from ._imports import *

from ..contents.__init__ import TelegramMessage


class TelegramMessageReceived(p.MessageReceived):
    def __init__(self, event: tlc.Message):
        super().__init__()
        self.event: tlc.Message = event

    def __hash__(self) -> int:
        return self.event.id

    @ap.async_cached_property
    async def message(self) -> TelegramMessage:
        return TelegramMessage(msg=self.event)


class TelegramMessageEdited(p.MessageEdited):
    def __init__(self, event: tlc.Message):
        super().__init__()
        self.event: tlc.Message = event

    def __hash__(self) -> int:
        return self.event.id

    @ap.async_cached_property
    async def message(self) -> TelegramMessage:
        return TelegramMessage(msg=self.event)


class TelegramMessageDeleted(p.MessageDeleted):
    def __init__(self, event: tlc.Message):
        super().__init__()
        self.event: tlc.Message = event

    def __hash__(self) -> int:
        return self.event.id

    @ap.async_cached_property
    async def message(self) -> TelegramMessage:
        return TelegramMessage(msg=self.event)


__all__ = (
    "TelegramMessageReceived",
    "TelegramMessageEdited",
    "TelegramMessageDeleted",
)
