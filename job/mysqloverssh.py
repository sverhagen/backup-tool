import logging
import re
from fabric.api import env
from fabric.operations import run, get

from job.basejob import BaseJob


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Job(BaseJob):
    def __str__(self):
        return "{}[{}]".format(BaseJob.__str__(self), self.configuration["database"]["host"])

    def is_name(self, name):
        return BaseJob.is_name(self, name) \
               or name == "{}[{}]".format(self.__module__, self.configuration["database"]["host"])

    def execute(self):
        env.host_string = self._get_user_at_host_configuration()
        backup_file_name = "backup.mysql.gz"
        log.info("creating MySQL backup file remotely for: {}".format(self._get_user_at_host_configuration()))
        run(self._get_create_backup_file_command(backup_file_name), shell=False)
        log.info("downloading MySQL backup file: {}".format(self._get_user_at_host_configuration()))
        get(backup_file_name, self._get_output_file_name("MySql"))

    def _get_user_at_host_configuration(self):
        return self.configuration["user_at_host"]

    def _get_create_backup_file_command(self, backup_file_name):
        database_configuration = self.configuration["database"]
        host = database_configuration["host"]
        instance = database_configuration["instance"]
        password = database_configuration["password"]
        user_name = database_configuration["user_name"]

        return "mysqldump -h {} -u {} -p\"{}\" {} | gzip > {}".format(host, user_name, password, instance, backup_file_name)

    def _get_output_file_name(self, job_type):
        host = self.configuration["database"]["host"]
        name = re.sub("\.", "_", host)
        output_filename = "{}/{}-{}.gz".format(self.output_folder, job_type, name)
        return output_filename
