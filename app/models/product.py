from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Annotated
from bson import ObjectId
from datetime import datetime
from pydantic.json_schema import GetJsonSchemaHandler
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetJsonSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate(value: str) -> str:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return str(value)

        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        populate_by_name=True,  
        arbitrary_types_allowed=True,
    )