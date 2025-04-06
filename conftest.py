import allure
import pytest

from api.api_client import ApiClient


@pytest.fixture
def api_client() -> ApiClient:
    """Fixture providing an API client for tests"""
    return ApiClient()


@pytest.fixture
def create_entity(api_client: ApiClient):
    """
    Fixture that creates an entity and ensures it gets deleted after test completion.

    Returns:
        dict: The created entity data including its ID
    """
    with allure.step("Создание новой сущности"):
        entity_data = api_client.create_entity()
        entity_id = entity_data['id']

    yield entity_data

    try:
        with allure.step(f"Удаление созданной сущности c ID: {entity_id}"):
            api_client.delete_entity(entity_id)
    except Exception as e:
        print(f"Warning: Failed to delete entity {entity_id}: {e}")
