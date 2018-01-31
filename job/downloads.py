import os
from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self, context):
        downloads_location = "{}/Downloads".format(context.home_folder)
        self._package_folder("Downloads", downloads_location)
