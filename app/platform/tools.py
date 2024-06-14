from abc import ABC, abstractmethod
import os

from app.utils.common import get_python_executable_path
from app.utils.path import get_project_root_dir

class SchedulerABC(ABC):
    task_name_prefix = 'UpWebTools '
    python_executable_path = get_python_executable_path()
    entrypoint_script_path = os.path.join(get_project_root_dir(),'start.py')
    
    @abstractmethod
    def get_scheduled_tasks(self):
        pass

    @abstractmethod
    def new_scheduled_task(self, task_name, arguments, frequency, start_at):
        pass

    @abstractmethod
    def delete_scheduled_task(self, task_name):
        pass