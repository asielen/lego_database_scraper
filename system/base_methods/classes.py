__author__ = 'andrew.sielen'

import arrow

from system.logger import logger


class process_timer():
    def __init__(self):
        self.start_time = arrow.now()
        self.tasks = 0

    def _get_run_time(self):
        time_diff = arrow.now() - self.start_time
        return time_diff.seconds

    def _update_tasks(self, num_of_tasks):
        self.tasks += num_of_tasks

    def log_time(self, num_of_tasks, remaining_tasks=None):
        time_diff = self._get_run_time()
        self._update_tasks(num_of_tasks)
        logger.info("Run Time: {} seconds / {} processed".format(time_diff, self.tasks))
        tasks_per_second = self.tasks / time_diff
        logger.info("Run Time: {} per second".format(round(tasks_per_second)))
        tasks_per_min = 60 * tasks_per_second
        logger.info("Run Time: {} per min".format(round(tasks_per_min)))
        if remaining_tasks is not None:
            logger.info(
                "Run Time: Est Time Remaining {} mins for {} objects".format(round(remaining_tasks / tasks_per_min),
                                                                             remaining_tasks))
