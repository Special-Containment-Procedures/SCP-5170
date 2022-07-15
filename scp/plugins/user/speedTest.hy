(import [scp[user]])
(import [scp.utils.SpeedTest[Speedtest]])


(setv __PLUGIN__ "speedtest"
    __DOC__ (str
        (user.md.KanTeXDocument
            (user.md.Section "Test speed on speedtest.net"
                (user.md.SubSection "speedTest" (user.md.Code "(*prefix)speedTest"))))))


(defn/a speed-test-handler [_ ^user.types.Message message]
    (setv reply (await (message.reply "`SpeedTest ...`" :quote True))
        ^Speedtest s (await (Speedtest)))
    (await (s.get_best_server))
    (await (s.download))
    (await (s.upload))
    (setv text (user.md.KanTeXDocument 
        (user.md.Section
            "speedTest"
            (user.md.SubSection
                "Ping:"
                (user.md.Code (+ (str s.results.ping) "ms")))
            (user.md.SubSection
                "Download:"
                (user.md.Code (+ (str (round (/ s.results.download 1000.0 1000.0) 2)) "Mbit/s")))
            (user.md.SubSection
                "Upload:"
                (user.md.Code (+ (str (round (/ s.results.upload 1000.0 1000.0) 2)) "Mbit/s"))))))
    (return (await (reply.edit text))))


(user.add_handler
    :handler (user.handlers.MessageHandler
    :callback speed-test-handler
    :filters (& (| (user.filters.user user.sudo) (user.filters.user user.me.id)) (user.filters.command "speedtest"))))