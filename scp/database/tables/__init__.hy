(import configparser)
(import [scp[user]])


(defn/a checkTable [^str name]
    (if (int (user._config.get "pyrogram" "test_mode"))
        (setv db "databaseChannel-test")
        (setv db "databaseChannel"))
    (try
        (setv tableID (user._config.getint ".internal" name))
        (except [configparser.NoOptionError]
            (setv table (await (user.send_message
                            :chat_id (user._config.getint ".internal" db)
                            :text "{}")))
            (user._config.set ".internal" name (str table.id))
            (with [file (open "config.ini" "w")]
                (user._config.write file))
            (setv tableID table.id)))
        (return tableID))
