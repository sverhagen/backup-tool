import os

from context import Context
from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self, context):
        context.assert_windows(self)
        configuration_folder = "{}/FileZilla".format(os.environ["APPDATA"])
        self._copy_files("FileZillaConfig", configuration_folder, "*.xml")
