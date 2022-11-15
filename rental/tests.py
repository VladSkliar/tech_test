from django.test import TestCase
from rest_framework.test import APIClient
from rental.models import Rental
from django.urls import reverse_lazy


class RentalTestCase(TestCase):
    fixtures = ['rentals.json']

    def setUp(self):
        self.client = APIClient()
        self.endpoints = {
            'rental-list': reverse_lazy('v1:rentals:rental-list'),
            'rental-detail': lambda x: reverse_lazy(
                'v1:rentals:rental-detail', kwargs={'pk': x}
            )
        }

    def test_initial(self):
        rentals = Rental.objects.all()
        self.assertEqual(rentals.count(), 2)
        self.assertTrue(self.endpoints)

    def test_rentals_list(self):
        endpoint = self.endpoints.get('rental-list')
        resp = self.client.get(endpoint)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, len(resp.json()))
        self.assertEqual(list, type(resp.json()))

    def test_rental_detail(self):
        """
        Get correct id from fixtures and test detail info
        :return:
        """
        endpoint = self.endpoints.get('rental-detail')(1)
        resp = self.client.get(endpoint)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.json().get('id'))
        self.assertEqual('rental-1', resp.json().get('name'))
        self.assertEqual(dict, type(resp.json()))

    def test_rental_detail_fail(self):
        """
        Get wrong id and test detail info
        :return:
        """
        endpoint = self.endpoints.get('rental-detail')(10)
        resp = self.client.get(endpoint)
        self.assertEqual(404, resp.status_code)