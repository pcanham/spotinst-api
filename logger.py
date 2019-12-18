import logging

class Logging(object):
    # Logging formats
    _log_simple_format = '[%(asctime)s] [%(levelname)s] %(message)s'
    _log_detailed_format = '[%(asctime)s] [%(levelname)s] [%(name)s(%(lineno)s):%(funcName)s] %(message)s'

    def configure(self, verbosity = 0):
        ''' Configure the logging format and verbosity '''

        # Configure our logging output
        if verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG, format=self._log_detailed_format, datefmt='%Y-%m-%d %H:%M:%S')
        elif verbosity >= 1:
            logging.basicConfig(level=logging.INFO, format=self._log_detailed_format, datefmt='%Y-%m-%d %H:%M:%S')
        else:
            logging.basicConfig(level=logging.INFO, format=self._log_simple_format, datefmt='%Y-%m-%d %H:%M:%S')

        # Configure Boto's logging output
        if verbosity >= 4:
            #logging.getLogger('boto3').setLevel(logging.DEBUG)
            #logging.getLogger('botocore').setLevel(logging.DEBUG)
            #logging.getLogger('s3transfer').setLevel(logging.DEBUG)
            logging.getLogger('urllib3').setLevel(logging.DEBUG)
            logging.getLogger('spotinst_sdk').setLevel(logging.DEBUG)
            logging.getLogger('spotinst_sdk.spotinst_functions').setLevel(logging.DEBUG)
        elif verbosity >= 3:
            #logging.getLogger('boto3').setLevel(logging.INFO)
            #logging.getLogger('botocore').setLevel(logging.INFO)
            #logging.getLogger('s3transfer').setLevel(logging.INFO)
            logging.getLogger('urllib3').setLevel(logging.INFO)
            logging.getLogger('spotinst_sdk').setLevel(logging.INFO)
            logging.getLogger('spotinst_sdk.spotinst_functions').setLevel(logging.INFO)
        else:
            #logging.getLogger('boto3').setLevel(logging.CRITICAL)
            #logging.getLogger('botocore').setLevel(logging.CRITICAL)
            #logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
            #logging.getLogger('urllib3').setLevel(logging.CRITICAL)
            logging.getLogger('spotinst_sdk').setLevel(logging.CRITICAL)
            logging.getLogger('spotinst_sdk.spotinst_functions').setLevel(logging.CRITICAL)
