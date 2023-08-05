import pytest
from requests import codes

from pythonanywhereapiclient import webapp
from pythonanywhereapiclient.utils import construct_request_payload


def test_base_is_valid():
    assert 'webapps/' == webapp.base_endpoint
    assert webapp.client


@pytest.mark.usefixtures('webapp_response_create')
@pytest.mark.parametrize(
    'webapp_response_create', [codes.CREATED, codes.OK], indirect=True
)
def test_create_is_successful(webapp_new):
    assert webapp_new == webapp.create(**webapp_new)


def test_create_requires_domain_name_and_python_version_as_argument():
    with pytest.raises(TypeError) as exc:
        webapp.create()

    assert 'required positional argument' in str(exc.value)
    assert 'domain_name' in str(exc.value)
    assert 'python_version' in str(exc.value)


@pytest.mark.usefixtures('webapp_response_create_forbidden')
def test_create_raises_quotaerror(webapp_new):
    with pytest.raises(webapp.QuotaError):
        webapp.create(**webapp_new)


@pytest.mark.usefixtures('webapp_response_create_unknown')
def test_create_raises_responseerror(webapp_new):
    with pytest.raises(webapp.ResponseError):
        webapp.create(**webapp_new)


@pytest.mark.usefixtures('webapp_response_create_static')
def test_create_static_is_successful(webapp_static_new):
    domain_name, body = webapp_static_new

    assert body == webapp.create_static(domain_name=domain_name, **body)


@pytest.mark.usefixtures('webapp_response_create_static_unknown')
def test_create_static_raises_responseerror(webapp_static_new):
    domain_name, body = webapp_static_new

    with pytest.raises(webapp.ResponseError):
        webapp.create_static(domain_name, **body)


@pytest.mark.usefixtures('webapp_response_delete')
def test_delete_is_successful(webapp_existing):
    domain_name, body = webapp_existing

    assert webapp.delete(domain_name=domain_name) is None


@pytest.mark.usefixtures('webapp_response_delete_unknown')
def test_delete_raises_responseerror(webapp_existing):
    domain_name, body = webapp_existing

    with pytest.raises(webapp.ResponseError):
        webapp.delete(domain_name=domain_name)


def test_delete_ssl_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.delete_ssl()


def test_delete_static_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.delete_static()


@pytest.mark.usefixtures('webapp_response_disable')
def test_disable_is_successful(webapp_existing):
    domain_name, body = webapp_existing

    assert webapp.disable(domain_name=domain_name) is None


@pytest.mark.usefixtures('webapp_response_disable_unknown')
def test_disable_raises_responseerror(webapp_existing):
    domain_name, body = webapp_existing

    with pytest.raises(webapp.ResponseError):
        webapp.disable(domain_name=domain_name)


@pytest.mark.usefixtures('webapp_response_enable')
def test_enable_is_successful(webapp_existing):
    domain_name, body = webapp_existing

    assert webapp.enable(domain_name=domain_name) is None


@pytest.mark.usefixtures('webapp_response_enable_unknown')
def test_enable_raises_responseerror(webapp_existing):
    domain_name, body = webapp_existing

    with pytest.raises(webapp.ResponseError):
        webapp.enable(domain_name=domain_name)


def test_get_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.get()


def test_get_ssl_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.get_ssl()


def test_get_static_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.get_static()


@pytest.mark.usefixtures('webapp_response_list')
def test_list_is_successful(webapp_existing):
    domain_name, body = webapp_existing

    assert [body] == webapp.list()


@pytest.mark.usefixtures('webapp_response_list_unknown')
def test_list_raises_responseerror():
    with pytest.raises(webapp.ResponseError):
        webapp.list()


def test_list_static_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.list_static()


@pytest.mark.usefixtures('webapp_response_modify')
def test_modify_is_successful(webapp_existing):
    domain_name, body = webapp_existing
    params = construct_request_payload(
        body.copy(), exclude=['id', 'domain_name', 'user', 'expiry']
    )

    assert body == webapp.modify(domain_name=domain_name, **params)


@pytest.mark.usefixtures('webapp_response_modify_unknown')
def test_modify_raises_responseerror(webapp_existing):
    domain_name, body = webapp_existing
    params = construct_request_payload(
        body.copy(), exclude=['id', 'domain_name', 'user', 'expiry']
    )

    with pytest.raises(webapp.ResponseError):
        webapp.modify(domain_name=domain_name, **params)


def test_modify_ssl_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.modify_ssl()


def test_modify_static_not_implemented():
    with pytest.raises(NotImplementedError):
        webapp.modify_static()


@pytest.mark.usefixtures('webapp_response_reload')
def test_reload_is_successful(webapp_existing):
    domain_name, body = webapp_existing

    assert webapp.reload(domain_name=domain_name) is None


@pytest.mark.usefixtures('webapp_response_reload_unknown')
def test_reload_raises_responseerror(webapp_existing):
    domain_name, body = webapp_existing

    with pytest.raises(webapp.ResponseError):
        webapp.reload(domain_name=domain_name)
