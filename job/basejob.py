import glob
import logging
import os
import shutil
import tarfile

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class BaseJob:
    def __init__(self, configuration, output_folder):
        self.configuration = configuration
        self.output_folder = output_folder
        self._validate_configuration(configuration)

    def __str__(self):
        return "job {}".format(self.__module__)

    def is_name(self, name):
        return name in [self.__module__, "{}.{}".format(self.__module__, self.__class__.__name__), self.__str__()]

    def _validate_configuration(self, configuration):
        pass

    def _package_folder(self, name, location):
        if not os.path.exists(location):
            raise RuntimeError("location does not exist: {}".format(location))

        log.info("packaging up {} as {}".format(location, name))

        output_filename = "{}/{}.tar.gz".format(self.output_folder, name)
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(location, arcname=os.path.basename(location))

    def _copy_folder(self, target_folder, source_folder):
        absolute_target_folder = "{}/{}".format(self.output_folder, target_folder)
        log.info("copying from source folder {} to target folder {}".format(source_folder, target_folder))
        shutil.copytree(source_folder, absolute_target_folder)

    def _copy_files(self, target_folder, source_folder, extensions_mask):
        absolute_target_folder = "{}/{}".format(self.output_folder, target_folder)
        if not os.path.exists(absolute_target_folder):
            os.makedirs(absolute_target_folder)

        log.info("copying {} from source folder {} to target folder {}".format(extensions_mask, source_folder,
                                                                               target_folder))
        files = glob.iglob(os.path.join(source_folder, extensions_mask))
        for file in files:
            if os.path.isfile(file):
                shutil.copy2(file, absolute_target_folder)
