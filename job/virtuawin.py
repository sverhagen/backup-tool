import os
from job.basejob import BaseJob


class Job(BaseJob):
    def execute(self, context):
        context.assert_windows(self)
        modules_folder = "/cygdrive/c/Program Files (x86)/VirtuaWin/modules"
        configuration_folder = "{}/VirtuaWin".format(os.environ["APPDATA"])
        self._copy_folder("VirtuaWin/modules", modules_folder)
        self._copy_folder("VirtuaWin/AppData", configuration_folder)
