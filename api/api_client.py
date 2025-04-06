import requests

from api.endpoints import Endpoints
from api.models.entity_model import EntityResponse
from api.payloads import Payloads
from utils.helper import Helper


class ApiClient:
    """Enhanced client for interacting with the Entity API with response validation"""

    def __init__(self) -> None:
        self.payloads = Payloads()
        self.endpoints = Endpoints()
        self.helper = Helper()

    def create_entity(self) -> dict:
        """Create a new entity with optional custom fields"""
        payload = self.payloads.create

        response = requests.post(
            url=self.endpoints.create_entity,
            json=payload
        )
        assert response.status_code == 200, f"Ожидаемый статус 200, полученный {response.status_code}: {response.text}"
        entity_id = response.json()

        return_data = {"id": entity_id, **payload}
        self.helper.attach_response(return_data)

        return return_data

    def get_entity(self, entity_id: str) -> dict:
        """Get an entity by ID with response validation"""
        response = requests.get(
            url=self.endpoints.get_entity(entity_id)
        )

        assert response.status_code == 200, f"Ожидаемый статус 200, полученный {response.status_code}: {response.text}"
        entity_data = response.json()
        EntityResponse(**entity_data)

        self.helper.attach_response(entity_data)
        return entity_data

    def get_all_entities(
            self,
            title: str = None,
            verified: bool = None,
            page: int = None,
            per_page: int = None
    ) -> list:
        """Get a list of entities with optional filtering"""
        params = {}
        if title is not None:
            params["title"] = title
        if verified is not None:
            params["verified"] = verified
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page

        response = requests.get(
            url=self.endpoints.get_all_entities,
            params=params
        )
        assert response.status_code == 200, f"Ожидаемый статус 200, полученный {response.status_code}: {response.text}"

        response_data = response.json()
        self.helper.attach_response(response_data)

        entities = response_data["entity"]
        for entity in entities:
            EntityResponse(**entity)

        return entities

    def update_entity(self, entity_id: str) -> dict:
        """Update an existing entity with optional custom fields"""
        payload = self.payloads.create
        response = requests.patch(
            url=self.endpoints.update_entity(entity_id),
            json=payload
        )
        assert response.status_code == 204, f"Ожидаемый статус 204, полученный {response.status_code}: {response.text}"

        updated_entity = self.get_entity(entity_id)
        self.helper.attach_response(updated_entity)

        return updated_entity

    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity"""
        response = requests.delete(
            url=self.endpoints.delete_entity(entity_id)
        )
        assert response.status_code == 204, f"Ожидаемый статус 204, полученный {response.status_code}: {response.text}"
        return True
