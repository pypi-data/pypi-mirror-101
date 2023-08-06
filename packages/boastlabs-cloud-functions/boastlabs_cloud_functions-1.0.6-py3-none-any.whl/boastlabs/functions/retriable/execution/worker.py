from abc import abstractmethod
import random
import time

from boastlabs.functions.retriable.execution.exceptions import RetryException, SleepException
from boastlabs.functions.retriable.execution.threading import TimedThread
from boastlabs.functions.retriable.execution.state import State
from boastlabs.functions.retriable.execution.time import Timer
from boastlabs.functions.retriable.execution.config import Status


class Worker(TimedThread):

    def __init__(self, timer: Timer, event_id: str, state: State):
        TimedThread.__init__(self, timer=timer, event_id=event_id, name=self.__class__.__name__)

        self.state = state

    def get_sleep_duration(self):
        raise 0

    @abstractmethod
    def work(self):
        raise NotImplementedError

    def run(self):
        self.state.set_created_at()
        self.state.set_modified_at()

        if self.state.status == Status.SLEEP:
            self.state.set_status(Status.SLEEP)

            duration = self.get_sleep_duration()

            # Wait duration / can be interrupted by timeout

            self.logger.debug(f"# SLEEP START {duration}")
            self.timer.timeout_event.wait(duration)
            self.logger.debug(f"# SLEEP END")

            # Move to WAITING_RETRY state and resume execution on next call

            self.state.set_status(Status.WAITING_RETRY)

        if self.state.status == Status.RUNNING:
            self.logger.debug(f"# RUNNING")
            try:
                self.state.set_status(Status.RUNNING)
                self.work()
                self.state.set_status(Status.DONE)
            except RetryException:
                self.state.set_status(Status.WAITING_RETRY)
            except SleepException:
                self.state.set_status(Status.WAITING_SLEEP)
            except Exception as e:
                self.state.set_status(Status.FAILED, error=e)
                raise e


class TestWorker(Worker):

    def work(self):
        sleep = random.randint(0, 15)
        self.logger.debug(f"Sleep {sleep}")
        time.sleep(sleep)

        # if (random.randint(0, 9) == 1):
        #     raise Exception('Ingester Kind #1 exception')
        # if (random.randint(0, 9) == 2):
        #     raise Exception('Ingester Kind #2 exception')
