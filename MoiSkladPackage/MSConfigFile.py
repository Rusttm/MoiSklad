from MSMainClass import MSMainClass

import os
import json


class MSConfigFile(MSMainClass):
    """ json configfile connector"""
    logger_name = "configfile"
    dir_name = ["config"]
    file_name = "ms_main_config.json"
    file_path = os.path

    def check_json_config_file(self):
        """ extract data from sql config file
        return config section POSTGRESQL """
        try:
            pkg_dir = os.path.dirname(__file__)
            dirs_path = pkg_dir
            for d in self.dir_name:
                dirs_path = os.path.join(dirs_path, d)
            self.file_path = os.path.join(dirs_path, self.file_name)
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"file {self.file_path} not found")
            # self.logger.debug(f"module {__class__.__name__} read config from {self.file_path}")
            return  True
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't find config file")
            return False
    def read_json_file(self) -> dict:
        d = dict()
        try:
            if self.check_json_config_file():
                with open(self.file_path) as f:
                    d = json.load(f)
                    print(d)
        except Exception as e:
            self.logger.debug(f"module {__class__.__name__} can't read data from config file")
        return d

if __name__ == '__main__':
    connector = MSConfigFile()
    print(connector.read_json_file())