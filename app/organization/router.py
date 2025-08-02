from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_super_admin
from app.auth.schemas import TokenData
from app.database.session import get_session
from app.organization.schemas import AdminLogin, OrgCreate, OrgRetrieve, Token
from app.organization.services import OrganizationService

router = APIRouter()


async def get_org_service(session: AsyncSession = Depends(get_session)) -> OrganizationService:
    return OrganizationService(session)


@router.post("/org/create", response_model=OrgRetrieve)
async def create_org(
    payload: OrgCreate,
    current_user: TokenData = Depends(get_super_admin),  # Requires super admin
    service: OrganizationService = Depends(get_org_service),
):
    """Create a new organization with its own database. Only super admin can perform this action."""
    org = await service.create_organization(payload)
    return OrgRetrieve(organization_name=org.name, db_url=org.db_url, admin_email=org.admin_email)


@router.get("/org/get", response_model=OrgRetrieve)
async def get_org(organization_name: str, service: OrganizationService = Depends(get_org_service)):
    """Get organization details by name."""
    org = await service.get_organization(organization_name)
    return OrgRetrieve(organization_name=org.name, db_url=org.db_url, admin_email=org.admin_email)


@router.post("/admin/login", response_model=Token)
async def admin_login(payload: AdminLogin, service: OrganizationService = Depends(get_org_service)):
    """Login for organization admin."""
    return await service.admin_login(payload)
