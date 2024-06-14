from datetime import datetime
from app.service.scheduler.schedulable import get_next_run_time
from app.storage.sqlite.sql.dml import delete, insert
from app.platform.platform import Scheduler
from app.service.scheduler.model import ExecutionHistory, ScheduledJob
from app.utils.datetime import timestamp

def get_scheduled_jobs():
    return ScheduledJob.select_all()

def get_execution_history():
    return ExecutionHistory.select_all_with_scheduled_job()

def create_scheduled_job(task_name, module_name, scheduled_class_name, frequency, start_at):
    start_at_datetime = get_datetime_from_time_string(start_at)
    job_id = insert(ScheduledJob({
        "name":task_name,
        "scheduled_module_name":module_name,
        "scheduled_class_name":scheduled_class_name,
        "frequency":frequency,
        "start_time":timestamp(start_at_datetime),
        "next_run_time":get_next_run_time(frequency,start_at_datetime)
    }))
    
    arguments = ["run_scheduled", job_id, module_name, scheduled_class_name]
    result = Scheduler.new_scheduled_task(task_name,arguments,frequency,start_at)

    if result:
        return result
    else:
        delete(ScheduledJob({"id":job_id}))

def delete_scheduled_job(job_id):
    job = ScheduledJob.select_by_id(job_id)
    delete_status = Scheduler.delete_scheduled_task(job.get('name'))

    if delete_status:
        delete(ScheduledJob({"id":job_id}))

def get_datetime_from_time_string(time_string):
    current_date = datetime.now().date()
    hours, minutes = map(int, time_string.split(':'))
    return datetime(current_date.year, current_date.month, current_date.day, hours, minutes)