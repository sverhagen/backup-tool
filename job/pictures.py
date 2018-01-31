import os
from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self, context):
        pictures_location = "{}/Pictures".format(context.home_folder)
        self._package_folder("Pictures", pictures_location)

