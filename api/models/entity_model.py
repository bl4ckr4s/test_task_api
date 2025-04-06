from pydantic import BaseModel


class AdditionData(BaseModel):
    additional_info: str
    additional_number: int


class AdditionResponse(AdditionData):
    id: int


class EntityRequest(BaseModel):
    """Model representing the request body for entity creation/update"""
    title: str
    verified: bool
    important_numbers: list[int]
    addition: AdditionData


class EntityResponse(BaseModel):
    id: int
    title: str
    verified: bool
    important_numbers: list[int]
    addition: AdditionResponse






