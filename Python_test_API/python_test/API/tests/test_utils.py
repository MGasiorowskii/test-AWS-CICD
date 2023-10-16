import os
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from ..utils import save_photos


def mocked_import_data_from_api():
    mocked_data = [
        {
            "albumId": 73,
            "id": 3650,
            "title": "libero quo quae ut fugit",
            "url": "https://via.placeholder.com/600/711574",
            "thumbnailUrl": "https://via.placeholder.com/150/711574"
        },
        {
            "albumId": 74,
            "id": 3651,
            "title": "at odit iusto qui exercitationem et temporibus",
            "url": "https://via.placeholder.com/600/fc59b1",
            "thumbnailUrl": "https://via.placeholder.com/150/fc59b1"
        },
    ]

    save_photos(mocked_data)


class ImportPhotosJsonTest(APITestCase):

    def setUp(self):

        self.client = APIClient()

    @patch('API.utils.JSON_FILE_NAME', './API/tests/test_data.json')
    def test_import_valid_data_from_file(self):

        response = self.client.get(reverse('photos-import-json'))

        response_after_import = self.client.get(reverse('photos-list'),
                                                content_type='application/json')
        expected_data = [
            {
                "id": 3,
                "title": "in voluptate sit officia non nesciunt quis",
                "albumId": 100,
                "width": 600,
                "height": 600,
                "color": "1b9d08",
                "url": "http://testserver/media/photos/1b9d08.png"
            },
            {
                "id": 4,
                "title": "error quasi sunt cupiditate voluptate ea odit beatae",
                "albumId": 100,
                "width": 600,
                "height": 600,
                "color": "6dd9cb",
                "url": "http://testserver/media/photos/6dd9cb.png"
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_after_import.data, expected_data)


class ImportPhotosApiTest(APITestCase):

    def setUp(self):

        self.client = APIClient()

    @patch('API.views.import_data_from_api', mocked_import_data_from_api)
    def test_import_valid_data_from_file(self):

        response = self.client.get(reverse('photos-import-api'))

        response_after_import = self.client.get(reverse('photos-list'),
                                                content_type='application/json')

        expected_data = [
            {
                "id": 1,
                "title": "libero quo quae ut fugit",
                "albumId": 73,
                "width": 600,
                "height": 600,
                "color": "711574",
                "url": "http://testserver/media/photos/711574.png"
            },
            {
                "id": 2,
                "title": "at odit iusto qui exercitationem et temporibus",
                "albumId": 74,
                "width": 600,
                "height": 600,
                "color": "fc59b1",
                "url": "http://testserver/media/photos/fc59b1.png"
            }
        ]

        self.assertTrue(os.path.exists('./media/photos/711574.png'))
        self.assertTrue(os.path.exists('./media/photos/fc59b1.png'))
        self.assertEqual(response_after_import.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




