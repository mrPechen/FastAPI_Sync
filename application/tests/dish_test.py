import pytest
from fastapi.testclient import TestClient

from application.main import app

from . import menu_test, submenu_test

client = TestClient(app)


@pytest.fixture(autouse=True)
def init_cache(request):
    request.config.cache.get('menu', None)
    request.config.cache.get('submenu', None)
    request.config.cache.get('dish', None)


@pytest.mark.order(15)
def test_create_menu_and_submenu(request):
    menu_test.test_create_menu(request)
    submenu_test.test_create_submenu(request)


@pytest.mark.order(16)
def test_create_dish(request, test_count=False, new_body=None):
    if test_count is False:
        menu_id = request.config.cache.get('menu', None)['id']
        submenu_id = request.config.cache.get('submenu', None)['id']
        body = {
            'title': 'title dish 15',
            'description': 'description dish 15',
            'price': '1.45'
        }
        response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=body)
        json_response = response.json()
        print(response.request)
        print(response)
        print(json_response)
        assert response.status_code == 201
        if response.status_code == 201:
            data = json_response
            request.config.cache.set('dish', data)
        cache_dish = request.config.cache.get('dish', None)
        assert response.json()['id'] == cache_dish['id']
        assert response.json()['title'] == body['title']
        assert response.json()['description'] == body['description']
        assert response.json()['price'] == body['price']
    if test_count is True:
        menu_id = request.config.cache.get('menu', None)['id']
        submenu_id = request.config.cache.get('submenu', None)['id']
        response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=new_body)
        json_response = response.json()
        print(response.request)
        print(response)
        print(json_response)
        assert response.status_code == 201
        if response.status_code == 201:
            data = json_response
            request.config.cache.set('dish', data)
        cache_dish = request.config.cache.get('dish', None)
        assert response.json()['id'] == cache_dish['id']


@pytest.mark.order(17)
def test_get_dishes(request):
    menu_id = request.config.cache.get('menu', None)['id']
    submenu_id = request.config.cache.get('submenu', None)['id']
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
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


@pytest.mark.order(18)
def test_get_dish(request):
    menu_id = request.config.cache.get('menu', None)['id']
    submenu_id = request.config.cache.get('submenu', None)['id']
    cache_dish = request.config.cache.get('dish', None)
    dish_id = cache_dish['id']
    dish_title = cache_dish['title']
    dish_description = cache_dish['description']
    dish_price = cache_dish['price']
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    print(response.request)
    print(response)
    print(response.json())
    if response.status_code == 200:
        assert response.status_code == 200
        assert response.json()['id'] == dish_id
        assert response.json()['title'] == dish_title
        assert response.json()['description'] == dish_description
        assert response.json()['price'] == dish_price
    if response.status_code == 404:
        assert response.status_code == 404
        assert response.json() == {'detail': 'dish not found'}


@pytest.mark.order(19)
def test_update_submenu(request):
    body = {
        'title': 'updated title dish',
        'description': 'updated description dish',
        'price': '1.00'
    }
    menu_id = request.config.cache.get('menu', None)['id']
    submenu_id = request.config.cache.get('submenu', None)['id']
    cache_dish = request.config.cache.get('dish', None)
    dish_id = cache_dish['id']
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=body)
    print(response.request)
    print(response)
    print(response.json())
    if response.status_code == 200:
        cache_dish['title'] = body['title']
        cache_dish['description'] = body['description']
        cache_dish['price'] = body['price']
        request.config.cache.set('dish', cache_dish)
    assert response.status_code == 200
    assert response.json()['title'] == body['title']
    assert response.json()['description'] == body['description']
    assert response.json()['price'] == body['price']
    test_get_dish(request)


@pytest.mark.order(20)
def test_delete_dish(request):
    menu_id = request.config.cache.get('menu', None)['id']
    submenu_id = request.config.cache.get('submenu', None)['id']
    dish_id = request.config.cache.get('dish', None)['id']
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    print(response.request)
    print(response)
    assert response.status_code == 200


@pytest.mark.order(21)
def test_deleted_dish(request):
    test_get_dishes(request)
    test_get_dish(request)
    submenu_test.test_deleted_submenu(request)
    submenu_test.test_delete_submenu(request)
    menu_test.test_deleted_menu(request)
    menu_test.test_delete_menu(request)
