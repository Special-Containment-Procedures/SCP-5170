from scp import bot, user


@bot.on_inline_query(
    user.filters.user(
        user.me.id,
    )
    & bot.filters.regex('^inline'),
)
async def _(_, query: bot.types.CallbackQuery):
    task = query.query.split(' ')[1]
    return await query.answer([user.cache[task]], cache_time=0)
