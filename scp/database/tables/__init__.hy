(import configparser)
(import [scp[user]])


(defn/a checkTable [^str name]
    (if (int (user.config.get "pyrogram" "test_mode"))
        (setv db "databaseChannel-test")
        (setv db "databaseChannel"))
    (try
        (setv tableID (user.config.getint ".internal" name))
        (except [configparser.NoOptionError]
            (setv table (await (user.send_message
                            :chat_id (user.config.getint ".internal" db)
                            :text "{}")))
            (user.config.set ".internal" name (str table.id))
            (with [file (open "config.ini" "w")]
                (user.config.write file))
            (setv tableID table.id)))
        (return tableID))
