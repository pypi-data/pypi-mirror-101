import pytest

from pythonanywhereapiclient import schedule


def test_base_is_valid():
    assert 'schedule/' == schedule.base_endpoint
    assert schedule.client


@pytest.mark.usefixtures('schedule_response_create')
def test_create_is_successful(schedule_new):
    assert schedule_new == schedule.create(**schedule_new)


def test_create_requires_command_as_argument():
    with pytest.raises(TypeError) as exc:
        schedule.create()

    assert 'required positional argument' in str(exc.value)
    assert 'command' in str(exc.value)


@pytest.mark.usefixtures('schedule_response_create_forbidden')
def test_create_raises_quotaerror(schedule_new):
    with pytest.raises(schedule.QuotaError):
        schedule.create(**schedule_new)


@pytest.mark.usefixtures('schedule_response_create_unknown')
def test_create_raises_responseerror(schedule_new):
    with pytest.raises(schedule.ResponseError):
        schedule.create(**schedule_new)


@pytest.mark.usefixtures('schedule_response_delete')
def test_delete_is_successful(schedule_existing):
    id, body = schedule_existing

    assert schedule.delete(id=id) is None


@pytest.mark.usefixtures('schedule_response_delete_unknown')
def test_delete_raises_quotaerror(schedule_existing):
    id, body = schedule_existing

    with pytest.raises(schedule.ResponseError):
        schedule.delete(id=id)


def test_delete_requires_id_as_argument():
    with pytest.raises(TypeError) as exc:
        schedule.delete()

    assert 'required positional argument' in str(exc.value)
    assert 'id' in str(exc.value)


@pytest.mark.usefixtures('schedule_response_get')
def test_get_is_successful(schedule_existing):
    id, body = schedule_existing

    assert body == schedule.get(id=id)


@pytest.mark.usefixtures('schedule_response_get_unknown')
def test_get_raises_responseerror(schedule_existing):
    id, body = schedule_existing

    with pytest.raises(schedule.ResponseError):
        schedule.get(id=id)


def test_get_requires_id_as_argument():
    with pytest.raises(TypeError) as exc:
        schedule.get()

    assert 'required positional argument' in str(exc.value)
    assert 'id' in str(exc.value)


@pytest.mark.usefixtures('schedule_response_list')
def test_list_is_successful(schedule_existing):
    id, body = schedule_existing

    assert [body] == schedule.list()


@pytest.mark.usefixtures('schedule_response_list_unknown')
def test_list_raises_responseerror():
    with pytest.raises(schedule.ResponseError):
        schedule.list()


def test_modify_not_implemented():
    with pytest.raises(NotImplementedError):
        schedule.modify()
