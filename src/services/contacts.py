from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.repository.contacts import ContactRepository
from src.schemas import ContactModel, ContactUpdate, User


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
        user: User,
    ):
        return await self.repository.get_contacts(
            skip, limit, first_name, last_name, email, user
        )

    async def get_contact(self, contact_id: int, user: User):
        return await self.repository.get_contact_by_id(contact_id, user)

    async def get_upcoming_birthdays(self, user: User):
        return await self.repository.get_upcoming_birthdays(user)

    async def create_contact(self, body: ContactModel, user: User):
        existing_contact = await self.repository.get_contact_by_email(body.email, user)

        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A contact with this email already exists.",
            )

        return await self.repository.create_contact(body, user)

    async def update_contact(self, contact_id: int, body: ContactUpdate, user: User):
        existing_contact = await self.repository.get_contact_by_email(body.email, user)

        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A contact with this email already exists.",
            )

        return await self.repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        return await self.repository.remove_contact(contact_id, user)
