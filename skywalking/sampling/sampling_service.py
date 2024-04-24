import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Thread, Timer
from typing import Any

from skywalking import config
from skywalking.agent import agent
from skywalking.loggings import logger
from skywalking.utils.time import current_milli_time


class SamplingService(Thread):

    def __init__(self):
        super().__init__(name='samplingService', daemon=True)
        logger.debug(f'Started sampling service, {config.sample_n_per_3_secs}')
        self.on = config.sample_n_per_3_secs > 0
        self.lock = Lock()
        self.sampling_factor = 0

    def run(self):
        while True:
            time.sleep(3)
            if not self.on:
                continue
            self.reset_sampling_factor()

    def try_sampling(self) -> bool:
        if not self.on:
            return True
        with self.lock:
            if self.sampling_factor < config.sample_n_per_3_secs:
                self.sampling_factor += 1
                return True
            return False

    def force_sampled(self) -> None:
        with self.lock:
            self.sampling_factor += 1

    def reset_sampling_factor(self) -> None:
        with self.lock:
            self.sampling_factor = 0
