from requests import codes

from pythonanywhereapiclient.client import Client
from pythonanywhereapiclient.error import ResponseError


base_endpoint = 'files/'
client = Client()


def delete():
    """Deletes the file at the specified path"""
    raise NotImplementedError


def delete_share():
    """Stop sharing a path"""
    raise NotImplementedError


def download():
    """Downloads the file at the specified path"""
    raise NotImplementedError


def list(path):
    """Returns a list of the contents of a directory, and its subdirectories as
    a list"""
    response = client.get(f'{base_endpoint}tree/?path={path}')

    if response.status_code == codes.OK:
        return response.json()
    else:
        raise ResponseError(response)


def share():
    """Start sharing a file"""
    raise NotImplementedError


def status():
    """Check sharing status for a path"""
    raise NotImplementedError


def upload(path, file):
    """Uploads a file to the specified file path"""
    payload = {'content': file}
    response = client.post(f'{base_endpoint}path{path}', files=payload)

    if response.status_code in [codes.CREATED, codes.OK]:
        return
    else:
        raise ResponseError(response)
