import os
from app.platform.macos.launchd import delete_launchd_job, new_launchd_job
from app.platform.tools import SchedulerABC
from app.utils.path import get_project_root_dir

class MacOSScheduler(SchedulerABC):
    def get_scheduled_tasks(self):
        pass

    def new_scheduled_task(self, task_name, arguments, frequency, start_at):
        task_name = self.task_name_prefix + task_name
        program_arguments = [self.python_executable_path, self.entrypoint_script_path] + arguments
        scheduler_log_file_path = os.path.join(get_project_root_dir(),'logs','mac_scheduler.log')
        working_directory = get_project_root_dir()
        start_at_parts = start_at.split(':')
        start_minute = start_at_parts[1]
        start_hour = start_at_parts[0] if frequency == 'daily' else None

        return new_launchd_job(task_name, program_arguments, scheduler_log_file_path, working_directory, start_minute, start_hour)

    def delete_scheduled_task(self, task_name):
        task_name = self.task_name_prefix + task_name              
        return delete_launchd_job(task_name)