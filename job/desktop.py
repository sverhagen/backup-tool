import os
from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self, context):
        desktop_location = "{}/Desktop".format(context.home_folder)
        self._package_folder("Desktop", desktop_location)
