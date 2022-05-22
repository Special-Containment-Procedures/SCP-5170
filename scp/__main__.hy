(import asyncio)
(require sys)
(import [scp[user bot loop idle]])
(import [scp.core.functions.plugins[loadPlugins]])
(import [scp.database.Operational[InitializeDatabase]])


(defn/a main []
    (await (bot.start))
    (await (user.start))
    (await (InitializeDatabase))
    (await (loadPlugins(.split(user._config.get "scp-5170" "plugins"))))
    (await (idle.idle))
)


(if (= __name__ "__main__")
    (loop.run_until_complete (main)))
