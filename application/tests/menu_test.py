import pytest
from fastapi.testclient import TestClient

from application.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def init_cache(request):
    request.config.cache.get('menu', None)


@pytest.mark.order(1)
def test_create_menu(request):
    body = {
        'title': 'title',
        'description': 'description'
    }
    response = client.post('/api/v1/menus', json=body)
    json_response = response.json()
    print(response.request)
    print(response)
    print(json_response)
    assert response.status_code == 201
    if response.status_code == 201:
        data = json_response
        request.config.cache.set('menu', data)
    assert response.json()['title'] == body['title']
    assert response.json()['description'] == body['description']


@pytest.mark.order(2)
def test_get_menus():
    response = client.get('/api/v1/menus')
    response_json = response.json()
    print(response.request)
    print(response)
    print(response_json)
    if response:
        assert response.status_code == 200
        assert response.json() != [{}]
    if not response:
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.order(3)
def test_get_menu(request, test_count=False, submenu_count=None, dish_count=None):
    if test_count is False:
        cache = request.config.cache.get('menu', None)
        menu_id = cache['id']
        title = cache['title']
        description = cache['description']
        response = client.get(f'/api/v1/menus/{menu_id}')
        print(response.request)
        print(response)
        print(response.json())
        if response.status_code == 200:
            assert response.status_code == 200
            assert response.json()['id'] == menu_id
            assert response.json()['title'] == title
            assert response.json()['description'] == description
        if response.status_code == 404:
            assert response.status_code == 404
            assert response.json() == {'detail': 'menu not found'}
    if test_count is True:
        cache = request.config.cache.get('menu', None)
        menu_id = cache['id']
        response = client.get(f'/api/v1/menus/{menu_id}')
        print(response.request)
        print(response)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['id'] == menu_id
        assert response.json()['submenus_count'] == submenu_count
        assert response.json()['dishes_count'] == dish_count


@pytest.mark.order(4)
def test_update_menu(request):
    body = {
        'title': 'updated title',
        'description': 'updated description'
    }
    cache = request.config.cache.get('menu', None)
    menu_id = cache['id']
    response = client.patch(f'/api/v1/menus/{menu_id}', json=body)
    print(response.request)
    print(response)
    print(response.json())
    assert response.status_code == 200
    if response.status_code == 200:
        cache['title'] = body['title']
        cache['description'] = body['description']
        request.config.cache.set('menu', cache)
    assert response.json()['title'] == body['title']
    assert response.json()['description'] == body['description']
    test_get_menu(request)


@pytest.mark.order(5)
def test_delete_menu(request):
    cache = request.config.cache.get('menu', None)
    menu_id = cache['id']
    response = client.delete(f'/api/v1/menus/{menu_id}')
    print(response.request)
    print(response)
    assert response.status_code == 200


@pytest.mark.order(6)
def test_deleted_menu(request):
    test_get_menus()
    test_get_menu(request)
