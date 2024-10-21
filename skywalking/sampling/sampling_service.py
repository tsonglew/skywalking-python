import time
from threading import Lock, Thread

from skywalking import config, profile
from skywalking.log import logger
from skywalking.trace import context
from skywalking.trace.context import NoopContext, SpanContext, _spans
from skywalking.utils.time import current_milli_time


class SamplingService(Thread):

    def __init__(self):
        super().__init__(name="samplingService", daemon=True)
        logger.debug("Started sampling service sampling_n_per_3_secs: %d",
                     config.sample_n_per_3_secs)
        self.on = config.sample_n_per_3_secs > 0
        self.lock = Lock()
        self.sampling_factor = 0

    def run(self):
        if not self.on:
            logger.debug("Sampling service is off")
            return

        while True:
            time.sleep(3)

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
            logger.debug("Reset sampling factor")
            self.sampling_factor = 0


sampling_service = SamplingService()
sampling_service.start()
