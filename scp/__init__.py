import logging
import sys
import time
from .core.clients import Bot, User
from rich.logging import RichHandler
from pyromod import listen  # noqa
from scp.utils.gitTools import getVersion


RUNTIME = time.time()

__longVersion__, __version__ = getVersion()

if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    logging.error('Python version Lower than 3.8! Abort!')
    sys.exit()


LOG_FORMAT = (
    '%(filename)s:%(lineno)s %(levelname)s: %(message)s'
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt='%m-%d %H:%M',
    handlers=[RichHandler()],
)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

log = logging.getLogger()

bot = Bot()
user = User()
