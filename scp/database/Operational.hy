(import configparser)
(import [scp [user]])


(defn/a InitializeDatabase[]
    (try
        (if (int (user._config.get "pyrogram" "test_mode"))
            (setv db "databaseChannel-Test")
            (setv db "databaseChannel"))
        (user._config.getint ".internal" db)
        (except [configparser.NoSectionError]
            (with [file (open "config.ini" "w")]
                (user._config.add_section ".internal")
                (user._config.write file)))
            (except [configparser.NoOptionError]
                (setv channel
                    (await (user.create_channel "scp-Database"
                            :description "Do not Play with this channel!")))
                (user._config.set
                    ".internal" db (str channel.id))))
        (with [file (open "config.ini" "w")]
                (user._config.write file)))
