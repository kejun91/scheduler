from datetime import datetime
import importlib
from app.service.scheduler.schedulable import get_next_run_time
from app.storage.sqlite.sql.dml import insert, update
from app.service.scheduler.model import ExecutionHistory, ScheduledJob
from app.storage.sqlite.table.column_enum import ID
from app.utils.common import get_exception_detail, import_module_from_path
from app.utils.datetime import timestamp


def run_scheduled_tasks(job_id, module_name, scheduled_class_name):
    job = ScheduledJob.select_by_id(job_id)
    history_id = update_execution_started(job)
    try:
        if not module_name.startswith('app'):
            module = import_module_from_path(module_name)
        else:
            module = importlib.import_module(module_name)
        scheduled_class = getattr(module, scheduled_class_name)
        scheduled_class().execute()
        update_execution_completed(history_id)
    except Exception as e:
        update_execution_failed(history_id, e)

def update_execution_started(job):
    current_timestamp = timestamp(datetime.now())
    history_id = insert(ExecutionHistory({
        "status":"Running",
        "run_start_time": current_timestamp,
        "scheduled_job_id": job.get(ID)
    }))

    update(ScheduledJob({
        ID:job.get(ID),
        "last_run_time": current_timestamp,
        "next_run_time": get_next_run_time(job.get('frequency'),datetime.fromtimestamp(int(job.get('start_time')/1000)))
    }))

    return history_id

def update_execution_completed(history_id):
    update(ExecutionHistory({
        ID:history_id,
        "status":"Completed",
        "run_end_time":timestamp(datetime.now())
    }))

def update_execution_failed(history_id, e: Exception):
    update(ExecutionHistory({
        ID:history_id,
        "status":"Failed",
        "run_end_time":timestamp(datetime.now()),
        "message":get_exception_detail(e)
    }))