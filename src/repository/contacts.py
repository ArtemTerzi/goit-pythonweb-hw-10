from typing import List
from datetime import date, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None,
        last_name: str | None,
        email: str | None,
    ) -> List[Contact]:
        stmt = select(Contact)

        if first_name:
            stmt = stmt.filter(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            stmt = stmt.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))

        stmt = stmt.offset(skip).limit(limit)

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def get_upcoming_birthdays(self) -> List[Contact]:
        today = date.today()
        upcoming_dates = [today + timedelta(days=i) for i in range(8)]
        target_days = [d.strftime("%m-%d") for d in upcoming_dates]

        stmt = select(Contact).filter(
            func.to_char(Contact.birthday, "MM-DD").in_(target_days)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Contact | None:
        query = select(Contact).filter_by(id=contact_id)
        result = await self.db.execute(query)
        contact = result.scalar_one_or_none()

        if not contact:
            return None

        update_data = body.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(contact, key, value)

        await self.db.commit()
        await self.db.refresh(contact)

        return contact

    async def remove_contact(self, contact_id: int):
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_contact_by_email(self, email: str):
        stmt = select(Contact).filter_by(email=email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
