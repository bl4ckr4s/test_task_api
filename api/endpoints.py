HOST = "http://localhost:8080"


class Endpoints:
    create_entity = f"{HOST}/api/create"
    get_all_entities = f"{HOST}/api/getAll"
    get_entity = lambda self, entity_id: f"{HOST}/api/get/{entity_id}"
    update_entity = lambda self, entity_id: f"{HOST}/api/patch/{entity_id}"
    delete_entity = lambda self, entity_id: f"{HOST}/api/delete/{entity_id}"
