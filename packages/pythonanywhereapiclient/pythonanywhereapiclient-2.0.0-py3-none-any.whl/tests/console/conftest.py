import json

import pytest
import requests

from pythonanywhereapiclient import console


@pytest.fixture
def console_existing(console_new, data):
    # Global data
    user = data['user']

    # Local data
    console_existing = console_new.copy()
    id = 1

    console_existing['id'] = id
    console_existing['user'] = user
    console_existing['arguments'] = None
    console_existing['working_directory'] = None
    console_existing['name'] = f'Bash console {id}'
    console_existing['console_url'] = f'/user/{user}/consoles/{id}/'
    console_existing['console_frame_url'] = f'/user/{user}/consoles/{id}/frame/'

    return id, console_existing


@pytest.fixture
def console_new():
    return {
        'executable': 'bash',
    }


@pytest.fixture
def console_response_create(data, responses, console_existing):
    id, body = console_existing
    responses.add(
        responses.POST,
        console.client._construct_endpoint_url(console.base_endpoint),
        body=json.dumps(body),
        status=requests.codes.CREATED,
        content_type='application/json',
    )


@pytest.fixture
def console_response_create_unknown(data, responses):
    responses.add(
        responses.POST,
        console.client._construct_endpoint_url(console.base_endpoint),
        body=json.dumps(data['body_unknown_error']),
        status=requests.codes.INTERNAL_SERVER_ERROR,
        content_type='application/json',
    )


@pytest.fixture
def console_response_get_latest_output(console_existing, responses):
    id, body = console_existing
    responses.add(
        responses.GET,
        console.client._construct_endpoint_url(
            f'{console.base_endpoint}{id}/get_latest_output/'
        ),
        body=json.dumps({'output': 'foo'}),
        status=requests.codes.OK,
        content_type='application/json',
    )


@pytest.fixture
def console_response_get_latest_output_unknown(data, responses):
    responses.add(
        responses.GET,
        console.client._construct_endpoint_url(
            f'{console.base_endpoint}1/get_latest_output/'
        ),
        body=json.dumps(data['body_unknown_error']),
        status=requests.codes.INTERNAL_SERVER_ERROR,
        content_type='application/json',
    )


@pytest.fixture
def console_response_kill(console_existing, responses):
    id, body = console_existing
    responses.add(
        responses.DELETE,
        console.client._construct_endpoint_url(f'{console.base_endpoint}{id}/'),
        body=None,
        status=requests.codes.NO_CONTENT,
        content_type='application/json',
    )

    return {'output': 'foo'}


@pytest.fixture
def console_response_kill_unknown(console_existing, data, responses):
    id, body = console_existing
    responses.add(
        responses.DELETE,
        console.client._construct_endpoint_url(f'{console.base_endpoint}{id}/'),
        body=json.dumps(data['body_unknown_error']),
        status=requests.codes.INTERNAL_SERVER_ERROR,
        content_type='application/json',
    )


@pytest.fixture
def console_response_list(responses, console_existing):
    id, body = console_existing
    body = [body]
    responses.add(
        responses.GET,
        console.client._construct_endpoint_url(console.base_endpoint),
        body=json.dumps(body),
        status=requests.codes.OK,
        content_type='application/json',
    )


@pytest.fixture
def console_response_list_unknown(data, responses):
    responses.add(
        responses.GET,
        console.client._construct_endpoint_url(console.base_endpoint),
        body=json.dumps(data['body_unknown_error']),
        status=requests.codes.INTERNAL_SERVER_ERROR,
        content_type='application/json',
    )


@pytest.fixture
def console_response_send_input(data, responses, console_existing):
    id, body = console_existing
    responses.add(
        responses.POST,
        console.client._construct_endpoint_url(
            f'{console.base_endpoint}{id}/send_input/'
        ),
        body=json.dumps(data['body_ok']),
        status=requests.codes.OK,
        content_type='application/json',
    )


@pytest.fixture
def console_response_send_input_unknown(console_existing, data, responses):
    id, body = console_existing
    responses.add(
        responses.POST,
        console.client._construct_endpoint_url(
            f'{console.base_endpoint}{id}/send_input/'
        ),
        body=json.dumps(data['body_unknown_error']),
        status=requests.codes.INTERNAL_SERVER_ERROR,
        content_type='application/json',
    )
