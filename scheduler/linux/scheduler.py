from scheduler.abc import SchedulerABC
from scheduler.linux.cron import delete_cron_job, new_cron_job


class LinuxScheduler(SchedulerABC):
    def get_scheduled_tasks(self):
        pass

    def new_scheduled_task(self, task_name, arguments, frequency, start_at):
        task_name = self.task_name_prefix + task_name
        command_and_arguments = ' '.join([self.python_executable_path,self.entrypoint_script_path] + [str(a) for a in arguments])
        cron_expression = ''
        start_at_parts = start_at.split(':')
        start_at_minute = start_at_parts[1]
        start_at_hour = start_at_parts[0] if frequency == 'daily' else None

        if frequency == 'daily':
            cron_expression = f'{start_at_minute} {start_at_hour} * * *'
        elif frequency == 'hourly':
            cron_expression = f'{start_at_minute} * * * *'
        
        return new_cron_job(task_name, cron_expression, command_and_arguments)

    def delete_scheduled_task(self, task_name):
        return delete_cron_job(task_name)