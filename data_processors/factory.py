import os
from urllib.parse import urlparse

import requests
from linkpreview import link_preview

from schemas.content import Content as ContentSchema


def scrape_with_api_service(url) -> ContentSchema:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Linkpreview-Api-Key": os.environ["LINK_PREVIEW_API_KEY"],
    }

    url = f"https://api.linkpreview.net?q={url}"
    resp = requests.get(url, headers=headers)

    parsed_uri = urlparse(url)
    hostname = parsed_uri.netloc

    data = resp.json()
    data["site_name"]: hostname
    return data


def instagram_processor(url) -> ContentSchema:
    preview = link_preview(url)

    def no_data_returned(data):
        return data.title == "Instagram" and data.image.startswith("data:image/")

    data = preview.generic

    if no_data_returned(data):
        data = scrape_with_api_service(url)

    return {
        "title": data["title"],
        "description": data["description"],
        "image_url": data["image"],
        "site_name": "www.instagram.com",
        "source_url": url,
    }


def generic_processor(url) -> ContentSchema:
    preview = link_preview(url)

    data = preview.generic

    return {
        "title": data.title,
        "description": data.description,
        "image_url": data.image,
        "site_name": data.site_name,
        "source_url": url,
    }


def data_processor(url):
    parsed_uri = urlparse(url)
    processors = {"www.instagram.com": instagram_processor}

    hostname = parsed_uri.netloc
    if hostname in processors.keys():
        processor = processors[hostname]
    else:
        processor = generic_processor

    return processor(url)
