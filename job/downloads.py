import os
from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self):
        downloads_location = "{}/Downloads".format(os.environ["USERPROFILE"])
        self._package_folder("Downloads", downloads_location)
