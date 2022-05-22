import asyncio
import logging
import signal
from signal import signal as signal_fn, SIGINT, SIGTERM, SIGABRT

log = logging.getLogger(__name__)


signals = {
    k: v for v, k in signal.__dict__.items()
    if v.startswith('SIG') and not v.startswith('SIG_')
}


class Idle:
    def __init__(
        self,
        is_idling: bool = False,
    ):
        self.is_idling = is_idling

    def signal_handler(self, signum, __):
        logging.info(f'Stop signal received ({signals[signum]}). Exiting...')
        self.is_idling = False

    async def idle(self, stop: bool = False):
        for s in (SIGINT, SIGTERM, SIGABRT):
            signal_fn(s, self.signal_handler)
        self.is_idling = not stop
        while self.is_idling:
            await asyncio.sleep(1)
            if not self.is_idling:
                break
