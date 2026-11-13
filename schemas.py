from pydantic import BaseModel, EmailStr, Field, ConfigDict

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=18, le=60)
    email: EmailStr
    salary: float = Field(gt=0)


class EmployeeResponse(EmployeeCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)