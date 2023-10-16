import json
from collections import OrderedDict

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from ..models import Photo


class GetRequestPhotosTest(APITestCase):

    def setUp(self):

        self.photo1 = Photo.objects.create(
            title='title1', albumId=1, width=150, height=150, color='c2ca9d', url=f'photos/c2ca9d.png')

        self.photo2 = Photo.objects.create(
            title='title2', albumId=2, width=300, height=300, color='ac0048', url=f'photos/ac0048.png')

        self.photo3 = Photo.objects.create(
            title='title3', albumId=3, width=600, height=600, color='9c78fb', url=f'photos/9c78fb.png')

    def test_list_all_photos(self):

        response = self.client.get(reverse('photos-list'))

        expected = [OrderedDict([('id', self.photo1.pk), ('title', 'title1'), ('albumId', 1), ('width', 150), ('height', 150),
                                 ('color', 'c2ca9d'), ('url', 'http://testserver/media/photos/c2ca9d.png')]),
                    OrderedDict([('id', self.photo2.pk), ('title', 'title2'), ('albumId', 2), ('width', 300), ('height', 300),
                                 ('color', 'ac0048'), ('url', 'http://testserver/media/photos/ac0048.png')]),
                    OrderedDict([('id', self.photo3.pk), ('title', 'title3'), ('albumId', 3), ('width', 600), ('height', 600),
                                 ('color', '9c78fb'), ('url', 'http://testserver/media/photos/9c78fb.png')])
                    ]

        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_valid_single_photo(self):

        response = self.client.get(reverse('photos-detail', kwargs={'pk': self.photo2.pk}))

        expected = {'id': self.photo2.pk, 'title': 'title2', 'albumId': 2, 'width': 300, 'height': 300,
                    'color': 'ac0048', 'url': 'http://testserver/media/photos/ac0048.png'}

        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_invalid_single_photo(self):

        response = self.client.get(reverse('photos-detail', kwargs={'pk': 100}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostRequestPhotosTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.valid_payload = {'title': 'title1',
                              'albumId': 1,
                              'url': 'https://via.placeholder.com/150/d32776'
                              }

        self.invalid_payload_url = {'title': 'title2',
                                    'albumId': 2,
                                    'url': 'photos/c2ca9d.png'
                                    }

        self.invalid_payload_title = {'title': '',
                                      'albumId': 3,
                                      'url': 'https://via.placeholder.com/150/d32776'
                                      }

    def test_create_valid_photo(self):

        response = self.client.post(reverse('photos-list'),
                                    data=json.dumps(self.valid_payload),
                                    content_type='application/json'
                                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Photo.objects.filter(title='title1').exists())

    def test_create_invalid_url_photo(self):

        response = self.client.post(reverse('photos-list'),
                                    data=json.dumps(self.invalid_payload_url),
                                    content_type='application/json'
                                    )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_title_photo(self):

        response = self.client.post(reverse('photos-list'),
                                    data=json.dumps(self.invalid_payload_title),
                                    content_type='application/json'
                                    )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PutPatchRequestPhotosTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.photo1 = Photo.objects.create(
            title='title1', albumId=1, width=150, height=150, color='c2ca9d', url=f'photos/c2ca9d.png')

        self.photo2 = Photo.objects.create(
            title='title2', albumId=2, width=300, height=300, color='ac0048', url=f'photos/ac0048.png')

        self.valid_payload = {'title': 'title3',
                              'albumId': 3,
                              'url': 'https://via.placeholder.com/150/d32776'
                              }

        self.valid_single_payload = {'title': 'title3'}

        self.invalid_single_payload = {"albumId": 'test'}

        self.invalid_payload_url = {'title': 'title4',
                                    'albumId': 4,
                                    'url': 'photos/c2ca9d.png'
                                    }

        self.invalid_payload_lack_title = {'title': '',
                                           'albumId': 5,
                                           'url': 'https://via.placeholder.com/150/d32776'
                                           }

    def test_partial_update_valid_photo(self):

        response = self.client.patch(reverse('photos-detail', kwargs={'pk': self.photo1.pk}),
                                     data=json.dumps(self.valid_single_payload),
                                     content_type='application/json'
                                     )

        expected_title = self.valid_single_payload['title']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Photo.objects.get(pk=self.photo1.pk).title, expected_title)

    def test_partial_update_invalid_photo(self):
        response = self.client.patch(reverse('photos-detail', kwargs={'pk': self.photo2.pk}),
                                     data=json.dumps(self.invalid_single_payload),
                                     content_type='application/json'
                                     )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid_photo(self):

        response = self.client.put(reverse('photos-detail', kwargs={'pk': self.photo1.pk}),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json'
                                   )

        result_data = self.client.get(reverse('photos-detail', kwargs={'pk': self.photo1.pk}))

        expected_data = {
            'id': self.photo1.pk,
            'title': 'title3',
            'albumId': 3,
            'width': 150,
            'height': 150,
            'color': 'd32776',
            'url': "http://testserver/media/photos/d32776.png"
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result_data.data, expected_data)

    def test_update_invalid_url_photo(self):
        response = self.client.patch(reverse('photos-detail', kwargs={'pk': self.photo2.pk}),
                                     data=json.dumps(self.invalid_payload_url),
                                     content_type='application/json'
                                     )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_lack_title_photo(self):
        response = self.client.patch(reverse('photos-detail', kwargs={'pk': self.photo2.pk}),
                                     data=json.dumps(self.invalid_payload_lack_title),
                                     content_type='application/json'
                                     )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteRequestPhotosTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.photo1 = Photo.objects.create(
            title='title1', albumId=1, width=150, height=150, color='c2ca9d', url=f'photos/c2ca9d.png')

    def test_delete_valid_photo(self):

        pk = self.photo1.pk
        response = self.client.delete(reverse('photos-detail', kwargs={'pk': pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Photo.objects.filter(pk=pk).exists())

    def test_delete_invalid_photo(self):

        response = self.client.delete(reverse('photos-detail', kwargs={'pk': 100}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


