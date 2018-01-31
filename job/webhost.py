import logging
import os
import re

from fabric.api import env
from fabric.context_managers import settings
from fabric.operations import run, get

from job.basejob import BaseJob

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Job(BaseJob):
    def __str__(self):
        return "{}[{}]".format(BaseJob.__str__(self), self._get_user_at_host_configuration())

    def is_name(self, name):
        return BaseJob.is_name(self, name) \
               or name == "{}[{}]".format(self.__module__, self._get_user_at_host_configuration())

    def execute(self, context):
        env.host_string = self._get_user_at_host_configuration()
        backup_file_name = "backup.tar.gz"
        log.info("creating backup file remotely for: {}".format(self._get_user_at_host_configuration()))
        run_command = self._get_create_backup_file_command(backup_file_name)
        attribute_string = run(run_command, shell=False, warn_only=True)
        if attribute_string.return_code:
            raise Exception("failed with return code {} when running command: {}".format(
                attribute_string.return_code, run_command))

        log.info("downloading backup file: {}".format(self._get_user_at_host_configuration()))
        with settings(connection_attempts=5, keepalive=60):
            get("{}.*".format(backup_file_name), self._get_output_folder("WebHost"))

    def _get_user_at_host_configuration(self):
        return self.configuration["user_at_host"]

    def _get_create_backup_file_command(self, backup_file_name):
        list_source_files = "ls -A | grep -Ev \"^($BACKUP_FILE|logs|Maildir|.+\.log)$\""
        ignore_failed_read = "--ignore-failed-read" if self.configuration.get("ignore_failed_read", False) else ""
        excludes = " ".join(
            "--exclude={}".format(exclude) for exclude in self.configuration.get("exclude_patterns", "").split(","))
        if not backup_file_name:
            raise Exception("backup file name empty (this is an extra validation to prevent a remote \"rm *\"")
        create_backup_file = "BACKUP_FILE_NAME={} ; " \
                             "rm -f $BACKUP_FILE_NAME $BACKUP_FILE_NAME.* ; " \
                             "tar {} {} -zcf - $({}) | split --bytes=200MB - $BACKUP_FILE_NAME.".format(
            backup_file_name, ignore_failed_read, excludes, list_source_files)
        return create_backup_file

    def _get_output_folder(self, job_type):
        user_at_host = self._get_user_at_host_configuration()
        name = re.sub("^.*@", "", user_at_host)
        output_folder = "{}/{}-{}/".format(self.output_folder, job_type, name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        return output_folder

    def _validate_configuration(self, configuration):
        pass
