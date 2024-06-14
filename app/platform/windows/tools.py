from app.platform.tools import SchedulerABC
from app.platform.windows.task_scheduler import delete_scheduled_task, get_scheduled_tasks, new_scheduled_task
from app.utils.logger import logger

class WindowsScheduler(SchedulerABC):
    def get_scheduled_tasks(self):
        return get_scheduled_tasks(self.task_name_prefix)

    def new_scheduled_task(self, task_name, arguments, frequency, start_at):
        task_name = self.task_name_prefix + task_name
        argument = ' '.join([self.entrypoint_script_path] + [str(a) for a in arguments])

        trigger_arguments = ''
        if frequency == 'daily':
            trigger_arguments = f'-Daily -At "{start_at}"'
        elif frequency == 'hourly':
            trigger_arguments = f'-Once -At "{start_at}" -RepetitionInterval ([System.TimeSpan]::FromHours(1))'
        else:
            logger.info(f'Frequency of {frequency} is not supported yet')
            return False
    
        return new_scheduled_task(task_name, self.python_executable_path, argument, trigger_arguments, start_at)

    def delete_scheduled_task(self, task_name):
        task_name = self.task_name_prefix + task_name
        return delete_scheduled_task(task_name)