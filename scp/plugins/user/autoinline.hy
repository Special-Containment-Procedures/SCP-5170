(import [scp[user bot]])


(defn/a auto-inline [_ ^bot.types.InlineQuery query]
    (setv task (get (query.query.split " ") 1))
    (return (await (query.answer [(.get user.cache task)] :cache_time 0))))


(bot.add_handler
    :handler (bot.handlers.InlineQueryHandler
    :callback auto-inline
    :filters (& (bot.filters.user user.me.id) (bot.filters.regex "^inline"))))
