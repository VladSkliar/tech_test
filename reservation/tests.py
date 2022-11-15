from django.test import TestCase
from rest_framework.test import APIClient
from reservation.models import Reservation
from django.urls import reverse_lazy


class ReservationTestCase(TestCase):
    fixtures = ['rentals.json', 'reservations.json']

    def setUp(self):
        self.client = APIClient()
        self.endpoints = {
            'reservation-list': reverse_lazy('v1:reservations:reservation-list'),
            'reservation-detail': lambda x: reverse_lazy(
                'v1:reservations:reservation-detail', kwargs={'pk': x}
            )
        }

    def test_initial(self):
        rentals = Reservation.objects.all()
        self.assertEqual(rentals.count(), 5)
        self.assertTrue(self.endpoints)

    def test_reservation_list(self):
        endpoint = self.endpoints.get('reservation-list')
        resp = self.client.get(endpoint)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(5, len(resp.json()))
        self.assertEqual(list, type(resp.json()))

    def test_reservation_list_filter(self):
        """
        Test filter reservations by rental id
        :return:
        """
        endpoint = self.endpoints.get('reservation-list')
        resp = self.client.get(f'{endpoint}?rental_id=1')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, len(resp.json()))
        self.assertEqual(list, type(resp.json()))

    def test_reservation_list_filter_name(self):
        """
        Test filter reservations by rental name
        :return:
        """
        endpoint = self.endpoints.get('reservation-list')
        resp = self.client.get(f'{endpoint}?rental__name=rental-2')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, len(resp.json()))
        self.assertEqual(list, type(resp.json()))

    def test_reservation_list_filter_no_results(self):
        endpoint = self.endpoints.get('reservation-list')
        resp = self.client.get(f'{endpoint}?rental__name=rental-3')
        self.assertEqual(200, resp.status_code)
        self.assertFalse(resp.json())

    def test_reservation_list_filter_bad_choices(self):
        endpoint = self.endpoints.get('reservation-list')
        resp = self.client.get(f'{endpoint}?rental_id=3')
        self.assertEqual(400, resp.status_code)

    def test_reservation_detail(self):
        """
        Get correct id from fixtures and test detail info
        :return:
        """
        endpoint = self.endpoints.get('reservation-detail')(1)
        resp = self.client.get(endpoint)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.json().get('id'))
        self.assertEqual('rental-1', resp.json().get('rental_name'))
        self.assertEqual('2022-01-01', resp.json().get('checkin'))
        self.assertEqual('2022-01-13', resp.json().get('checkout'))
        self.assertIsNone(resp.json().get('prev_reservation_id'))
        self.assertEqual(dict, type(resp.json()))

    def test_reservation_detail_with_prev_reservation(self):
        """
        Test reservation which has previous reservation
        :return:
        """
        endpoint = self.endpoints.get('reservation-detail')(2)
        resp = self.client.get(endpoint)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(2, resp.json().get('id'))
        self.assertEqual('rental-1', resp.json().get('rental_name'))
        self.assertEqual('2022-01-20', resp.json().get('checkin'))
        self.assertEqual('2022-02-10', resp.json().get('checkout'))
        self.assertEqual(1, resp.json().get('prev_reservation_id'))
        self.assertEqual(dict, type(resp.json()))

    def test_reservation_detail_fail(self):
        """
        Get wrong id and test detail info
        :return:
        """
        endpoint = self.endpoints.get('reservation-detail')(10)
        resp = self.client.get(endpoint)
        self.assertEqual(404, resp.status_code)
