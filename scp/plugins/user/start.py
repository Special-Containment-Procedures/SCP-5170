from scp import user, __version__, bot, RUNTIME, __longVersion__
from hy import __version__ as hyVer
from pyrogram import __version__ as pyroVer
import time
from scp.utils.parser.timeUtils import HumanizeTime
from scp.utils.unpack import unpackInlineMessage  # type: ignore
from scp.utils.cache import Messages  # type: ignore


@user.on_message(
    user.filters.sudo & user.filters.command('scp'),
)
async def _(_, message: user.types.Message):
    start = time.time()
    m = await user.send_message('me', '.')
    end = time.time()
    await m.delete()
    with user.storage.lock, user.storage.conn:
        groups = user.storage.conn.execute(
            'SELECT COUNT(id) FROM peers WHERE type in ("group", "supergroup", "channel")'
        ).fetchone()
        users = user.storage.conn.execute(
            'SELECT COUNT(id) FROM peers WHERE type in ("user", "bot")').fetchone()
    text = user.md.KanTeXDocument(user.md.Section('SCP-5170', user.md.SubSection(f"version: {user.md.Link(__version__, f'https://github.com/Special-Containment-Procedures/SCP-5170/commit/{__longVersion__}')}", user.md.KeyValueItem(user.md.Bold('dc_id'), user.md.Code(await user.storage.dc_id()),), user.md.KeyValueItem(user.md.Bold('ping_dc'), user.md.Code(f'{round((end - start) * 1000, 3)}ms'),), user.md.KeyValueItem(user.md.Bold('peer_users'), user.md.Code(f'{users[0]} users'),), user.md.KeyValueItem(user.md.Bold('peer_groups'), user.md.Code(f'{groups[0]} groups'),), user.md.KeyValueItem(user.md.Bold('scp_uptime'), user.md.Code(HumanizeTime(time.time() - RUNTIME)),), user.md.KeyValueItem(user.md.Bold('message_recieved'), user.md.Code(str(len(Messages))),), user.md.KeyValueItem(user.md.Bold('base'), user.md.Code(f'pyro({pyroVer})/hy({hyVer})')))))
    return await message.reply(
        text,
        reply_markup=bot.types.InlineKeyboardMarkup(
            [[
                bot.types.InlineKeyboardButton(
                    'Source', url='https://github.com/Special-Containment-Procedures/SCP-5170',
                ),
                bot.types.InlineKeyboardButton(
                    'close', callback_data='close_message',
                ),
            ]],
        ),
        disable_web_page_preview=True,
    )


@bot.on_callback_query(
    (bot.filters.user(bot.sudo) | bot.filters.user(user.me.id))
    & bot.filters.regex('^close_message'),
)
async def _(_, query: user.types.CallbackQuery):
    unPacked = unpackInlineMessage(query.inline_message_id)
    await user.delete_messages(
        chat_id=unPacked.chat_id,
        message_ids=unPacked.message_id,
    )
