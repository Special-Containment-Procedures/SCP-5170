from scp import user, bot


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
