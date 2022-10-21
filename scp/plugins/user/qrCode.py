from scp import user
import aiohttp
import os


__PLUGIN__ = 'qrCode'
__DOC__ = str(
    user.md.KanTeXDocument(
        user.md.Section(
            'Qrcode Encoding & Decoding',
            user.md.SubSection(
                'Encode',
                user.md.Code('(*prefix)qrGen {content}'),
            ),
            user.md.SubSection(
                'Decode',
                user.md.Code('(*prefix)qrRead {replied_media}'),
            ),
        ),
    ),
)


def _gen(content: str):
    return {
        'data': content,
        'config': {
            'body': 'circle-zebra',
            'eye': 'frame13',
            'eyeBall': 'ball14',
            'erf1': [],
            'erf2': [],
            'erf3': [],
            'brf1': [],
            'brf2': [],
            'brf3': [],
            'bodyColor': '#000000',
            'bgColor': '#FFFFFF',
            'eye1Color': '#000000',
            'eye2Color': '#000000',
            'eye3Color': '#000000',
            'eyeBall1Color': '#000000',
            'eyeBall2Color': '#000000',
            'eyeBall3Color': '#000000',
            'gradientColor1': '',
            'gradientColor2': '',
            'gradientType': 'linear',
            'gradientOnEyes': 'true',
            'logo': '',
            'logoMode': 'default',
        },
        'size': 1000,
        'download': 'imageUrl',
        'file': 'png',
    }


@user.on_message(user.filters.sudo & user.filters.command('qrGen'))
async def _(_, message: user.types.Message):
    if len(message.text.split()) == 1:
        return await message.delete()
    data = _gen(message.text.split(None, 1)[1])
    await message.reply_document(
        (await (
            await user.aioclient.post(
                'https://api.qrcode-monkey.com//qr/custom',
                json=data,
            )
        ).json())['imageUrl'].replace(
            '//api', 'https://api',
        ),
        quote=True,
    )


@user.on_message(user.filters.sudo & user.filters.reply & user.filters.command('qrRead'))
async def _(_, message: user.types.Message):
    if (
        not message.reply_to_message.document
        and not message.reply_to_message.photo
    ):
        return
    f = await message.reply_to_message.download()
    await message.reply(
        user.md.KanTeXDocument(
            user.md.Section(
                'qrCode Decoded:',
                user.md.KeyValueItem(
                    user.md.Bold('data'), user.md.Code(
                        await QrRead(f),
                    ),
                ),
            ),
        ), quote=True,
    )
    os.remove(f)


async def QrRead(file: str):
    async with user.aioclient.post(
        'http://api.qrserver.com/v1/read-qr-code/',
        data={'file': open(file, 'rb')},
    ) as resp:
        return (await resp.json())[0]['symbol'][0]['data']
