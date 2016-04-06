from job.basejob import BaseJob

class Job(BaseJob):
    def execute(self):
        cygwin_home_location = "/cygdrive/c/cygwin64/home"
        self._package_folder("CygwinHome", cygwin_home_location)
