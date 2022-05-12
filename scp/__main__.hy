(import asyncio)
(require sys)
(import [pyrogram[idle]])
(import [scp[user bot loop]])
(import [scp.core.functions.plugins[loadPlugins]])
(import [scp.utils.selfInfo[updateInfo]])
(import [scp.database.Operational[InitializeDatabase]])

(defn/a main []
    (await (bot.start))
    (await (user.start))
    (await (updateInfo))
    (await (InitializeDatabase))
    (await (loadPlugins(.split(user._config.get "scp-5170" "plugins"))))
    (await (idle))
)


(if (= __name__ "__main__")
    (try
        (loop.run_until_complete (main))
        (except [KeyboardInterrupt]
            (sys.exit 1))))
