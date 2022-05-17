from typing import Optional, List
import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.inline_mode import InlineQueryResult


class InlineQueryResultAudio(InlineQueryResult):
    def __init__(
        self,
        audio_url: str,
        thumb_url: Optional[str] = None,
        id: Optional[str] = None,
        title: str = None,
        mime_type: Optional[str] = None,
        description: Optional[str] = None,
        caption: Optional[str] = '',
        audio_duration: Optional[int] = 0,
        performer: Optional[str] = '',
        parse_mode: Optional[str] = object,
        caption_entities: List['types.MessageEntity'] = None,
        reply_markup: Optional['types.InlineKeyboardMarkup'] = None,
        input_message_content: Optional['types.InputMessageContent'] = None,
    ):
        super().__init__(
            'audio',
            id,
            input_message_content,
            reply_markup,
        )
        self.audio_url = audio_url
        self.thumb_url = thumb_url
        self.title = title
        self.mime_type = mime_type
        self.description = description
        self.caption = caption
        self.caption_entities = caption_entities
        self.parse_mode = parse_mode
        self.voice = self.mime_type == 'audio/ogg'
        self.performer = performer
        self.audio_duration = audio_duration
        self.reply_markup = reply_markup
        if mime_type == 'text/html' and input_message_content is None:
            raise ValueError(
                'input_message_content is required for audio with `text/html` mime type, not `(audio/mp3, audio/ogg)`',
            )

        self.input_message_content = input_message_content

    async def write(self, client: 'pyrogram.Client'):
        audio = raw.types.InputWebDocument(
            url=self.audio_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[
                raw.types.DocumentAttributeAudio(
                    duration=self.audio_duration,
                    title=self.title,
                    performer=self.performer,
                    voice=self.voice,
                ),
            ],
        )
        if self.thumb_url:
            thumb = raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type='image/jpeg',
                attributes=[],
            )
        else:
            thumb = None

        message, entities = (
            await utils.parse_text_entities(
                client, self.caption, self.parse_mode, self.caption_entities,
            )
        ).values()
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=audio,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities,
                )
            ),
        )
