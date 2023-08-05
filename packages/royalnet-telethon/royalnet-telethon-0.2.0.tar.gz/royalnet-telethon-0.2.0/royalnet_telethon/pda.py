"""
The PDA ("main" class) for the :mod:`royalnet_telethon` frontend.
"""

from __future__ import annotations
import royalnet.royaltyping as t

import logging
import asyncio
import royalnet.engineer as engi
import telethon as tt
import telethon.tl.custom as tlc
import enum

from .bullet.projectiles.message import TelegramMessageReceived, TelegramMessageEdited, TelegramMessageDeleted

log = logging.getLogger(__name__)


class TelethonPDAMode(enum.Enum):
    GLOBAL = enum.auto()
    CHAT = enum.auto()
    USER = enum.auto()
    CHAT_USER = enum.auto()


class TelethonPDA:
    """
    A PDA which handles :mod:`royalnet` input and output using a Telegram bot as a source.
    """

    def __init__(self,
                 tg_api_id: int,
                 tg_api_hash: str,
                 bot_username: str,
                 mode: TelethonPDAMode = TelethonPDAMode.CHAT_USER,
                 ):
        """
        Create a new :class:`.TelethonPDA` .

        Get API properties `here <https://my.telegram.org/apps>`_.

        :param tg_api_id: The Telegram ``api_id``.
        :param tg_api_hash: The Telegram ``api_hash``.
        :param mode: The mode to use for mapping dispensers.
        """

        log.debug(f"Creating new TelethonPDA...")

        self.dispensers: dict[t.Any, engi.Dispenser] = {}
        """
        The :class:`royalnet.engineer.dispenser.Dispenser`\\ s of this PDA.
        """

        self.conversations: t.List[engi.Conversation] = []
        """
        A :class:`list` of conversations to run before a new _event is :meth:`.put` in a 
        :class:`~royalnet.engineer.dispenser.Dispenser`.
        """

        self.client: tt.TelegramClient = tt.TelegramClient("bot", api_id=tg_api_id, api_hash=tg_api_hash)
        """
        The :mod:`telethon` Telegram _client that this PDA will use to interface with Telegram.
        """

        self._register_events()

        self.mode: TelethonPDAMode = mode
        """
        The mode to use for mapping dispensers.
        """

        self.bot_username: str = bot_username

    def _register_events(self):
        self.client.add_event_handler(callback=self._message_new, event=tt.events.NewMessage())
        self.client.add_event_handler(callback=self._message_edit, event=tt.events.MessageEdited())
        self.client.add_event_handler(callback=self._message_delete, event=tt.events.MessageDeleted())
        # self._client.add_event_handler(callback=self._message_read, _event=tt.events.MessageRead())
        # self._client.add_event_handler(callback=self._chat_action, _event=tt.events.ChatAction())
        # self._client.add_event_handler(callback=self._user_update, _event=tt.events.UserUpdate())
        # self._client.add_event_handler(callback=self._callback_query, _event=tt.events.CallbackQuery())
        # self._client.add_event_handler(callback=self._inline_query, _event=tt.events.InlineQuery())
        # self._client.add_event_handler(callback=self._album, _event=tt.events.Album())

    def _determine_key(self, event: tlc.message.Message):
        if self.mode == TelethonPDAMode.GLOBAL:
            return None
        elif self.mode == TelethonPDAMode.USER:
            if event.from_id:
                return event.from_id.user_id
            else:
                return event.peer_id.user_id
        elif self.mode == TelethonPDAMode.CHAT:
            return event.chat_id
        elif self.mode == TelethonPDAMode.CHAT_USER:
            if event.from_id:
                return event.chat_id, event.from_id.user_id
            else:
                return event.chat_id, event.peer_id.user_id
        else:
            raise TypeError("Invalid mode")

    async def _message_new(self, event: tlc.message.Message):
        await self.put_projectile(
            key=self._determine_key(event),
            proj=TelegramMessageReceived(event=event),
        )

    async def _message_edit(self, event: tlc.message.Message):
        await self.put_projectile(
            key=self._determine_key(event),
            proj=TelegramMessageEdited(event=event),
        )

    async def _message_delete(self, event: tlc.message.Message):
        await self.put_projectile(
            key=self._determine_key(event),
            proj=TelegramMessageDeleted(event=event),
        )

    async def run(self, bot_token: str) -> t.NoReturn:
        """
        Run the main loop of the :class:`.ConsolePDA` for ``cycles`` cycles, or unlimited cycles if the parameter is
        :data:`True`.
        """
        # Login to the Telegram API
        self.client: tt.TelegramClient = await self.client.start(bot_token=bot_token)
        await self.client.connect()
        await self.client.get_me()
        await self.client.catch_up()
        await self.client.run_until_disconnected()

    def register_conversation(self, conv: engi.Conversation) -> None:
        """
        Register a new conversation in the PDA.

        :param conv: The conversation to register.
        """
        log.info(f"Registering conversation: {conv!r}")
        self.conversations.append(conv)

    def unregister_conversation(self, conv: engi.Conversation) -> None:
        """
        Unregister a conversation from the PDA.

        :param conv: The conversation to unregister.
        """
        log.info(f"Unregistering conversation: {conv!r}")
        self.conversations.remove(conv)

    def register_partial(self, part: engi.PartialCommand, names: t.List[str]) -> engi.Command:
        """
        Register a new :class:`~royalnet.engineer.command.PartialCommand` in the PDA, converting it to a
        :class:`royalnet.engineer.Command` in the process.

        :param part: The :class:`~royalnet.engineer.command.PartialCommand` to register.
        :param names: The :attr:`~royalnet.engineer.command.Command.names` to register the command with.
        :return: The resulting :class:`~royalnet.engineer.command.Command`.
        """
        log.debug(f"Completing partial: {part!r}")
        if part.syntax:
            command = part.complete(pattern=rf"^/{{name}}(?:@{self.bot_username})?\s+{{syntax}}$", names=names)
        else:
            command = part.complete(pattern=rf"^/{{name}}(?:@{self.bot_username})?$", names=names)
        self.register_conversation(command)
        return command

    async def put_projectile(self, key: t.Any, proj: engi.Projectile) -> None:
        """
        Insert a new projectile into the dispenser.

        :param key: The key of the dispenser to interact with.
        :param proj: The projectile to put in the dispenser.
        """
        if key not in self.dispensers:
            log.debug(f"Dispenser not found, creating one...")
            self.dispensers[key] = engi.Dispenser()

        dispenser = self.dispensers[key]

        log.debug("Getting running loop...")
        loop = asyncio.get_running_loop()

        for conversation in self.conversations:
            log.debug(f"Creating run task for: {conversation!r}")
            loop.create_task(dispenser.run(conversation, _pda=self), name=f"{repr(conversation)}")

        log.debug("Running a _event loop cycle...")
        await asyncio.sleep(0)

        log.debug(f"Putting projectile {proj!r} in dispenser {dispenser!r}...")
        await dispenser.put(proj)

        log.debug("Awaiting another _event loop cycle...")
        await asyncio.sleep(0)


# Objects exported by this module
__all__ = (
    "TelethonPDA",
)
