
class InsertError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InsertError, {0}'.format(self.message)
        else:
            return 'InsertError has been raised.'

class UpdateError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'UpdateError, {0}'.format(self.message)
        else:
            return 'UpdateError has been raised.'

class DeleteError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'DeleteError, {0}'.format(self.message)
        else:
            return 'DeleteError has been raised.'

class FetchError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FetchError, {0}'.format(self.message)
        else:
            return 'FetchError has been raised.'

class InputError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InputError, {0}'.format(self.message)
        else:
            return 'InputError has been raised.'

class LoginError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'LoginError, {0}'.format(self.message)
        else:
            return 'LoginError has been raised.'

class RecoverPasswordError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'RecoverPasswordError, {0}'.format(self.message)
        else:
            return 'RecoverPasswordError has been raised.'

class SelectionError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'SelectionError, {0}'.format(self.message)
        else:
            return 'SelectionError has been raised.'

class CaptureError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'CaptureError, {0}'.format(self.message)
        else:
            return 'CaptureError has been raised.'

class FileMissingError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FileMissingError, {0}'.format(self.message)
        else:
            return 'FileMissingError has been raised.'

class FileSizeError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FileSizeError, {0}'.format(self.message)
        else:
            return 'FileSizeError has been raised.'


class ApplicationSubmissionError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ApplicationSubmissionError, {0}'.format(self.message)
        else:
            return 'ApplicationSubmissionError has been raised.'
        
