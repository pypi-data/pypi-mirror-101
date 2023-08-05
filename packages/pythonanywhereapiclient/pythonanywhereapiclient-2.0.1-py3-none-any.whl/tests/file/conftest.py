import json

import pytest
import requests

from pythonanywhereapiclient import file


@pytest.fixture
def schedule_existing(data, schedule_new):
    schedule_existing = schedule_new.copy()
    id = 1
    user = data['user']
    schedule_existing['id'] = id
    schedule_existing['url'] = f'/api/v0/user/{user}/schedule/{id}/'
    schedule_existing['user'] = user
    schedule_existing['expiry'] = '2020-03-26'
    schedule_existing[
        'logfile'
    ] = f'/user/{user}/files/var/log/tasklog-{id}-{schedule_new["interval"]}-at-{schedule_new["hour"]}{schedule_new["minute"]}-{schedule_new["command"]}.log'
    schedule_existing['extend_url'] = f'/user/{user}/schedule/task/{id}/extend'
    schedule_existing[
        'printable_time'
    ] = f'{schedule_new["hour"]}:{schedule_new["minute"]}'
    schedule_existing['can_enable'] = False

    return id, schedule_existing


@pytest.fixture
def schedule_new():
    return {
        'command': 'clear',
        'enabled': True,
        'interval': 'daily',
        'hour': 12,
        'minute': 59,
    }


@pytest.fixture
def file_response_list(data, responses):
    responses.add(
        responses.GET,
        file.client._construct_endpoint_url(
            f'{file.base_endpoint}tree/?path=/home/{data["user"]}'
        ),
        body=json.dumps([f'/home/{data["user"]}/README.txt']),
        status=requests.codes.OK,
        content_type='application/json',
    )


@pytest.fixture
def file_response_list_unknown(data, responses):
    responses.add(
        responses.GET,
        file.client._construct_endpoint_url(
            f'{file.base_endpoint}tree/?path=/unknown'
        ),
        body=json.dumps({'detail': '/unknown does not exist'}),
        status=requests.codes.BAD_REQUEST,
        content_type='application/json',
    )


@pytest.fixture
def file_response_upload(data, request, responses):
    responses.add(
        responses.POST,
        file.client._construct_endpoint_url(
            f'{file.base_endpoint}path/home/{data["user"]}'
        ),
        body=None,
        status=request.param,
        content_type='application/json',
    )


@pytest.fixture
def file_response_upload_unknown(data, responses):
    responses.add(
        responses.POST,
        file.client._construct_endpoint_url(
            f'{file.base_endpoint}path/home/{data["user"]}'
        ),
        body=json.dumps(data['body_unknown_error']),
        status=requests.codes.INTERNAL_SERVER_ERROR,
        content_type='application/json',
    )
