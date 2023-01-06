from django.test import TestCase
from reservations.models import Reservation
from properties.models import Property, Announcement

# Create your tests here.


class AnnouncementsTestCase(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            code="TEST",
            max_guests=4,
            n_bathrooms=2,
            is_pet_friendly=True,
            clean_price="100.00",
            activation_date="2023-01-01",
        )
        self.announcement = Announcement.objects.create(
            property=self.property,
            platform=Announcement.SEAZONE,
            platform_fee="10.00",
        )
        self.reservation1 = Reservation.objects.create(
            announcement=self.announcement,
            checkin_date="2023-01-01",
            checkout_date="2023-01-02",
            total_price="100.00",
            n_guests=2,
        )
        self.reservation2 = Reservation.objects.create(
            announcement=self.announcement,
            checkin_date="2023-01-02",
            checkout_date="2023-01-03",
            total_price="100.00",
            n_guests=4,
        )

    def test_add_reservation(self):
        response = self.client.get("/api/v1/reservations/reservations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

        reservation3_data = {
            "announcement_id": self.announcement.id,
            "checkin_date": "03/01/2023",
            "checkout_date": "04/01/2023",
            "total_price": "100.00",
            "n_guests": 4,
        }

        response = self.client.post(
            "/api/v1/reservations/reservations/", reservation3_data
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v1/reservations/reservations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)

    def test_remove_reservation(self):
        response = self.client.get("/api/v1/reservations/reservations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

        response = self.client.delete(
            f"/api/v1/reservations/reservations/{self.reservation1.id}/"
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/reservations/reservations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_add_with_more_guests_than_maximum(self):
        reservation3_data = {
            "announcement_id": self.announcement.id,
            "checkin_date": "03/01/2023",
            "checkout_date": "04/01/2023",
            "total_price": "100.00",
            "n_guests": 5,
        }

        response = self.client.post(
            "/api/v1/reservations/reservations/", reservation3_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data["n_guests"][0]), "Number of guests exceeds maximum"
        )

    def test_add_with_checkin_after_checkout(self):
        reservation3_data = {
            "announcement_id": self.announcement.id,
            "checkin_date": "03/01/2023",
            "checkout_date": "02/01/2023",
            "total_price": "100.00",
            "n_guests": 2,
        }

        response = self.client.post(
            "/api/v1/reservations/reservations/", reservation3_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data["checkin_date"][0]),
            "Checkin date must be before checkout date",
        )

    def test_fail_update_reservation(self):
        response = self.client.get("/api/v1/reservations/reservations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

        response = self.client.patch(
            f"/api/v1/reservations/reservations/{self.reservation1}/",
            {"n_guests": 5},
        )
        self.assertEqual(response.status_code, 405)
