import sys

class QsmProcessError(Exception):
    pass

def process_error(append = None):
    message = "Error: process is unable to complete"
    if append != None:
        message += " {}".format(append)
    print(message)
    raise QsmProcessError
