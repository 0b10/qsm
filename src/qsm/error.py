class QsmProcessError(Exception):
    """Raised when a process returns a non-zero exit status
    """
    pass


def raise_process_error(append=None):
    message = "Error: process is unable to complete"

    if append is not None:
        message += " {}".format(append)

    print(message)
    raise QsmProcessError
