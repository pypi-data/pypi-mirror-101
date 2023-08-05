from requests import codes

from pythonanywhereapiclient.client import Client
from pythonanywhereapiclient.error import ResponseError
from pythonanywhereapiclient.utils import construct_request_payload


base_endpoint = 'consoles/'
client = Client()


def create(executable, arguments=None, working_directory=None):
    """Create a new console object"""
    response = client.post(
        f'{base_endpoint}',
        data=construct_request_payload(locals()),
    )

    if response.status_code == codes.CREATED:
        return response.json()
    else:
        raise ResponseError(response)


def get():
    """Return information about a console instance"""
    raise NotImplementedError


def get_latest_output(id):
    """Get the most recent output from the console (approx. 500 characters)"""
    response = client.get(f'{base_endpoint}{id}/get_latest_output/')

    if response.status_code == codes.OK:
        return response.json()
    else:
        raise ResponseError(response)


def kill(id):
    """Kill a console"""
    response = client.delete(f'{base_endpoint}{id}/')

    if response.status_code == codes.NO_CONTENT:
        return
    else:
        raise ResponseError(response)


def list():
    """List all your consoles"""
    response = client.get(base_endpoint)

    if response.status_code == codes.OK:
        return response.json()
    else:
        raise ResponseError(response)


def list_shared():
    """View consoles shared with you"""
    raise NotImplementedError


def send_input(id, input):
    """Type into the console. Add a "\n" for return"""
    response = client.post(
        f'{base_endpoint}{id}/send_input/',
        data=construct_request_payload(locals(), exclude=['id']),
    )

    if response.status_code == codes.OK:
        return
    else:
        raise ResponseError(response)
