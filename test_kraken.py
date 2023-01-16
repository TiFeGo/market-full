import requests
import pytest
import json
import random


@pytest.fixture
def headers():
    headers_ = {
        'accept': 'application/json',
    }
    return headers_


@pytest.fixture
def user():
    return {
        'name': 'user',
        'email': 'user1@example.com',
        'password': 'string'
    }


@pytest.fixture
def credentials(user):
    return {
        'grant_type': '',
        'username': user['email'],
        'password': user['password'],
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }


@pytest.fixture
def url():
    return 'http://localhost:8080/v1'


def test_get_all_products(headers, url):
    params = {
        'skip': '0',
        'limit': '10',
    }

    response = requests.get(f'{url}/products/', headers=headers, params=params)

    assert response.status_code == 200
    data = json.loads(response.content.decode())
    assert 'products' in data.keys()


def test_register_new_user(headers, user, url):
    headers['Content-Type'] = 'application/json'

    response = requests.post(f'{url}/users/', headers=headers, json=user)
    data = json.loads(response.content.decode())
    assert response.status_code == 200
    assert data['name'] == user['name']
    assert data['email'] == user['email']
    assert data['id']


def test_get_access_token(headers, credentials, url):

    response = requests.post(f'{url}/login', headers=headers, data=credentials)
    assert response.status_code == 200
    user_access_token = json.loads(response.content.decode())['access_token']
    assert user_access_token != ''


def test_access(headers, credentials, url):
    headers['content-type'] = 'application/x-www-form-urlencoded'

    params = {
        'user_id': '1',
    }

    response = requests.post(f'{url}/cart/confirm', params=params, headers=headers)

    assert response.status_code == 401

    response = requests.post(f'{url}/login', headers=headers, data=credentials)
    assert response.status_code == 200
    user_access_token = json.loads(response.content.decode())['access_token']
    assert user_access_token != ''

    headers['Authorization'] = f'Bearer {user_access_token}'
    response = requests.post(f'{url}/login', headers=headers, data=credentials)
    assert response.status_code == 200
