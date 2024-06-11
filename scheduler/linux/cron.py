from logging import getLogger
import subprocess

logger = getLogger()

def new_cron_job(task_name, cron_expression, command_and_arguments):
    existing_crontab = get_existing_crontab()
    new_job = f"{cron_expression} {command_and_arguments} {task_name}"
    new_crontab_content = existing_crontab + '\n' + new_job + '\n'
    write_to_crontab(new_crontab_content)


def get_existing_crontab():
    existing_crontab = ""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        existing_crontab = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(e)
    return existing_crontab

def delete_cron_job(task_name):
    existing_crontab = get_existing_crontab()
    crontab_lines = existing_crontab.splitlines()
    filtered_lines = [line for line in crontab_lines if task_name not in line]
    new_crontab_content = '\n'.join(filtered_lines) + '\n'
    write_to_crontab(new_crontab_content)

def write_to_crontab(new_crontab_content):
    try:
        subprocess.run(["crontab", "-"], input=new_crontab_content, text=True, check=True)
        logger.info("Crontab updated successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error updating crontab: {e}")
        return False