from scp import user, bot


@bot.on_message(
    (bot.filters.user(bot.sudo) | bot.filters.user(user.me.id))
    & bot.filters.command('sessions', prefixes='/'),
)
async def _(_, message: user.types.Message):
    auths = await user.GetAuthorizations()
    try:
        session_hash = int(message.command[1])
    except IndexError:
        session_hash = 0
    for auth in auths.authorizations:
        if auth.hash == session_hash:
            sec = user.md.Section(
                "Active Session (This Session)",
                user.md.KeyValueItem(
                    user.md.Bold('device_model'), user.md.Code(auth.device_model)),
                user.md.KeyValueItem(
                    user.md.Bold('platform'), user.md.Code(auth.platform)),
                user.md.KeyValueItem(
                    user.md.Bold('sys_version'), user.md.Code(auth.system_version)),
                user.md.KeyValueItem(
                    user.md.Bold('api_id'), user.md.Code(auth.api_id)),
                user.md.KeyValueItem(
                    user.md.Bold('app'),
                    user.md.Code(f"{auth.app_name}({auth.app_version}) {'⭐' if auth.official_app else ''}")),
                user.md.KeyValueItem(
                    user.md.Bold('country'), user.md.Code(f"{auth.country} {auth.ip}"))
            )
            return await message.reply(
                user.md.KanTeXDocument(sec),
                reply_markup=bot.types.InlineKeyboardMarkup(
                    [
                        [bot.types.InlineKeyboardButton(f"Calls {'❎' if auth.call_requests_disabled else '✅'}", callback_data=f'ses_{auth.hash}_c'),bot.types.InlineKeyboardButton(f"Secret Chats {'❎' if auth.encrypted_requests_disabled else '✅'}", callback_data=f'ses_{auth.hash}_s')],
                        [] if auth.hash == 0 else [bot.types.InlineKeyboardButton('Log Out', callback_data=f'logout_{auth.hash}')],
                        [bot.types.InlineKeyboardButton('Other Sessions', switch_inline_query_current_chat="getAuths")]
                    ]
                )
            )

@bot.on_callback_query(
    (bot.filters.user(bot.sudo) | bot.filters.user(user.me.id))
    & bot.filters.regex('logout_'),
)
async def _(_, query: user.types.CallbackQuery):
    await user.ResetAuthorization(hash=int(query.data.split('_')[1]))
    await query.message.delete()
    return await query.answer("Session has been Destroyed!", show_alert=True)

# WIP
@bot.on_callback_query(
    (bot.filters.user(bot.sudo) | bot.filters.user(user.me.id))
    & bot.filters.regex('ses_'),
)
async def _(_, query: user.types.CallbackQuery):
    q = query.data.split('_')
    if q[2] == 'c':
        data = {
            'call_requests_disabled': query.message.reply_markup.inline_keyboard[0][0].text.split(' ')[1] == '✅'
        }

    elif q[2] == 's':
        data = {
            'encrypted_requests_disabled': query.message.reply_markup.inline_keyboard[0][1].text.split(' ')[1] == '✅'
        }

    else:
        ...
    await user.ChangeAuthorizationSettings(
            hash=int(q[1]),
            **data
    )
    await query.message.edit_reply_markup(reply_markup=user.types.InlineKeyboardMarkup([[bot.types.InlineKeyboardButton(f"Calls {'✅' if q[2] == 'c' and query.message.reply_markup.inline_keyboard[0][0].text.split(' ')[-1] != '✅' else '❎'}", callback_data=f'ses_{q[1]}_c'), bot.types.InlineKeyboardButton(f"Secret Chats {'✅' if q[2] == 's' and query.message.reply_markup.inline_keyboard[0][1].text.split(' ')[-1] != '✅' else '❎'}", callback_data=f'ses_{q[1]}_s')], [bot.types.InlineKeyboardButton('Log Out', callback_data=f'logout_{q[1]}')], [bot.types.InlineKeyboardButton('Other Sessions', switch_inline_query_current_chat="getAuths")]]))
    return await query.answer(f'{"Secret Chat" if q[2] == "s" else "Calls"} settings changed.')

@bot.on_inline_query(
    user.filters.user(
        user.me.id,
    )
    & user.filters.regex('^getAuths'),
)
async def _(_, query: bot.types.InlineQuery):
    auths = await user.GetAuthorizations()
    answers = [user.types.InlineQueryResultArticle(title=f"{auth.app_name}({auth.app_version}) {'⭐' if auth.official_app else ''}", description=f"{auth.device_model} || {auth.country} {auth.ip}", input_message_content=user.types.InputTextMessageContent(f'/sessions {auth.hash}')) for auth in auths.authorizations if auth.hash != 0]
    await query.answer(
        answers,
        cache_time=0,
    )