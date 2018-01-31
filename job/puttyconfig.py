import subprocess

from job.basejob import BaseJob


class Job(BaseJob):
    def execute(self, context):
        self._export_registry_key("PuttyConfig", "HKEY_CURRENT_USER\Software\SimonTatham")

    def _get_cygpath_windows(self, path):
        args = ["cygpath", "--windows", path]
        return subprocess.check_output(args).split()[0]

    def _export_registry_key(self, name, key):
        output_filename = "{}/{}.reg".format(self.output_folder, name)
        windows_output_filename = self._get_cygpath_windows(output_filename)
        args = ["regedit", "/e", windows_output_filename, key]
        returncode = subprocess.call(args)
        if returncode:
            raise RuntimeError("unexpected return code: {}".format(returncode))
