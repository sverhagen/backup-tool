import os

from git import Repo

from job.basejob import BaseJob


class Job(BaseJob):
    TARGET_FOLDER = "BackupToolConfig"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = Repo(".")

    def execute(self, context):
        current_folder = os.getcwd()
        self._copy_files(Job.TARGET_FOLDER, current_folder, "*.yaml")
        self._write_git_information()

    def _write_git_information(self):
        target_folder = "{}/{}".format(self.output_folder, Job.TARGET_FOLDER)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        file_name = "{}/git.txt".format(target_folder)
        with open(file_name, "w") as text_file:
            print("branch", self._get_branch(), file=text_file)
            print("ref", self._get_ref(True), file=text_file)
            print("local_changes", self._has_local_changes(), file=text_file)

    def _get_branch(self):
        return self.repo.head.ref

    def _get_local_changes(self):
        diffs = self.repo.index.diff(None)
        diffs.extend(self.repo.index.diff(None, staged=True))

        return diffs

    def _get_ref(self, short):
        return self.repo.git.rev_parse(self.repo.head, short=short)

    def _has_local_changes(self):
        return len(self._get_local_changes()) > 0
