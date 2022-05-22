(import configparser)
(import [scp [user]])


(defn/a InitializeDatabase[]
    (try
        (if (int (user.config.get "pyrogram" "test_mode"))
            (setv db "databaseChannel-Test")
            (setv db "databaseChannel"))
        (user.config.getint ".internal" db)
        (except [configparser.NoSectionError]
            (with [file (open "config.ini" "w")]
                (user.config.add_section ".internal")
                (user.config.write file)))
            (except [configparser.NoOptionError]
                (setv channel
                    (await (user.create_channel "scp-Database"
                            :description "Do not Play with this channel!")))
                (user.config.set
                    ".internal" db (str channel.id))))
        (with [file (open "config.ini" "w")]
                (user.config.write file)))
