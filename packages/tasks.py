from huey import crontab
from huey.contrib.djhuey import periodic_task

from packages.services import PyPiPackagesProcessor


@periodic_task(crontab(minute="20", hour="13", day="*/1"))
def fetch_and_index_packages():
    proc = PyPiPackagesProcessor()
    proc.index_packages()
