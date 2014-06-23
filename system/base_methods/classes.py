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
        logger.info("@ Process Timer Report")
        logger.info("@ Process Time: {} seconds FOR {} processed".format(time_diff, self.tasks))
        tasks_per_second = self.tasks / max(1, time_diff)
        logger.info(
            "@ Process Time: {} per min IS {} per second".format(60 * tasks_per_second, round(tasks_per_second)))
        if remaining_tasks is not None:
            logger.info(
                "@ Process Time: ETR: {} mins FOR {} objects".format(round(remaining_tasks / (60 * tasks_per_second)),
                                                                             remaining_tasks))