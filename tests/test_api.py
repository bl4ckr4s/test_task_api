import allure

from api.api_client import ApiClient


@allure.epic("API Сущностей")
class TestEntityApi:

    @allure.feature("Создание Сущности")
    @allure.title("Тест успешного создания сущности")
    def test_create_entity(self, api_client: ApiClient):
        with allure.step("Создание новой сущности"):
            response = api_client.create_entity()
            entity_id = response['id']

        with allure.step("Проверка получения ID сущности"):
            assert entity_id, "ID сущности не должен быть пустым"

        with allure.step("Получение и проверка созданной сущности"):
            entity = api_client.get_entity(entity_id)
            assert entity['title'] == response['title'], "Заголовок должен соответствовать созданному"
            assert entity['verified'] == response['verified'], "Статус проверки должен соответствовать созданному"
            assert entity['important_numbers'] == response[
                'important_numbers'], "Массив чисел должен соответствовать созданному"

        with allure.step(f"Удаление созданной сущности c ID: {entity_id}"):
            api_client.delete_entity(entity_id)

    @allure.feature("Получение Сущности")
    @allure.title("Тест получения сущности по ID")
    def test_get_entity(self, api_client: ApiClient, create_entity):
        entity_id = create_entity['id']

        with allure.step(f"Получение сущности по ID: {entity_id}"):
            retrieved_entity = api_client.get_entity(entity_id)

        with allure.step("Проверка соответствия данных сущности"):
            assert retrieved_entity['id'] == entity_id, "ID полученной сущности должен соответствовать запрошенному"
            assert retrieved_entity['title'] == create_entity['title'], "Заголовок должен соответствовать созданному"
            assert retrieved_entity['verified'] == create_entity[
                'verified'], "Статус проверки должен соответствовать созданному"
            assert retrieved_entity['important_numbers'] == create_entity[
                'important_numbers'], "Массив чисел должен соответствовать созданному"
            assert 'addition' in retrieved_entity, "Сущность должна содержать блок дополнительных данных"
            assert 'additional_info' in retrieved_entity[
                'addition'], "Блок дополнительных данных должен содержать additional_info"
            assert 'additional_number' in retrieved_entity[
                'addition'], "Блок дополнительных данных должен содержать additional_number"

    @allure.feature("Получение Всех Сущностей")
    @allure.title("Тест получения всех сущностей с фильтрами")
    def test_get_all_entities(self, api_client: ApiClient):
        entity_ids = []
        entities_data = []

        with allure.step("Создание тестовых сущностей"):
            for _ in range(3):
                response = api_client.create_entity()
                entity_ids.append(response['id'])
                entities_data.append(response)

        with allure.step("Получение всех сущностей"):
            all_entities = api_client.get_all_entities()

        with allure.step("Проверка получения всех сущностей"):
            entity_ids_in_response = [entity['id'] for entity in all_entities]
            for entity_id in entity_ids:
                assert entity_id in entity_ids_in_response, f"Созданная сущность {entity_id} должна присутствовать в списке"

        with allure.step("Получение сущностей с фильтром по заголовку"):
            target_title = entities_data[0]['title']
            filtered_by_title = api_client.get_all_entities(title=target_title)

        with allure.step("Проверка фильтрации по заголовку"):
            assert isinstance(filtered_by_title, list), "Результат должен быть списком"
            if filtered_by_title:  # If any results returned
                for entity in filtered_by_title:
                    assert target_title in entity['title'], f"Все сущности должны содержать переданный заголовок: {target_title}"

        with allure.step("Получение сущностей с фильтром по статусу проверки"):
            verified_entities = api_client.get_all_entities(verified=True)

        with allure.step("Проверка фильтрации по статусу проверки"):
            for entity in verified_entities:
                assert entity['verified'] is True, "Все полученные сущности должны иметь параметр verified=True"

        with allure.step("Тестирование пагинации"):
            paginated_entities = api_client.get_all_entities(page=1, per_page=2)

        with allure.step("Проверка работы пагинации"):
            assert len(paginated_entities) <= 2, "При параметре per_page=2 должно быть получено не более 2 сущностей"

        with allure.step("Удаление всех созданных сущностей"):
            for entity_id in entity_ids:
                with allure.step(f"Удаление созданной сущности c ID: {entity_id}"):
                    api_client.delete_entity(entity_id)

    @allure.feature("Обновление Сущности")
    @allure.title("Тест обновления сущности")
    def test_update_entity(self, api_client: ApiClient, create_entity):
        original_data = create_entity
        entity_id = original_data['id']

        with allure.step(f"Обновление сущности с ID: {entity_id}"):
            updated_entity = api_client.update_entity(entity_id)

        with allure.step("Проверка корректности обновления всех полей сущности"):
            assert updated_entity['id'] == entity_id, "ID не должен измениться"
            assert updated_entity['title'] != original_data['title'], "Заголовок должен быть изменен"
            assert 'important_numbers' in updated_entity, "Должен присутствовать массив чисел"
            assert updated_entity['addition'] != original_data['addition'], "Дополнительные данные должны быть обновлены"

    @allure.feature("Удаление Сущности")
    @allure.title("Тест удаления сущности")
    def test_delete_entity(self, api_client: ApiClient):
        with allure.step("Создание тестовой сущности"):
            response = api_client.create_entity()
            entity_id = response['id']

        with allure.step(f"Удаление сущности с ID: {entity_id}"):
            result = api_client.delete_entity(entity_id)

        with allure.step("Проверка успешного удаления"):
            assert result is True, "Метод удаления должен вернуть True в случае успеха"
