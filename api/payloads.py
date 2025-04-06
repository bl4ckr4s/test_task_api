from faker import Faker

from api.models.entity_model import AdditionData, EntityRequest


fake = Faker()


class Payloads:

    @property
    def create(self) -> dict[str, object]:
        """Generate create entity payload using EntityRequest model"""
        addition_data = AdditionData(
            additional_info=fake.sentence(),
            additional_number=fake.random_int(min=100, max=999)
        )

        entity = EntityRequest(
            title=fake.catch_phrase(),
            verified=fake.boolean(),
            important_numbers=[
                fake.random_int(min=1, max=100),
                fake.random_int(min=1, max=100),
                fake.random_int(min=1, max=100)
            ],
            addition=addition_data
        )

        return entity.model_dump(exclude_none=True)
