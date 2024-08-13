from pydantic import BaseModel

class URLCreate(BaseModel):
    original_url: str

class URLInfo(BaseModel):
    original_url: str
    short_code: str

    class Config:
        orm_mode = True
