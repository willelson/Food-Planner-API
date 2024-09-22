from pydantic import BaseModel


class Content(BaseModel):
    title: str
    description: str
    image: str
    site_name: str
    source: str
