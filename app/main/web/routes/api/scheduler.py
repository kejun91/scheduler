from app.main.web.decorator import api
from app.service.scheduler.manage import create_scheduled_job as create_schd_job, delete_scheduled_job as del_schd_job, get_execution_history, get_scheduled_jobs as get_schd_jobs
from app.service.scheduler.schedulable import get_schedulable_classes as get_schd_cls

@api('/api/scheduler/jobs','GET')
def get_scheduled_jobs(request):
    return get_schd_jobs()

@api('/api/scheduler/schedulable-classes','GET')
def get_schedulable_classes2(request):
    return get_schd_cls()

@api('/api/scheduler/job','POST')
def create_scheduled_job2(request):
    task_name = request.body.get('taskName')
    module_name = request.body.get('moduleName')
    class_name = request.body.get('className')
    execution_frequency = request.body.get('executionFrequency')
    execution_start_time = request.body.get('executionStartTime')
    
    return create_schd_job(task_name, module_name, class_name, execution_frequency, execution_start_time)

@api('/api/scheduler/delete-job','POST')
def delete_scheduled_job(request):
    job_id = request.body.get('jobId')
    return del_schd_job(job_id)

@api('/api/scheduler/execution-history','GET')
def get_execution_history2(request):
    histories = get_execution_history()
    return histories