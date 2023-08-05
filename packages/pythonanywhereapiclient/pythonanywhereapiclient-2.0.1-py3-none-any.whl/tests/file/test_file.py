import pytest
from requests import codes

from pythonanywhereapiclient import file


def test_base_endpoint_is_valid():
    assert 'files/' == file.base_endpoint


def test_delete_not_implemented():
    with pytest.raises(NotImplementedError):
        file.delete()


def test_delete_share_not_implemented():
    with pytest.raises(NotImplementedError):
        file.delete_share()


def test_download_not_implemented():
    with pytest.raises(NotImplementedError):
        file.download()


def test_share_not_implemented():
    with pytest.raises(NotImplementedError):
        file.share()


def test_status_not_implemented():
    with pytest.raises(NotImplementedError):
        file.status()


@pytest.mark.usefixtures('file_response_list')
def test_list_is_successful():
    assert len(file.list('/home/testuser')) == 1


@pytest.mark.usefixtures('file_response_list_unknown')
def test_list_raises_responseerror():
    with pytest.raises(file.ResponseError):
        file.list('/unknown')


@pytest.mark.usefixtures('file_response_upload')
@pytest.mark.parametrize(
    'file_response_upload', [codes.CREATED, codes.OK], indirect=True
)
def test_upload_is_successful(data):
    assert file.upload(f'/home/{data["user"]}', 'textfile') is None


@pytest.mark.usefixtures('file_response_upload_unknown')
def test_upload_raises_responseerror(data):
    with pytest.raises(file.ResponseError):
        file.upload(f'/home/{data["user"]}', 'textfile')
