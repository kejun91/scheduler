import json
import subprocess
from app.utils.logger import logger


def get_scheduled_tasks(task_name_prefix):
    get_scheduled_tasks_script = r'''
        $scheduledTasks = Get-ScheduledTask | Where-Object { $_.TaskName -like '{{task_name_prefix}}*' }

        $tasksInfo = @()
        foreach ($task in $scheduledTasks) {
            # assuming there is only one action and one trigger for each scheduled task
            $taskInfo = @{
                "TaskName" = $task.TaskName
                "Actions.Execute" = $task.Actions.Execute
                "Actions.Arguments" = $task.Actions.Arguments
                "Triggers.Enabled" = $task.Triggers.Enabled
                "Triggers.StartBoundary" = $task.Triggers.StartBoundary
                "Triggers.Repetition.Interval" = $task.Triggers.Repetition.Interval
            }
            $tasksInfo += $taskInfo
        }

        $tasksInfo | ConvertTo-Json
    '''.replace("{{task_name_prefix}}",task_name_prefix or "")
    
    process = subprocess.Popen(["powershell.exe","-Command", get_scheduled_tasks_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate()
    
    if process.returncode == 0:
        output_list = json.loads(output) if output != '' else []
        if not isinstance(output_list,list):
            output_list = [output_list]
        return [ 
            {
                "name":task.get('TaskName'),
                "startDate":task.get('Triggers.StartBoundary'),
                "schedulablePythonClass":task.get('Actions.Arguments'),
                "frequency":'Hourly' if task.get("Triggers.Repetition.Interval") == 'PT1H' else 'Daily'
            } 
            for task in output_list
        ]
    else:
        return error

def new_scheduled_task(task_name, executable_path, argument, trigger_arguments, start_at):
    create_task_script = fr'''
        $action = New-ScheduledTaskAction -Execute "{executable_path}" -Argument "{argument}"
        $trigger = New-ScheduledTaskTrigger {trigger_arguments}
        Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "{task_name}"
    '''
    
    result = subprocess.run(["powershell.exe","-Command", create_task_script], capture_output=True, text=True)

    if result.returncode == 0:
        return {
            "executable":executable_path,
            "argument":argument,
            "frequency":"",
            "startAt":""
        }
    else:
        logger.info(result.returncode)
        logger.info(result.stdout)
        logger.info(result.stderr)
        return False
    
def delete_scheduled_task(task_name):
    delete_scheduled_task_script = fr'''
        Unregister-ScheduledTask -TaskName "{task_name}" -Confirm:$false
    '''
    result = subprocess.run(["powershell.exe","-Command", delete_scheduled_task_script], capture_output=True, text=True)
    
    if result.returncode == 0:
        return True
    else:
        logger.info(result.returncode)
        logger.info(result.stdout)
        logger.info(result.stderr)
        return False