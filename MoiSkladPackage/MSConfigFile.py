from MSMainClass import MSMainClass

import os
import json


class MSConfigFile(MSMainClass):
    """ configfile connector"""
    logger_name = "configfile"
    dir_name = "config"
    file_name = "ms_main_config.json"


    def get_config_data(self, sector='POSTGRESQL'):
        """ extract data from sql config file
        return config section POSTGRESQL """
        try:
            conf = configparser.ConfigParser()
            up_up_dir = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(up_up_dir, self.dir_name, self.file_name)
            conf.read(CONF_FILE_PATH)
            # self.logger.debug(f"module {__class__.__name__} read configfile")
            return conf[sector]
        except Exception as e:
            # self.logger.error(f"{__class__.__name__} can't read config file", e)
            return None


if __name__ == '__main__':
    connector = ConnALConfigFile()
    print(connector.get_config_data())