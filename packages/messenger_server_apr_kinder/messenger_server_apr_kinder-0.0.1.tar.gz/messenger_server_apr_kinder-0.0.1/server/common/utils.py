from common.variables import *
# from errors import IncorrectDataRecivedError, NonDictInputError
import json
import sys
sys.path.append('../')
from common.decos import log


@log
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        try:
            response = json.loads(json_response)
        except json.decoder.JSONDecodeError as err:
            print(err)
        if isinstance(response, dict):
            return response
        else:
            # raise IncorrectDataRecivedError
            raise ERROR
    else:
        # raise IncorrectDataRecivedError
        raise ERROR


@log
def send_message(sock, message):
    if not isinstance(message, dict):
        # raise NonDictInputError
        raise ERROR
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
