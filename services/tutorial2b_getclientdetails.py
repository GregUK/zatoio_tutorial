# stdlib
from datetime import datetime
from json import dumps, loads

# Zato
from zato.server.service import Service

class GetClientDetails(Service):

    def should_notify_frauds(self, cust_type):
        config_key = 'myapp:fraud-detection:cust-type'
        return cust_type in self.kvdb.conn.lrange(config_key, 0, -1)

    def handle(self):

        request = dumps(self.request.payload)

        self.logger.info('Request: {}'.format(self.request.payload))
        self.logger.info('Request type: {}'.format(type(self.request.payload)))

        # Fetch connection to CRM
        crm = self.outgoing.plain_http.get('CRM')

        # Fetch connection to Payments
        payments = self.outgoing.plain_http.get('Payments')

        # Grab the customer info ..
        cust = crm.conn.send(request)
        cust = loads(cust.text)

        # .. and last payment's details
        last_payment = payments.conn.send(request)
        last_payment = loads(last_payment.text)

        self.logger.info('Customer details: {}'.format(cust))
        self.logger.info('Last payment: {}'.format(last_payment))

        # Create response

        response = {}
        response['first_name'] = cust['firstName']
        response['last_name'] = cust['lastName']
        response['last_payment_date'] = last_payment['DATE']
        response['last_payment_amount'] = last_payment['AMOUNT']
        response = dumps(response)

        self.logger.info('Response: {}'.format(response))

        # Create a request to fraud detection and send it asynchronously
        # but only if a customer is of a certain type.

        if self.should_notify_frauds(self.request.payload['cust_type']):

            fraud_request = {}
            fraud_request['timestamp'] = datetime.utcnow().isoformat()
            fraud_request['request'] = request
            fraud_request['response'] = response
            fraud_request = dumps(fraud_request)

            self.outgoing.zmq.send(fraud_request, 'Fraud detection')

        else:
            self.logger.info('Skipped fraud detection for CID {}'.format(self.cid))

        # And return response to the caller
        self.response.payload = response