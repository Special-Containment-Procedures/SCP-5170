import importlib
from scp.plugins import loadModule
import logging

logging.getLogger(__name__)

HELP_COMMANDS = {}


async def loadPlugins(pluginDir: str = list):
    if isinstance(pluginDir, str):
        modules = loadModule(pluginDir)
        for mod in modules:
            imported_module = importlib.import_module(
                f'scp.plugins.{pluginDir}.{mod}',
            )
            if hasattr(
                imported_module,
                '__PLUGIN__',
            ) and imported_module.__PLUGIN__:
                imported_module.__PLUGIN__ = imported_module.__PLUGIN__
            if hasattr(
                imported_module,
                '__PLUGIN__',
            ) and imported_module.__PLUGIN__:
                if imported_module.__PLUGIN__.lower() not in HELP_COMMANDS:
                    HELP_COMMANDS[
                        imported_module.__PLUGIN__.lower()
                    ] = imported_module
                else:
                    raise ValueError(
                        "Can't have two modules with the same name!",
                    )
            if hasattr(imported_module, '__DOC__') and imported_module.__DOC__:
                HELP_COMMANDS[
                    imported_module.__PLUGIN__.lower()
                ] = imported_module
        return logging.info(f'imported {len(modules)} {pluginDir} modules')
    for plugin in pluginDir:
        modules = loadModule(plugin)
        for mod in modules:
            imported_module = importlib.import_module(
                f'scp.plugins.{plugin}.{mod}',
            )
            if hasattr(
                imported_module,
                '__PLUGIN__',
            ) and imported_module.__PLUGIN__:
                imported_module.__PLUGIN__ = imported_module.__PLUGIN__
            if hasattr(
                imported_module,
                '__PLUGIN__',
            ) and imported_module.__PLUGIN__:
                if imported_module.__PLUGIN__.lower() not in HELP_COMMANDS:
                    HELP_COMMANDS[
                        imported_module.__PLUGIN__.lower()
                    ] = imported_module
                else:
                    raise ValueError(
                        "Can't have two modules with the same name!",
                    )
            if hasattr(imported_module, '__DOC__') and imported_module.__DOC__:
                HELP_COMMANDS[
                    imported_module.__PLUGIN__.lower()
                ] = imported_module
        logging.info(f'imported {len(modules)} {plugin} modules')
