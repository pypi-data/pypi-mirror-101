import json
import stomp
import logging
import socket
import sys
import time

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class MessagingListener(stomp.ConnectionListener):
    '''
    Messaging Listener
    '''
    def __init__(self, broker):
        '''
        __init__
        '''
        self.__broker = broker
        self.logger = logging.getLogger(self.__class__.__name__)

    def on_error(self, headers, body):
        '''
        Error handler
        '''
        self.logger.error('[broker] [%s]: %s', self.__broker, body)

    def on_message(self, headers, body):
        self.logger.info("received message: %s", body)


class Receiver(stomp.ConnectionListener):
    def __init__(self, broker):
        '''
        __init__
        '''
        self.__broker = broker
        self.logger = logging.getLogger(self.__class__.__name__)

    def on_error(self, headers, body):
        '''
        Error handler
        '''
        self.logger.error('[broker] [%s]: %s', self.__broker, body)

    def on_message(self, headers, body):
        self.logger.info("received message: %s", body)
        body = json.loads(body)
        if body['msg_type'] == 'health_heartbeat':
            self.logger.info("received message: %s", body)


# broker = 'atlas-test-mb.cern.ch'
broker = 'atlas-mb.cern.ch'
receiver_port = 61013
# port = 6163
port = 61013
# topic = '/queue/atlas.idds'
topic = '/topic/atlas.idds'
receive_topics = ['/queue/Consumer.jedi.atlas.idds', '/queue/Consumer.prodsys.atlas.idds']
receive_topics = ['/queue/Consumer.monitor.atlas.idds']
# receive_topics = ['/queue/Consumer.jedi.atlas.idds']
username = 'atlasidds'
password = 'PQUxPqQF0DDzJoGz'

addrinfos = socket.getaddrinfo(broker, 0, socket.AF_INET, 0, socket.IPPROTO_TCP)
brokers_resolved = [ai[4][0] for ai in addrinfos]

for broker in brokers_resolved:
    conn = stomp.Connection12(host_and_ports=[(broker, port)], keepalive=True)
    conn.set_listener('message-sender', MessagingListener(conn.transport._Transport__host_and_ports[0]))

    conn.start()
    conn.connect(username, password, wait=True)

    payload = {"files": [{"adler32": "0cc737eb", "scope": "mock", "bytes": 1, "name": "file_ac6db48094974e039aa9d1ae52873596"}], "rse": "WJ-XROOTD", "operation": "add_replicas", "lifetime": 2}

    print("sending message")
    try:
        conn.send(destination=topic, body=json.dumps(payload), id='atlas-idds-messaging', ack='auto', headers={'persistent': 'true', 'vo': 'atlas'})
        pass
    except Exception as ex:
        print(ex)

    # time.sleep(10)
    print("sent message")

    for receive_topic in receive_topics:
        print('start receiver: %s' % receive_topic)
        conn = stomp.Connection12(host_and_ports=[(broker, receiver_port)], keepalive=True)
        conn.set_listener('message-receiver', Receiver(conn.transport._Transport__host_and_ports[0]))

        conn.start()
        conn.connect(username, password, wait=True)
        # conn.subscribe(destination=receive_topic, id='atlas-idds-messaging', ack='auto')
time.sleep(10)
