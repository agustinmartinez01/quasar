from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from Space.models import Satelite
from rest_framework.test import APIClient

SATELITE_URLS = {
    'create': reverse('space_list'),
    'list': reverse('space_list'),

}
TOPSECRET_URLS = {
    'post': reverse('topsecret')
}
TOPSECRET_SPLITS_URLS = {
    'post' : reverse('topsecret_post')
}
class SateliteApiTest(TestCase):
    """TaskApiTest

    Test cases for Task object
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_satelite_notsuccessful(self):
        """Create a Satelite successfully.

        Returns:

            If the satellite is not successfully created then status 400
        """
        satelite = {
            'latitude': 23.5485,
            'longitude': 23.5485
        }
        response = self.client.post(SATELITE_URLS['create'], satelite)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_satelite_successful(self):
        """Create a Satelite successfully.

            Returns:

            If the satellite was successfully created then status 200
        """
        satelite = {
            'name': "Arsat",
            'latitude': 23.5485,
            'longitude': 33.5944
        }
        response = self.client.post(SATELITE_URLS['create'], satelite)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_top_secret_fails(self):
        """Create a Satelite successfully.

            Returns: A new secret message is sent, which cannot be decrypted then status 404
        """
        satelite = {
            'name': "Arsat",
            'latitude': -500,
            'longitude': -200
        }
        satelite1 = {
            'name': "Arsat1",
            'latitude': 100,
            'longitude': -100
        }
        satelite2 = {
            'name': "Arsat2",
            'latitude': 500,
            'longitude': 100
        }
        data = {
            "satelites":[
                {
                 "name":"Arsat",
                 "message":["", "", "", "", "mensaje", ""],
                 "distance": 100.0
                },
                {
                "name":"Arsat1",
                "message":["", "", "un", "", "secreto"],
                "distance": 115.5
                },
                {
                "name":"Arsat2",
                "message":[ "", "", "", "mensaje"],
                "distance":142.7

                }
            ]

        }
        self.client.post(SATELITE_URLS['create'], satelite)
        self.client.post(SATELITE_URLS['create'], satelite1)
        self.client.post(SATELITE_URLS['create'], satelite2)
        response = self.client.post(TOPSECRET_URLS['post'], data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_top_secret_successful(self):
        """Create a Satelite successfully.

            Returns: A new secret message is sent, which could be deciphered then status 200
        """

        satelite = {
            'name': "Arsat",
            'latitude': -500,
            'longitude': -200
        }
        satelite1 = {
            'name': "Arsat1",
            'latitude': 100,
            'longitude': -100
        }
        satelite2 = {
            'name': "Arsat2",
            'latitude': 500,
            'longitude': 100
        }
        data = {
            "satelites":[
                {
                 "name":"Arsat",
                 "message":["", "este", "", "", "mensaje", ""],
                 "distance": 100.0
                },
                {
                "name":"Arsat1",
                "message":["este", "", "un", "mensaje", "secreto"],
                "distance": 115.5
                },
                {
                "name":"Arsat2",
                "message":[ "", "es", "", "mensaje"],
                "distance":142.7

                }
            ]

        }
        self.client.post(SATELITE_URLS['create'], satelite)
        self.client.post(SATELITE_URLS['create'], satelite1)
        self.client.post(SATELITE_URLS['create'], satelite2)
        response = self.client.post(TOPSECRET_URLS['post'], data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_secret_split_fails(self):
        """Create a Satelite successfully.

           Returns: You want to update the satellite but information is missing then status 404
       """
        data_succes = {
            'name': "Arsat",
            'latitude': 23.5485,
            'longitude': 33.5944
        }
        data_fails = {
                    "name": "Arsat",
                    "distance": 100.0
                }
        self.client.post(SATELITE_URLS['create'], data_succes)
        response = self.client.post(TOPSECRET_SPLITS_URLS['post'], data_fails, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_top_secret_split_successful(self):
        """Create a Satelite successfully.

                  Returns: You want to update the satellite successfully then status 200
              """
        satelite = {
            'name': "Arsat",
            'latitude': 23.5485,
            'longitude': 33.5944
        }
        data_succes = {
                    "name": "Arsat",
                    "message": ["", "este", "", "", "mensaje", ""],
                    "distance": 100.0
                }
        self.client.post(SATELITE_URLS['create'], satelite)
        response = self.client.post(TOPSECRET_SPLITS_URLS['post'], data_succes, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)