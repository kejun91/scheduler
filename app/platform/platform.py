import platform
from app.platform.linux.tools import LinuxScheduler
from app.platform.macos.tools import MacOSScheduler
from app.platform.tools import SchedulerABC
from app.platform.windows.tools import WindowsScheduler
from app.utils.logger import logger

system_platform = platform.system()

Scheduler:SchedulerABC = None

if system_platform == 'Windows':
    Scheduler = WindowsScheduler()
elif system_platform == 'Darwin':
    Scheduler = MacOSScheduler()
elif system_platform == 'Linux':
    Scheduler = LinuxScheduler()
else:
    logger.info('platform is not supported')