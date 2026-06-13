from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=50)
    phone_number: str = Field(..., max_length=20)
    birthday: date
    description: str | None = Field(None, max_length=250)


class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContactUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=2, max_length=50)
    last_name: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = Field(None, max_length=50)
    phone_number: str | None = Field(None, max_length=20)
    birthday: date | None = None
    description: str | None = Field(None, max_length=250)
