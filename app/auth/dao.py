from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import SuperAdmin
from app.auth.schemas import SuperAdminLogin
from app.database.dao import BaseDAO


class SuperAdminDAO(BaseDAO[SuperAdmin, SuperAdminLogin, SuperAdminLogin]):
    def __init__(self, session: AsyncSession):
        super().__init__(SuperAdmin, session)

    async def get_by_email(self, email: str) -> Optional[SuperAdmin]:
        """Get super admin by email."""
        result = await self.session.execute(select(SuperAdmin).where(SuperAdmin.email == email))
        return result.scalars().first()
