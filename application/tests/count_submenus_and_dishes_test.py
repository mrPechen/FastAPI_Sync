import pytest
from fastapi.testclient import TestClient

from application.main import app

from . import dish_test, menu_test, submenu_test

client = TestClient(app)


@pytest.fixture(autouse=True)
def init_cache(request):
    request.config.cache.get('menu', None)
    request.config.cache.get('submenu', None)
    request.config.cache.get('dish', None)


@pytest.mark.order(22)
def test_create_response(request):
    menu_test.test_create_menu(request)
    submenu_test.test_create_submenu(request)
    body = {
        'title': 'title dish',
        'description': 'description dish',
        'price': '2.30'
    }
    dish_test.test_create_dish(request, test_count=True, new_body=body)
    body = {
        'title': 'title dish 2',
        'description': 'description dish 2',
        'price': '2.30'
    }
    dish_test.test_create_dish(request, test_count=True, new_body=body)
    menu_test.test_get_menu(request, test_count=True, submenu_count=1, dish_count=2)
    submenu_test.test_get_submenu(request, test_count=True, dish_count=2)
    submenu_test.test_delete_submenu(request)
    submenu_test.test_get_submenus(request)
    dish_test.test_get_dishes(request)
    menu_test.test_get_menu(request, test_count=True, submenu_count=0, dish_count=0)
    menu_test.test_delete_menu(request)
    menu_test.test_get_menus()
