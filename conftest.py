import random

import allure
import pytest

from api.api_client import ApiClient
from utils.helper import Helper


@pytest.fixture
def api_client() -> ApiClient:
    """Fixture providing an API client for tests"""
    return ApiClient()


@pytest.fixture
def create_entity(api_client: ApiClient):
    """
    Fixture that creates an entity and ensures it gets deleted after test completion.

    Returns:
        int: Entity ID
        dict: The created entity data including its ID
    """
    with allure.step("Создание новой сущности"):
        entity_data = api_client.create_entity()
        entity_id = entity_data['id']

    yield entity_id, entity_data

    Helper.delete_entities(api_client, entity_id)


@pytest.fixture
def create_entities(api_client: ApiClient):
    """
    Fixture that creates an entities and ensures it gets deleted after test completion.

    Returns:
        list: Entity IDs
        dict: The created entity data
    """
    entity_ids = []
    entities_data = []

    for _ in range(random.randint(2, 9)):
        entity_data = api_client.create_entity()
        entity_ids.append(entity_data['id'])
        entities_data.append(entity_data)

    yield entity_ids, entities_data

    Helper.delete_entities(api_client, entity_ids)
