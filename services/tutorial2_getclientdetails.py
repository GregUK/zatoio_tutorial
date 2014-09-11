__author__ = 'greg'
# stdlib
from json import dumps, loads

# Zato
from zato.server.service import Service

class GetClientDetails(Service):
    def handle(self):

        self.logger.info('Request: {}'.format(self.request.payload))
        self.logger.info('Request type: {}'.format(type(self.request.payload)))

        # Fetch connection to CRM.  It is name attribute within the out going connections config
        crm = self.outgoing.plain_http.get('CRM')

        # Fetch connection to Payments.  It is name attribute within the out going connections config
        payments = self.outgoing.plain_http.get('Payments')

        # Grab the customer info ..
        cust = crm.conn.send(dumps(self.request.payload))
        cust = loads(cust.text)

        # .. and last payment's details
        last_payment = payments.conn.send(dumps(self.request.payload))
        last_payment = loads(last_payment.text)

        self.logger.info('Customer details: {}'.format(cust))
        self.logger.info('Last payment: {}'.format(last_payment))

        response = {}
        response['first_name'] = cust['firstName']
        response['last_name'] = cust['lastName']
        response['last_payment_date'] = last_payment['DATE']
        response['last_payment_amount'] = last_payment['AMOUNT']
        response = dumps(response)

        self.logger.info('Response: {}'.format(response))

        self.response.payload = response