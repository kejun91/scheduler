import os
import subprocess


def generate_job_plist_content(label, program_arguments, scheduler_log_file_path, working_directory, start_minute, start_hour = None):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>{label}</string>
	<key>ProgramArguments</key>
	<array>
        {"{{ProgramArguments}}"}
	</array>
    <key>StandardErrorPath</key>
	<string>{scheduler_log_file_path}</string>
	<key>StandardOutPath</key>
	<string>{scheduler_log_file_path}</string>
	<key>WorkingDirectory</key>
	<string>{working_directory}</string>
	<key>StartCalendarInterval</key>
    <dict>{"{{Hour}}"}
        <key>Minute</key>
        <integer>{start_minute}</integer>
    </dict>
</dict>
</plist>'''.replace('{{Hour}}',('\n\t\t<key>Hour</key>\n\t\t<integer>' + start_hour + '</integer>') if start_hour is not None else '').replace('{{ProgramArguments}}','<string>' + '</string>\n\t\t<string>'.join([str(a) for a in program_arguments]) + '</string>')

def load_job(job_plist_file_path):
    subprocess.run(["launchctl", "load", job_plist_file_path], check=True)

def new_launchd_job(task_name, program_arguments, scheduler_log_file_path, working_directory, start_minute, start_hour = None):
    job_plist_content = generate_job_plist_content(task_name, program_arguments, scheduler_log_file_path, working_directory, start_minute, start_hour)
    job_plist_file_path = get_job_plist_file_path(task_name)
    with open(job_plist_file_path, 'w') as pf:
        pf.write(job_plist_content)

    load_job(job_plist_file_path)

    return True

def get_job_plist_file_path(task_name):
    launch_agents_user_directory = os.path.join(os.path.expanduser('~'), 'Library', 'LaunchAgents')
    return os.path.join(launch_agents_user_directory, task_name.replace(' ','.') + '.plist')

def delete_launchd_job(task_name):
    job_plist_file_path = get_job_plist_file_path(task_name)
    os.remove(job_plist_file_path)

    return True