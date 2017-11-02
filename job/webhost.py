import logging
import re
from fabric.api import env
from fabric.operations import run, get

from job.basejob import BaseJob


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Job(BaseJob):
    def __str__(self):
        return "{}[{}]".format(BaseJob.__str__(self), self._get_user_at_host_configuration())

    def execute(self):
        env.host_string = self._get_user_at_host_configuration()
        backup_file_name = "backup.tar.gz"
        log.info("creating backup file remotely for: {}".format(self._get_user_at_host_configuration()))
        run(self._get_create_backup_file_command(backup_file_name), shell=False)
        log.info("downloading backup file: {}".format(self._get_user_at_host_configuration()))
        get(backup_file_name, self._get_output_file_name("WebHost"))

    def _get_user_at_host_configuration(self):
        return self.configuration["user_at_host"]

    def _get_create_backup_file_command(self, backup_file_name):
        list_source_files = "ls -A | grep -Ev \"^($BACKUP_FILE|logs|Maildir|.+\.log)$\""
        ignore_failed_read = "--ignore-failed-read" if self.configuration.get("ignore_failed_read", False) else ""
        create_backup_file = "BACKUP_FILE_NAME={} ; " \
                             "rm -f $BACKUP_FILE_NAME ; " \
                             "tar {} -zcf $BACKUP_FILE_NAME $({})".format(backup_file_name, ignore_failed_read,
                                                                          list_source_files)
        return create_backup_file

    def _get_output_file_name(self, job_type):
        user_at_host = self._get_user_at_host_configuration()
        name = re.sub("^.*@", "", user_at_host)
        output_filename = "{}/{}-{}.tar.gz".format(self.output_folder, job_type, name)
        return output_filename

    def _validate_configuration(self, configuration):
        pass
