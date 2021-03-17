from pydantic import BaseModel


class ClassificationResponse(BaseModel):
    success: bool = False
    msg: str = ""
    predicted_class: str = ""


class MLModel(BaseModel):
    type: str  # Or enum
    filename: str
    name: str  # key
