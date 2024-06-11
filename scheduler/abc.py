from abc import ABC, abstractmethod

class SchedulerABC(ABC):
    task_name_prefix = 'LocalScheduler '
    
    @abstractmethod
    def get_scheduled_tasks(self):
        pass

    @abstractmethod
    def new_scheduled_task(self, task_name, arguments, frequency, start_at):
        pass

    @abstractmethod
    def delete_scheduled_task(self, task_name):
        pass