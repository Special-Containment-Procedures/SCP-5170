(import [scp[user bot]])

(defn/a config-manager [_ ^bot.types.Message message]
    (setv doc (bot.md.KanTeXDocument)
        sec (bot.md.Section "Configurations"))
    (for [(, x y) (.items (.get bot.config.__dict__ "_sections"))]
        (setv subsec (bot.md.SubSection x))
        (for [(, i n) (.items y)]
            (.append subsec (bot.md.KeyValueItem (bot.md.Bold i) (bot.md.Code n))))
        (.append sec subsec))
    (.append doc sec)
    (return (await (message.reply doc
        :reply_markup (bot.types.InlineKeyboardMarkup
            [[(bot.types.InlineKeyboardButton "Edit Config" :callback_data "edit/config")]])))))


(defn/a edit-config [_ ^bot.types.CallbackQuery query]
    (setv buttons [])
    (for [(, _ y) (.items (.get bot.config.__dict__ "_sections"))]
        (for [i y] (.append buttons [(bot.types.InlineKeyboardButton i :callback_data f"config/{i}")])))
    (return (await (query.edit_message_text "choose a config key to edit in config.ini"
        :reply_markup (bot.types.InlineKeyboardMarkup buttons)))))


(bot.add_handler
    :handler (bot.handlers.MessageHandler
    :callback config-manager
    :filters (& (bot.filters.user user.me.id) (bot.filters.command "config" :prefixes "/") bot.filters.private)))

(bot.add_handler
    :handler (bot.handlers.CallbackQueryHandler
    :callback edit-config
    :filters (& (bot.filters.user user.me.id) (bot.filters.regex "^edit/config"))))
