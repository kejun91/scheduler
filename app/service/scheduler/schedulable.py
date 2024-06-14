from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from app.utils.common import find_classes_inheriting_from, find_classes_inheriting_from_in_root_dir
from app.utils.datetime import timestamp


class Schedulable(ABC):
    @abstractmethod
    def execute(self):
        pass

def get_schedulable_classes():
    return [
        {
            'module':c.__module__,
            'name':c.__name__
        } 
        for c in find_classes_inheriting_from(Schedulable) + find_classes_inheriting_from_in_root_dir(Schedulable)
    ]

def get_next_run_time(frequency, start_time):
    current_time = datetime.now()
    if current_time < start_time:
        return start_time
    else:
        step_duration_in_minutes = 1
        if frequency == 'hourly':
            step_duration_in_minutes = 60
        elif frequency == 'daily':
            step_duration_in_minutes = 1440
        next_run_time = start_time
        while next_run_time < current_time:
            next_run_time = next_run_time + timedelta(minutes=step_duration_in_minutes)

        return timestamp(next_run_time)