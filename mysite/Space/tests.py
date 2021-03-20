from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from Space.models import Satelite
from rest_framework.test import APIClient

SATELITE_URLS = {
    'create': reverse('space_list'),
    'list': reverse('space_list'),
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
            If a satelite is not created successfully then
            an exception is raised, otherwise the satelite
            is created in the database
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
            If a satelite is not created successfully then
            an exception is raised, otherwise the satelite
            is created in the database
        """
        satelite = {
            'name': "Arsat",
            'latitude': 23.5485,
            'longitude': 33.5944
        }
        response = self.client.post(SATELITE_URLS['create'], satelite)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)