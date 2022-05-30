from scp import bot, user


@bot.on_callback_query(
    bot.filters.user(
        user.me.id,
    )
    & bot.filters.regex('^config'),
)
async def _(_, query: bot.types.CallbackQuery):
    toEdit = query.data.split('/')[1]
    for x, y in bot.config.__dict__['_sections'].items():
        for i, n in y.items():
            if i == toEdit:
                await query.edit_message_text(
                    bot.md.KanTeXDocument(
                        bot.md.Section(
                            'EditConfig current key and value',
                            bot.md.KeyValueItem(
                                bot.md.Bold(i),
                                bot.md.Code(n),
                            ),
                        ),
                    ),
                )
                editConfig = await query.from_user.ask(
                    f'send me the value to change in {i}',
                )
                bot.config.set(x, i, editConfig.text)
                with open('config.ini', 'w') as configfile:
                    bot.config.write(configfile)
                return await query.message.reply(
                    bot.md.KanTeXDocument(
                        bot.md.Section(
                            'Success',
                            bot.md.SubSection(
                                'Changes:',
                                bot.md.KeyValueItem(
                                    bot.md.Bold(
                                        i,
                                    ), bot.md.Code(editConfig.text),
                                ),
                            ),
                        ),
                    ),
                )
