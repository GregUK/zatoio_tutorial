__author__ = 'greg'
# stdlib
import logging

# ZeroMQ
import zmq

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

address = 'tcp://127.0.0.1:35101'

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind(address)

logging.info('Fraud detection app running on {}'.format(address))

while True:
    msg = socket.recv_json()
    logging.info(msg)
