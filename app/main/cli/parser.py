from app.service.scheduler.execute import run_scheduled_tasks


def parse(argv, len):
    if len > 1:
        if argv[1] == 'run_scheduled':
            if len >= 5:
                job_id = argv[2]
                module_name = argv[3]
                scheduled_class_name = argv[4]
                print("Running",job_id, module_name,scheduled_class_name)
                run_scheduled_tasks(job_id, module_name, scheduled_class_name)