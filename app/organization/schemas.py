from pydantic import BaseModel, EmailStr, constr


class OrgCreate(BaseModel):
    organization_name: constr(min_length=3, max_length=50)  # type: ignore
    email: EmailStr
    password: constr(min_length=8)  # type: ignore


class OrgRetrieve(BaseModel):
    organization_name: str
    db_url: str
    admin_email: str

    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
