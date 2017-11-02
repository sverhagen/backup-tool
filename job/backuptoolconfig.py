import os
from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self):
        current_folder = os.getcwd()
        self._copy_files("BackupToolConfig", current_folder, "*.yaml")
