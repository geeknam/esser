

class BaseCommandDispatcher(object):

    def send(self, command):
        raise NotImplementedError('send() not implemented')
