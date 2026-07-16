from pydantic import BaseModel, Field


class ExampleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class ExampleRead(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
