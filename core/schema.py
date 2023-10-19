from pydantic import BaseModel
from datetime import datetime


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str


class Experience(BaseModel):
    company: str
    position: str
    start_date: datetime
    end_date: datetime
    highlights: list[str]


class Education(BaseModel):
    institution: str
    degree: str
    start_date: datetime
    end_date: datetime


class Certification(BaseModel):
    name: str
    date: datetime


class Resume(BaseModel):
    name: str
    email: str
    phone: str
    address: Address
    summary: str
    experience: list[Experience]
    education: list[Education]
    skills: list[str]
    certifications: list[Certification]
