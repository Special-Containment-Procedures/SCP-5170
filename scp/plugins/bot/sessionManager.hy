(import [scp[user bot]])


(defn/a session-manager [_ ^bot.types.Message message]
    (setv auths (await (user.GetAuthorizations))
        session-hash (try (int (get message.command 1)) (except [IndexError] 0)))
    (for [auth auths.authorizations]
        (if (= auth.hash session-hash)
            (setv section (user.md.Section "Active Session"
                (user.md.KeyValueItem 
                    (user.md.Bold "device_model") (user.md.Code auth.device_model))
                (user.md.KeyValueItem 
                    (user.md.Bold "platform") (user.md.Code auth.platform))
                (user.md.KeyValueItem 
                    (user.md.Bold "sys_version") (user.md.Code auth.system_version))
                (user.md.KeyValueItem 
                    (user.md.Bold "api_id") (user.md.Code auth.api_id))
                (user.md.KeyValueItem 
                    (user.md.Bold "app") (user.md.Code f"{auth.app_name}({auth.app_version}) {(if auth.official_app \"⭐\" \"\")}"))
                (user.md.KeyValueItem 
                    (user.md.Bold "country") (user.md.Code f"{auth.country} {auth.ip}"))))))
            (return (await (message.reply
                (user.md.KanTeXDocument section)
                :reply_markup (bot.types.InlineKeyboardMarkup 
                [[(bot.types.InlineKeyboardButton f"Calls {(if auth.call_requests_disabled \"✅\"\"❎\")}" :callback_data f"ses_{auth.hash}_c")
                    (bot.types.InlineKeyboardButton f"Secret Chats {(if auth.encrypted_requests_disabled \"✅\"\"❎\")}" :callback_data f"ses_{auth.hash}_s")]
                    (if (= auth.hash 0) [] [(bot.types.InlineKeyboardButton "Log Out" :callback_data f"logout_{auth.hash}")])
                    [(bot.types.InlineKeyboardButton "Other Sessions" :switch_inline_query_current_chat "getAuths")]])))))


(defn/a get-auths [_ ^bot.types.InlineQuery query]
    (setv auths (await (user.GetAuthorizations))
        answers [] )
    (for [auth auths.authorizations] (if (!= auth.hash 0) (.append answers (user.types.InlineQueryResultArticle
        :title f"{auth.app_name}({auth.app_version}){(if auth.official_app \"⭐\" \"\")}"
        :description f"{auth.device_model} || {auth.country} {auth.ip}"
        :input_message_content (user.types.InputTextMessageContent f"/sessions {auth.hash}")))))
    (return (await (query.answer answers :cache_time 0))))


(defn/a logout-handler [_ ^bot.types.CallbackQuery query]
    (await (user.ResetAuthorization :hash (int (get (query.data.split "_") 1))))
    (await (query.message.delete))
    (return (await (query.answer "Session has been Desctroyed!" :show_alert True))))


(bot.add_handler
    :handler (bot.handlers.MessageHandler
    :callback session-manager
    :filters (& (| (bot.filters.user bot.sudo) (bot.filters.user user.me.id)) (bot.filters.command "sessions" :prefixes "/"))))

(bot.add_handler
    :handler (bot.handlers.InlineQueryHandler
    :callback get-auths
    :filters (& (bot.filters.user user.me.id) (bot.filters.regex "^getAuths"))))

(bot.add_handler
    :handler (bot.handlers.CallbackQueryHandler
    :callback logout-handler
    :filters (& (| (bot.filters.user bot.sudo) (bot.filters.user user.me.id)) (bot.filters.regex "logout_"))))
