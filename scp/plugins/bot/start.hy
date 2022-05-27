(import [scp[bot user __version__ __longVersion__]])


(defn/a start-command [_ message]
    (setv text
        (user.md.KanTeXDocument
            (user.md.Section "SCP-5170"
                (user.md.KeyValueItem
                    (user.md.Bold "Userbot Status")
                        (user.md.Code "Running"))
                (user.md.KeyValueItem
                    (user.md.Bold "Version")
                        (user.md.Link __version__ f"https://github.com/Special-Containment-Procedures/SCP-5170/commit/{__longVersion__}"))
            )))
    (await (message.reply
        text
        :reply_markup
            (bot.types.InlineKeyboardMarkup
                [[(bot.types.InlineKeyboardButton :text "help" :callback_data "help_back")]])
        :disable_web_page_preview True))
)



(bot.add_handler
    :handler (bot.handlers.MessageHandler
    :callback start-command
    :filters (& (| (bot.filters.user bot.sudo) (bot.filters.user user.me.id)) (bot.filters.command "start" :prefixes "/"))))
