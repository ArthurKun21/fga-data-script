from pydantic import BaseModel, Field, TypeAdapter, field_serializer


class ServantData(BaseModel):
    name: str
    idNumber: int = Field(alias="collectionNo")

    @field_serializer("idNumber")
    def serialized_id(self, v) -> str:
        return f"{v:05}"


servant_data_list = TypeAdapter(list[ServantData])
