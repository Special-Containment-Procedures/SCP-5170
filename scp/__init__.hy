(import logging)
(import hy) ; noqa
(import sys)
(import time)
(import asyncio)
(import [scp [core]])
(import [rich.logging [RichHandler]])
(import [pyromod [listen]])
(import [scp.utils.gitTools [getVersion]])
(import pathlib)

(setv RUNTIME (time.time)
    Versions (getVersion)
    loop (asyncio.get_event_loop)
    __longVersion__ (get Versions 0)
    __version__ (get Versions 1)
    console (logging.StreamHandler)
    fileLogger (logging.FileHandler "logs.txt" :encoding "utf-8")
    idle (core.functions.Idle))

(logging.basicConfig
    :level logging.INFO
    :format "%(filename)s:%(lineno)s %(levelname)s: %(message)s"
    :datefmt "%m-%d %H:%M"
    :handlers [(RichHandler)]
)
(console.setLevel logging.ERROR)
(fileLogger.setLevel logging.DEBUG)
(console.setFormatter
    (logging.Formatter "%(filename)s:%(lineno)s %(levelname)s: %(message)s"))
(fileLogger.setFormatter
    (logging.Formatter "%(filename)s:%(lineno)s %(levelname)s: %(message)s"))
(.addHandler (logging.getLogger "") console)
(.addHandler (logging.getLogger "") fileLogger)

(setv log (logging.getLogger)
    bot (core.clients.Client f"{(.parent.resolve (pathlib.Path __file__))}-bot")
    user (core.clients.Client f"{(.parent.resolve (pathlib.Path __file__))}-user"))
