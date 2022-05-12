from pyrogram import (
    Client,
    filters,
    types,
    raw,
    errors,
    session,
    handlers,
    enums,
)
from scp.core.filters.Command import command
from configparser import ConfigParser
from kantex import md as Markdown
from aiohttp import ClientSession
import asyncio
import logging

config = ConfigParser()
config.read('config.ini')


class client(Client):
    def __init__(
        self,
        name: str,
        aioclient=ClientSession,
        api_id: int = config.getint('pyrogram', 'api_id'),
        api_hash: str = config.get('pyrogram', 'api_hash'),
        test_mode: bool = config.getboolean('pyrogram', 'test_mode'),
    ):
        self.name = name
        self.api_id = api_id
        self.api_hash = api_hash
        self.test_mode = test_mode
        self.me = {}
        super().__init__(
            f'{self.name}-test_mode' if self.test_mode else self.name,
            workers=16,
            api_id=self.api_id,
            api_hash=self.api_hash,
            test_mode=self.test_mode,
        )

        self.aioclient = aioclient()

    async def start(self):
        await super().start()
        logging.warning(
            f'logged in as {(await super().get_me()).first_name}.',
        )

    async def stop(self, *args):
        logging.warning(
            f'logged out from {(await super().get_me()).first_name}.',
        )
        await super().stop()

    def command(self, *args, **kwargs):
        return command(*args, **kwargs)

    async def invoke(
        self,
        query: raw.core.TLObject,
        retries: int = session.Session.MAX_RETRIES,
        timeout: float = session.Session.WAIT_TIMEOUT,
        sleep_threshold: float = None
    ) -> raw.core.TLObject:
        while True:
            try:
                return await super().invoke(
                    query=query,
                    retries=retries,
                    timeout=timeout,
                    sleep_threshold=sleep_threshold,
                )
            except (errors.SlowmodeWait, errors.FloodWait) as e:
                logging.warning(f'Sleeping for - {e.x} | {e}')
                await asyncio.sleep(e.x + 2)
            except OSError:
                # attempt to fix TimeoutError on slower internet connection
                # await self.session.stop()
                # await self.session.start()
                ...

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

    filters = filters
    enums = enums
    raw = raw
    types = types
    handlers = handlers
    md = Markdown
    exceptions = errors
    _config = ConfigParser()
    _config.read('config.ini')
    _sudo = []
    for x in _config.get('scp-5170', 'SudoList').split():
        _sudo.append(int(x))
    sudo = (filters.me | filters.user(_sudo))
    log_channel = _config.getint('scp-5170', 'LogChannel')
