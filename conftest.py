import logging
import random

import allure
import pytest

from api.api_client import ApiClient
from utils.helper import Helper
from utils.logger import Logger


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


@pytest.fixture(scope="session", autouse=True)
def test_session_logger():
    """Create a session-wide logger"""
    logger = Logger(log_level=logging.INFO)
    logger.info("Starting test session")
    yield logger
    logger.info("Test session completed")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to take screenshots on test failure
    """
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        try:
            api_client = item.funcargs.get("api_client")
            if api_client:
                with allure.step("Taking API snapshot due to test failure"):
                    test_name = item.nodeid.replace("/", "_").replace("::", "_")
                    api_client.helper.take_screenshot(f"failure_{test_name}")
                    api_client.helper.take_health_snapshot()
                    api_client.logger.error(f"Test failed: {item.nodeid}")
        except Exception as e:
            print(f"Could not take API snapshot on failure: {e}")
