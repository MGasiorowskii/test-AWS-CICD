import requests
import json
from PIL import Image
from io import BytesIO
from .models import Photo


URL = "https://jsonplaceholder.typicode.com/photos"
JSON_FILE_NAME = './data.json'


def import_data_from_api() -> None:
    """Function import photos from external API at https://jsonplaceholder.typicode.com/photos"""

    response = requests.get(url=URL)
    data = response.json()

    save_photos(data)


def import_data_from_file() -> None:
    """Function import photos from JSON file - data.json"""

    with open(JSON_FILE_NAME) as json_file:
        data = json.load(json_file)

    save_photos(data)


def update_photo(data: dict, pk: int) -> None:
    """Function update an object from database with following arguments"""

    for photo in data:
        album_id = photo['albumId']
        title = photo['title']
        image_url = photo['url']
        dominant_color = image_url.split("/")[-1]

        image_width, image_height = download_photo(image_url, dominant_color)

        Photo.objects.filter(pk=pk).update(title=title,
                                           albumId=album_id,
                                           width=image_width,
                                           height=image_height,
                                           color=dominant_color,
                                           url=f'photos/{ dominant_color}.png')


def download_photo(image_url: str, dominant_color: str) -> [int, int]:
    """Function download and save photo from following URL"""

    file_name = dominant_color + ".png"
    img_from_url = requests.get(image_url + ".png")

    img = Image.open(BytesIO(img_from_url.content))
    image_width = img.width
    image_height = img.height

    img.save(f"./media/photos/{file_name}")

    return image_width, image_height


def save_photos(data: dict) -> None:
    """Function save photos from following JSON data"""

    for photo in data:
        album_id = photo['albumId']
        title = photo['title']
        image_url = photo['url']
        dominant_color = image_url.split("/")[-1]

        if not Photo.objects.filter(title=title).exists():
            image_width, image_height = download_photo(image_url, dominant_color)

            Photo.objects.create(title=title,
                                 albumId=album_id,
                                 width=image_width,
                                 height=image_height,
                                 color=dominant_color,
                                 url=f'photos/{ dominant_color}.png')

