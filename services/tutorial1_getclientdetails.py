__author__ = 'greg'

from zato.server.service import Service

class GetClientDetails(Service):
    def handle(self):
        self.log_input()