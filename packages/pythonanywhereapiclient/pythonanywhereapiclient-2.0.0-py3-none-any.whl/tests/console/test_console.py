import pytest

from pythonanywhereapiclient import console


def test_base_endpoint_is_valid():
    assert 'consoles/' == console.base_endpoint
    assert console.client


@pytest.mark.usefixtures('console_response_create')
def test_create_is_successful(console_existing, console_new):
    id, body = console_existing

    assert console.create(**console_new) == body


@pytest.mark.usefixtures('console_response_create_unknown')
def test_create_raises_responseerror(console_new):
    with pytest.raises(console.ResponseError):
        console.create(**console_new)


def test_get_not_implemented():
    with pytest.raises(NotImplementedError):
        console.get()


@pytest.mark.usefixtures('console_response_get_latest_output')
def test_get_latest_output_is_successful(console_existing):
    id, body = console_existing

    assert console.get_latest_output(id) == {'output': 'foo'}


@pytest.mark.usefixtures('console_response_get_latest_output_unknown')
def test_get_latest_output_raises_responseerror(console_existing):
    id, body = console_existing

    with pytest.raises(console.ResponseError):
        console.get_latest_output(id)


@pytest.mark.usefixtures('console_response_kill')
def test_kill_is_successful(console_existing):
    id, body = console_existing

    assert console.kill(id) is None


@pytest.mark.usefixtures('console_response_kill_unknown')
def test_kill_raises_responseerror(console_existing):
    id, body = console_existing

    with pytest.raises(console.ResponseError):
        console.kill(id)


@pytest.mark.usefixtures('console_response_list')
def test_list_is_successful(console_existing):
    id, body = console_existing

    assert console.list() == [body]


@pytest.mark.usefixtures('console_response_list_unknown')
def test_list_raises_responseerror():
    with pytest.raises(console.ResponseError):
        console.list()


def test_list_shared_not_implemented():
    with pytest.raises(NotImplementedError):
        console.list_shared()


@pytest.mark.usefixtures('console_response_send_input')
def test_send_input_is_successful(console_existing):
    id, body = console_existing

    assert console.send_input(id, 'whoami') is None


@pytest.mark.usefixtures('console_response_send_input_unknown')
def test_send_input_raises_responseerror(console_existing):
    id, body = console_existing

    with pytest.raises(console.ResponseError):
        console.send_input(id, 'whoami')
