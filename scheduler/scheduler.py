from logging import getLogger
import platform

from scheduler.abc import SchedulerABC
from scheduler.linux.scheduler import LinuxScheduler
from scheduler.macos.scheduler import MacOSScheduler
from scheduler.windows.scheduler import WindowsScheduler


logger = getLogger()

Scheduler:SchedulerABC = None

system_platform = platform.system()
if system_platform == 'Windows':
    Scheduler = WindowsScheduler()
elif system_platform == 'Darwin':
    Scheduler = MacOSScheduler()
elif system_platform == 'Linux':
    Scheduler = LinuxScheduler()
else:
    logger.info(f'Platform {system_platform} is not supported')