from basejob import BaseJob

class Job(BaseJob):
    def execute(self):
        self._export_registry_key("PuttyConfig", "HKEY_CURRENT_USER\Software\SimonTatham")
