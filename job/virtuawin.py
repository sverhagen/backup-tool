import os
from basejob import BaseJob

class Job(BaseJob):
    def execute(self):
        modules_folder = "/cygdrive/c/Program Files (x86)/VirtuaWin/modules"
        configuration_folder = "{}/VirtuaWin".format(os.environ["APPDATA"])
        self._copy_folder("VirtuaWin/modules", modules_folder)
        self._copy_folder("VirtuaWin/AppData", configuration_folder)
