__author__ = 'andrew.sielen'

import arrow

from system.logger import logger


class process_timer():
    def __init__(self, name=""):
        logger.info("Timer {} Started".format(name))
        self.name = name
        self.start_time = arrow.now()
        self.tasks = 0

    def _get_run_time(self):
        time_diff = arrow.now() - self.start_time
        return time_diff.seconds

    def _update_tasks(self, num_of_tasks):
        self.tasks += num_of_tasks

    @property
    def tasks_completed(self):
        return self.tasks

    def end(self):
        time_diff = self._get_run_time()
        logger.info("@ Run Time: {} seconds".format(time_diff))
        logger.info("Timer {} Ended".format(self.name))
        del self

    def log_time(self, num_of_tasks, remaining_tasks=None):  # num_of_tasks is number of last completed tasks
        time_diff = self._get_run_time()
        self._update_tasks(num_of_tasks)
        logger.info("@ Process Time: {} seconds FOR {} objects processed".format(time_diff, self.tasks))
        tasks_per_second = self.tasks / max(1, time_diff)
        logger.info(
            "@@ Process Time: {} per min IS {} objects per second".format(round(60 * tasks_per_second),
                                                                          round(tasks_per_second)))
        if remaining_tasks is not None:
            logger.info(
                "@@ Process Time: ETR: {} mins FOR {} objects".format(round(remaining_tasks / (60 * tasks_per_second)),
                                                                      remaining_tasks))