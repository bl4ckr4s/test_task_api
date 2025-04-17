import json

import allure
from allure_commons.types import AttachmentType
from requests import Response

from utils.screenshot import ApiScreenshot


class Helper:

    def __init__(self):
        """Initialize Helper with ApiScreenshot"""
        self.screenshot = ApiScreenshot()

    @staticmethod
    def attach_response(response: dict[str, object] | list[dict[str, object]]) -> None:
        """Attach API response to Allure report

        Args:
            response: Response data to attach
        """
        response_str = json.dumps(response, indent=4)
        allure.attach(body=response_str, name="Ответ API", attachment_type=AttachmentType.JSON)

    @staticmethod
    def assert_status_code(response: Response, expected_status: int) -> None:
        """Attach API response to Allure report

        Args:
            response: Response data to attach
            expected_status: Expected status for this response
        """
        assert response.status_code == expected_status, \
            f"Ожидаемый статус {expected_status}, полученный {response.status_code}: {response.text}"

    @staticmethod
    def delete_entities(api_client, entity_ids: list or int):
        """
        Helper method to delete entities by their IDs.

        Args:
            api_client: API client instance
            entity_ids: Single ID or list of IDs to delete
        """
        if not isinstance(entity_ids, list):
            entity_ids = [entity_ids]

        for entity_id in entity_ids:
            with allure.step(f"Удаление созданной сущности c ID: {entity_id}"):
                try:
                    api_client.delete_entity(entity_id)
                except Exception as e:
                    print(f"Warning: Failed to delete entity {entity_id}: {e}")

    def take_screenshot(self, name="api_state"):
        """
        Take an API state screenshot and attach it to the Allure report

        Args:
            name: Name prefix for the screenshot
        """
        return self.screenshot.take_api_snapshot(name)

    def take_health_snapshot(self):
        """
        Take a health snapshot of the API service

        Returns:
            dict: Health data snapshot
        """
        return self.screenshot.take_service_health_snapshot()
