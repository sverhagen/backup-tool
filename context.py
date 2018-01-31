import os
import platform
from enum import Enum


class Context:
    class Environments(Enum):
        CYGWIN = 1
        LINUX = 2
        WINDOWS = 3

    def __init__(self):
        self.environments = self._determine_environments()
        self.home_folder = self._determine_home_folder()

    def assert_cygwin(self, subject):
        if not Context.Environments.CYGWIN in self.environments:
            raise EnvironmentError("cannot run {} other than on Cygwin".format(subject))

    def assert_windows(self, subject):
        if not Context.Environments.WINDOWS in self.environments:
            raise EnvironmentError("cannot run {} other than on Windows".format(subject))

    def is_windows(self):
        return Context.Environments.CYGWIN in self.environments or Context.Environments.WINDOWS in self.environments

    def _determine_home_folder(self):
        if Context.Environments.WINDOWS in self.environments:
            home_folder = os.environ["USERPROFILE"]
        else:
            home_folder = os.environ["HOME"]

        return home_folder

    def _determine_environments(self):
        environments = []
        if platform.system() == "Linux":
            environments.append(Context.Environments.LINUX)
        elif platform.system().startswith("CYGWIN"):
            environments.append(Context.Environments.CYGWIN)
            environments.append(Context.Environments.WINDOWS)
        else:
            environments.append(Context.Environments.WINDOWS)

        return environments
