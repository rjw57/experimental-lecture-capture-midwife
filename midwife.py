import logging
import datetime

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest


# Logger
LOG = logging.getLogger(__name__)

# Global state dict. State is kept in this dict to avoid having to remember to use the "global"
# keyword. If this were just a set of global variables, then one would have to remember to use
# global at the top of all functions which do assignment otherwise it would silently create a copy
# of the state, not mutate it.
STATE = {
    # Global dict of payloads keyed by hostname. Each entry has the following form:
    #   {
    #       "receivedAt": UTC date time when payload was received.
    #       "payload": <Decoded JSON body of payload>,
    #   }
    'payloads': {},
}

# Maximum "age" of a payload before it is garbage collected
PAYLOAD_MAX_AGE = datetime.timedelta(days=2)

# The Flask application object.
app = Flask(__name__)


# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route('/healthz')
def healthz():
    return jsonify(ok=True)


@app.route('/payloads')
def payloads():
    _gc_payloads()
    return jsonify(**{
        hostname: {
            'receivedAt': record['receivedAt'].isoformat(),
            'payload': record['payload'],
        }
        for hostname, record in STATE['payloads'].items()
    })


@app.route('/cry', methods=['POST'])
def cry():
    payload = request.get_json()
    if 'hostname' not in payload:
        LOG.warn('Payload contained no hostname')
        raise BadRequest()

    _gc_payloads()
    STATE['payloads'][payload['hostname']] = {
        'receivedAt': datetime.datetime.utcnow(),
        'payload': payload,
    }

    return jsonify(ok=True)


def _gc_payloads():
    """
    "Garbage collect" the payloads by removing all payloads received more than PAYLOAD_MAX_AGE ago.

    """
    now = datetime.datetime.utcnow()
    STATE['payloads'] = {
        k: v for k, v in STATE['payloads'].items()
        if now - v.get('receivedAt', now) < PAYLOAD_MAX_AGE
    }
