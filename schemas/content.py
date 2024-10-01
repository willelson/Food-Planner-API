from pydantic import BaseModel


class Content(BaseModel):
    title: str
    description: str
    image_url: str
    site_name: str
    source_url: str
