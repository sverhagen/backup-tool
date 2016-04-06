import os
from basejob import BaseJob

class Job(BaseJob):
    def execute(self):
        desktop_location = "{}/Desktop".format(os.environ["USERPROFILE"])
        self._package_folder("Desktop", desktop_location)
