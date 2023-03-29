import yaml
import logging
from yaml.constructor import ConstructorError


'''
    class reads content files
'''


class Reader:

    '''
        reads yaml files and converts to dictionary
        args:
            - file_path, path to yaml
    '''

    def yml(self, file_path: str) -> dict:
        logging.info('start')
        try:
            with open(file_path, 'r') as file_:
                contents = yaml.safe_load(file_.read())
                logging.info('complete')
                return contents
        except ConstructorError as e:
            raise ValueError('short function forms not supported')
