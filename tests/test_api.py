import allure

from api.api_client import ApiClient


@allure.epic("API Сущностей")
class TestEntityApi:

    @allure.feature("Создание Сущности")
    @allure.title("Тест успешного создания сущности")
    def test_create_entity(self, api_client: ApiClient, create_entity):
        entity_id, entity_data = create_entity

        with allure.step("Проверка получения ID сущности"):
            assert entity_id, "ID сущности не должен быть пустым"

        with allure.step("Получение и проверка созданной сущности"):
            entity = api_client.get_entity(entity_id)
            assert entity.title == entity_data['title'], "Заголовок должен соответствовать созданному"
            assert entity.verified == entity_data['verified'], "Статус проверки должен соответствовать созданному"
            assert entity.important_numbers == entity_data[
                'important_numbers'], "Массив чисел должен соответствовать созданному"

    @allure.feature("Получение Сущности")
    @allure.title("Тест получения сущности по ID")
    def test_get_entity(self, api_client: ApiClient, create_entity):
        entity_id, entity_data = create_entity

        with allure.step(f"Получение сущности по ID: {entity_id}"):
            retrieved_entity = api_client.get_entity(entity_id)

        with allure.step("Проверка соответствия данных сущности"):
            assert retrieved_entity.id == entity_id, "ID полученной сущности должен соответствовать запрошенному"
            assert retrieved_entity.title == entity_data['title'], "Заголовок должен соответствовать созданному"
            assert retrieved_entity.verified == entity_data[
                'verified'], "Статус проверки должен соответствовать созданному"
            assert retrieved_entity.important_numbers == entity_data[
                'important_numbers'], "Массив чисел должен соответствовать созданному"
            assert retrieved_entity.addition, "Сущность должна содержать блок дополнительных данных"
            assert retrieved_entity.addition.additional_info, \
                "Блок дополнительных данных должен содержать additional_info"
            assert retrieved_entity.addition.additional_number, \
                "Блок дополнительных данных должен содержать additional_number"

    @allure.feature("Получение Всех Сущностей")
    @allure.title("Тест получения всех сущностей с фильтрами")
    def test_get_all_entities(self, api_client: ApiClient, create_entities):
        entity_ids, entities_data = create_entities

        with allure.step("Получение всех сущностей"):
            all_entities = api_client.get_all_entities()

        with allure.step("Проверка получения всех сущностей"):
            entity_ids_in_response = [entity.id for entity in all_entities]
            for entity_id in entity_ids:
                assert entity_id in entity_ids_in_response, \
                    f"Созданная сущность {entity_id} должна присутствовать в списке"

        with allure.step("Получение сущностей с фильтром по заголовку"):
            target_title = entities_data[0]['title']
            filtered_by_title = api_client.get_all_entities(title=target_title)

        with allure.step("Проверка фильтрации по заголовку"):
            assert isinstance(filtered_by_title, list), "Результат должен быть списком"
            for entity in filtered_by_title:
                assert target_title in entity.title, \
                    f"Все сущности должны содержать переданный заголовок: {target_title}"

        with allure.step("Получение сущностей с фильтром по статусу проверки"):
            verified_entities = api_client.get_all_entities(verified=True)

        with allure.step("Проверка фильтрации по статусу проверки"):
            for entity in verified_entities:
                assert entity.verified is True, "Все полученные сущности должны иметь параметр verified=True"

        with allure.step("Тестирование пагинации"):
            paginated_entities = api_client.get_all_entities(page=1, per_page=2)

        with allure.step("Проверка работы пагинации"):
            assert len(paginated_entities) <= 2, "При параметре per_page=2 должно быть получено не более 2 сущностей"

    @allure.feature("Обновление Сущности")
    @allure.title("Тест обновления сущности")
    def test_update_entity(self, api_client: ApiClient, create_entity):
        entity_id, original_data = create_entity

        with allure.step(f"Обновление сущности с ID: {entity_id}"):
            updated_entity = api_client.update_entity(entity_id)

        with allure.step("Проверка корректности обновления всех полей сущности"):
            assert updated_entity.id == entity_id, "ID не должен измениться"
            assert updated_entity.title != original_data['title'], "Заголовок должен быть изменен"
            assert updated_entity.important_numbers, "Должен присутствовать массив чисел"
            assert updated_entity.addition.additional_info != original_data['addition']['additional_info'], \
                "Дополнительные данные должны быть обновлены"

    @allure.feature("Удаление Сущности")
    @allure.title("Тест удаления сущности")
    def test_delete_entity(self, api_client: ApiClient):
        response = api_client.create_entity()
        entity_id = response['id']

        with allure.step(f"Удаление сущности с ID: {entity_id}"):
            result = api_client.delete_entity(entity_id)

        with allure.step("Проверка успешного удаления"):
            assert result is True, "Метод удаления должен вернуть True в случае успеха"

        with allure.step("Проверка что сущность отсутствует в списке всех сущностей"):
            all_entities = api_client.get_all_entities()
            entity_ids = [entity.id for entity in all_entities]
            assert entity_id not in entity_ids, "Сущность должна быть удалена и отсутствовать в списке"
