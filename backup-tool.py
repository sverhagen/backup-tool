#!/usr/bin/env python

import click
import ctypes
import importlib
import logging
import os
import yaml
import shutil

logging.basicConfig(format="%(asctime)-15s %(levelname)s: %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class ElevationHelper:
    @staticmethod
    def assert_elevated():
        shell32 = ctypes.cdll.LoadLibrary("shell32.dll")

        if not shell32.IsUserAnAdmin():
            raise RuntimeError("elevation required (Run As Administrator)")


class BackupTool:
    def __init__(self, target_folder, staging_folder, leave_staging_folder):
        self.target_folder = target_folder
        self.staging_folder = staging_folder

        self._assert_target_folder()
        if not leave_staging_folder:
            self._assert_staging_folder()

        self._load_configuration()
        self._load_jobs()

    def backup(self, resume_from):
        ElevationHelper().assert_elevated()
        self._prepare_staging_folder()
        self._execute_jobs(resume_from)

    def copy_to_target_folder(self):
        log.info("copying from staging folder {} to target folder {}".format(self.staging_folder, self.target_folder))
        shutil.copytree(self.staging_folder, self.target_folder)

    def remove_staging_folder(self, leave_staging_folder):
        self._list_staging_folder()
        if not leave_staging_folder:
            log.info("removing staging folder: {}".format(self.staging_folder))
            shutil.rmtree(self.staging_folder)

    def _load_configuration(self):
        with open("backup-tool.yaml") as configuration_file:
            self.configuration = yaml.load(configuration_file.read())

    def _load_jobs(self):
        self.jobs = []
        configured_jobs = self.configuration["jobs"]
        for configured_job in configured_jobs:
            job_module = configured_job["module"]
            job_configuration = configured_job.get("configuration", None)
            try:
                job_class = getattr(importlib.import_module(job_module), "Job")
                job = job_class(job_configuration, self.staging_folder)
                self.jobs.append(job)
                log.info("loaded {}".format(job))
            except Exception as e:
                raise RuntimeError("cannot instantiate job class for module {}: {}".format(job_module, e))

    def _execute_jobs(self, resume_from):
        resume_from_index = next(index for index, job in enumerate(self.jobs) if job.is_name(resume_from)) if resume_from else 0
        selected_jobs = self.jobs[resume_from_index:]

        log.info("executing {} jobs: {}".format(len(selected_jobs), ", ".join([str(job) for job in selected_jobs])))
        for job in selected_jobs:
            log.info("executing {}".format(job))
            try:
                job.execute()
            except Exception as e:
                log.warning("problem executing job {}: {}".format(job, str(e)))
                raise

    def _prepare_staging_folder(self):
        if not os.path.exists(self.staging_folder):
            log.info("preparing staging folder: {}".format(self.staging_folder))
            os.makedirs(self.staging_folder)

    def _list_staging_folder(self):
        print()
        print("overview of backup results:")

        folders_with_size = {}
        for root, dirs, file_names in os.walk(self.staging_folder, topdown=False):
            size_files = sum(os.path.getsize(os.path.join(root, file_name)) for file_name in file_names)
            size_sub_folders = sum(folders_with_size[os.path.join(root,d)] for d in dirs)
            my_size = folders_with_size[root] = size_files + size_sub_folders

            if root == self.staging_folder:
                for file_name in file_names:
                    print("- file {}: {} bytes".format(file_name, os.path.getsize(os.path.join(root, file_name))))

            if self.staging_folder in (root, os.path.dirname(root)):
                print("- folder {}: {} bytes".format(root, my_size))

        print()

    def _assert_target_folder(self):
        if os.path.isdir(self.target_folder):
            raise RuntimeError("target folder already exists: {}".format(self.target_folder))

    def _assert_staging_folder(self):
        if os.path.isdir(self.staging_folder) and os.listdir(self.staging_folder):
            raise RuntimeError("staging folder is not empty: {}".format(self.staging_folder))


@click.command()
@click.argument("target_folder")
@click.option("-s", "--staging-folder", help="Staging folder", default="/tmp/backup_tool_staging")
@click.option("-r", "--resume-from", help="Resume from the given job", default=None)
@click.option("-l", "--leave-staging-folder", is_flag=True,
              help="Allow there to be a non-empty existing staging folder and/or leave it behind")
def backup(target_folder, staging_folder, resume_from, leave_staging_folder):
    """
    Write backups to the given target folder.
    """
    if resume_from:
        leave_staging_folder = True
        log.info("backup tool, resuming from job \"{}\"".format(resume_from))
    else:
        log.info("backup tool, all jobs")

    backup_tool = BackupTool(target_folder, staging_folder, leave_staging_folder)
    backup_tool.backup(resume_from)
    backup_tool.copy_to_target_folder()
    backup_tool.remove_staging_folder(leave_staging_folder)

    log.info("all done")

if __name__ == '__main__':
    backup()
