from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.repository.contacts import ContactRepository
from src.schemas import ContactModel, ContactUpdate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
    ):
        return await self.repository.get_contacts(
            skip, limit, first_name, last_name, email
        )

    async def get_contact(self, contact_id: int):
        return await self.repository.get_contact_by_id(contact_id)

    async def get_upcoming_birthdays(self):
        return await self.repository.get_upcoming_birthdays()

    async def create_contact(self, body: ContactModel):
        existing_contact = await self.repository.get_contact_by_email(body.email)

        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A contact with this email already exists.",
            )

        return await self.repository.create_contact(body)

    async def update_contact(self, contact_id: int, body: ContactUpdate):
        existing_contact = await self.repository.get_contact_by_email(body.email)

        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A contact with this email already exists.",
            )

        return await self.repository.update_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        return await self.repository.remove_contact(contact_id)
