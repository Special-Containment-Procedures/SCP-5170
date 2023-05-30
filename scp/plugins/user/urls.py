from scp import user


__PLUGIN__ = 'follow'
__DOC__ = str(
    user.md.KanTeXDocument(
        user.md.Section(
            'HTTP(s) Tools',
            user.md.SubSection(
                'Redirect',
                user.md.Code('(*prefix)url {url}'),
            ),
        ),
    ),
)


@user.on_message(user.filters.sudo & user.filters.command('url'))
async def _(_, message: user.types.Message):
    if len(message.command) == 1:
        return await message.delete()
    link = message.command[1]
    text = user.md.KanTeXDocument(
        user.md.Section(
            'Redirect',
            user.md.KeyValueItem(
                user.md.Bold('Original URL'), user.md.Code(link),
            ),
            user.md.KeyValueItem(
                user.md.Bold('Followed URL'),
                user.md.Code(await user.resolve_url(link)),
            ),
        ),
    )
    await message.reply(text, quote=True)
