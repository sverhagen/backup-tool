import os
from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self, context):
        documents_location = "{}/Documents".format(context.home_folder)
        self._package_folder("Documents", documents_location)
