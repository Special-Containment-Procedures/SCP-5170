import pyrogram
from pyrogram import utils, file_id
from scp import core
from configparser import ConfigParser
from kantex import md as Markdown
from aiohttp import ClientSession
import asyncio
import logging
import os
import re
from typing import Union, Optional, List, BinaryIO, Callable
from datetime import datetime

config = ConfigParser()
with open('config.ini') as configFile:
    config.read_file(configFile)


class Client(pyrogram.Client):
    def __init__(
        self,
        name: str,
        aioclient=ClientSession,
        api_id: int = config.getint('pyrogram', 'api_id'),
        api_hash: str = config.get('pyrogram', 'api_hash'),
        test_mode: bool = config.getboolean('pyrogram', 'test_mode'),
        cache=None,
    ):
        if cache is None:
            cache = {}
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.test_mode = test_mode
        self.md = Markdown
        self.exceptions = pyrogram.errors
        self.filters = pyrogram.filters
        self.types = pyrogram.types
        self.raw = pyrogram.raw
        self.enums = pyrogram.enums
        self.handlers = pyrogram.handlers
        self.config = config
        self.cache = cache
        self.sudo = [
            int(x) for x in self.config.get(
                'scp-5170', 'SudoList',
            ).split()
        ]
        self.aioclient = aioclient()
        super().__init__(
            f'{self.name}-test_mode' if self.test_mode else self.name,
            workers=16,
            api_id=self.api_id,
            api_hash=self.api_hash,
            test_mode=self.test_mode,
        )

    def __getattr__(self, method_name):
        if not any(c.isupper() for c in method_name):
            return super().__getattribute__(method_name)

        async def invoke(**kwargs):
            for y in [
                x for x in dir(
                    self.raw.functions,
                ) if not x.startswith('__') and not x[0].isupper()
            ]:
                if method := getattr(
                    getattr(self.raw.functions, y, None),
                    method_name,
                    None,
                ):
                    return await self.invoke(method(**kwargs))
            raise AttributeError(
                f"'Client' object has no attribute '{method_name}'",
            )
        return invoke

    async def start(self):
        await super().start()
        setattr(
            self.filters, 'sudo',
            (self.filters.me | self.filters.user(self.sudo)),
        )
        setattr(self.filters, 'command', core.filters.command)
        logging.warning(
            f'logged in as {self.me.first_name}.',
        )

    async def stop(self):
        logging.warning(
            f'logged out from {super.me.first_name}.',
        )
        await super().stop()

    async def invoke(
        self,
        query: pyrogram.raw.core.TLObject,
        retries: int = pyrogram.session.Session.MAX_RETRIES,
        timeout: float = pyrogram.session.Session.WAIT_TIMEOUT,
        sleep_threshold: float = None
    ) -> pyrogram.raw.core.TLObject:
        while True:
            try:
                return await super().invoke(
                    query=query,
                    retries=retries,
                    timeout=timeout,
                    sleep_threshold=sleep_threshold,
                )
            except (
                self.exceptions.SlowmodeWait,
                self.exceptions.FloodWait,
            ) as e:
                logging.warning(f'Sleeping for - {e.x} | {e}')
                await asyncio.sleep(e.x + 2)
            except OSError:
                # attempt to fix TimeoutError on slower internet connection
                # await self.session.stop()
                # await self.session.start()
                ...

    async def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional['pyrogram.enums.ParseMode'] = None,
        entities: List['pyrogram.types.MessageEntity'] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        reply_markup: Union[
            'Client.types.InlineKeyboardMarkup',
            'Client.types.ReplyKeyboardMarkup',
            'Client.types.ReplyKeyboardRemove',
            'Client.types.ForceReply',
        ] = None
    ) -> 'Client.types.Message':
        if reply_markup and not self.me.is_bot:
            unique = str(self.rnd_id())
            self.cache[unique] = self.types.InlineQueryResultArticle(
                title='None',
                input_message_content=self.types.InputTextMessageContent(
                    text,
                    disable_web_page_preview=disable_web_page_preview,
                    parse_mode=parse_mode,
                ),
                reply_markup=reply_markup,
            )
            # do the magic here
            x = await super().get_inline_bot_results(
                self.cache['botUser'].me.username,
                f'inline_message {unique}',
            )
            output = await super().send_inline_bot_result(
                chat_id=chat_id,
                query_id=x.query_id,
                result_id=x.results[0].id,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
            )
            del self.cache[unique]
            return output
        return await super().send_message(
            chat_id,
            text,
            parse_mode,
            entities,
            disable_web_page_preview,
            disable_notification,
            reply_to_message_id,
            schedule_date,
            protect_content,
            reply_markup,
        )

    async def send_photo(
        self: 'pyrogram.Client',
        chat_id: Union[int, str],
        photo: Union[str, BinaryIO],
        caption: str = '',
        parse_mode: Optional['Client.enums.ParseMode'] = None,
        caption_entities: List['Client.types.MessageEntity'] = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        reply_markup: Union[
            'Client.types.InlineKeyboardMarkup',
            'Client.types.ReplyKeyboardMarkup',
            'Client.types.ReplyKeyboardRemove',
            'Client.types.ForceReply',
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional['Client.types.Message']:  # sourcery skip: last-if-guard
        if reply_markup and not self.me.is_bot:
            unique = str(self.rnd_id())
            if os.path.isfile(photo):
                media = self.raw.types.InputMediaUploadedPhoto(
                    file=await self.cache['botUser'].save_file(photo),
                )
                outfile = await self.cache['botUser'].UploadMedia(
                    peer=self.raw.types.InputPeerSelf(),
                    media=media,
                )
                photo_file = self.types.Photo._parse(
                    self.cache['botUser'],  photo=outfile.photo,
                )
                self.cache[unique] = self.types.InlineQueryResultCachedPhoto(
                    photo_file_id=photo_file.file_id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            elif re.match('^https?://', photo):
                self.cache[unique] = self.types.InlineQueryResultPhoto(
                    photo_url=photo,
                    thumb_url=None,
                    caption=caption,
                    reply_markup=reply_markup,
                )
            else:
                message = await self.send_photo(self.config.getint('.internal', 'databasechannel'), photo)
                message = await self.cache['botUser'].get_messages(
                    self.config.getint(
                        '.internal', 'databasechannel',
                    ), message.id,
                )
                self.cache[unique] = self.types.InlineQueryResultCachedPhoto(
                    photo_file_id=message.photo.file_id,
                    caption=caption,
                    reply_markup=reply_markup,
                )
                await super().delete_messages(self.config.getint('.internal', 'databasechannel'), message.id)
            # do the magic here
            x = await super().get_inline_bot_results(
                self.cache['botUser'].me.username,
                f'inline_message {unique}',
            )
            output = await super().send_inline_bot_result(
                chat_id=chat_id,
                query_id=x.query_id,
                result_id=x.results[0].id,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
            )
            del self.cache[unique]
            return output
        return await super().send_photo(
            chat_id,
            photo,
            caption,
            parse_mode,
            caption_entities,
            ttl_seconds,
            disable_notification,
            reply_to_message_id,
            schedule_date,
            protect_content,
            reply_markup,
            progress,
            progress_args,
        )
    # async def send_audio(

    # ):
    #     ...
    # from Kantek
    async def resolve_url(self, url: str) -> str:
        if not url.startswith('http'):
            url: str = f'http://{url}'
        async with self.aioclient.get(
            f'http://expandurl.com/api/v1/?url={url}',
        ) as response:
            e = await response.text()
        return e if e != 'false' and e[:-1] != url else None

    async def netcat(
        self,
        host: str,
        port: int,
        content: str
    ):
        reader, writer = await asyncio.open_connection(
            host, port,
        )
        writer.write(content.encode())
        await writer.drain()
        data = (await reader.read(100)).decode().strip('\n\x00')
        writer.close()
        await writer.wait_closed()
        return data
