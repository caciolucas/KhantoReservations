from decimal import Decimal
import uuid
from django.test import TestCase
from properties.models import Property, Announcement


class PropertyTestCase(TestCase):
    def setUp(self):
        self.property1 = Property.objects.create(
            code="TEST01",
            max_guests=2,
            n_bathrooms=1,
            is_pet_friendly=True,
            clean_price="200.00",
            activation_date="2020-01-01",
        )
        self.property2 = Property.objects.create(
            code="TEST02",
            max_guests=5,
            n_bathrooms=2,
            is_pet_friendly=False,
            clean_price="50.00",
            activation_date="2023-01-01",
        )

    def test_add_property(self):
        response = self.client.get("/api/v1/properties/properties/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

        property3_data = {
            "code": "TEST03",
            "max_guests": 3,
            "n_bathrooms": 1,
            "is_pet_friendly": True,
            "clean_price": "100.00",
            "activation_date": "01-12-2022",
        }
        response = self.client.post("/api/v1/properties/properties/", property3_data)
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v1/properties/properties/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(response.data["results"][2]["code"], "TEST03")

    def test_remove_property(self):
        response = self.client.get("/api/v1/properties/properties/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

        response = self.client.delete(
            f"/api/v1/properties/properties/{self.property1.id}/"
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/properties/properties/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["code"], "TEST02")

    def test_max_guests_filter(self):
        response = self.client.get("/api/v1/properties/properties/?max_guests__gte=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["code"], "TEST02")

        response = self.client.get("/api/v1/properties/properties/?max_guests__lte=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["code"], "TEST01")

    def test_missing_field(self):
        property3_data = {
            "code": "TEST03",
            "max_guests": 3,
            "n_bathrooms": 1,
            "is_pet_friendly": True,
            "clean_price": "100.00",
        }
        response = self.client.post("/api/v1/properties/properties/", property3_data)
        self.assertEqual(response.status_code, 400)

    def test_partial_update(self):
        response = self.client.get(
            f"/api/v1/properties/properties/{self.property1.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], "TEST01")

        property1_data = {
            "code": "TEST01",
            "max_guests": 3,
        }
        response = self.client.patch(
            f"/api/v1/properties/properties/{self.property1.id}/",
            property1_data,
            "application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f"/api/v1/properties/properties/{self.property1.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], "TEST01")
        self.assertEqual(response.data["max_guests"], 3)

    def test_update(self):
        response = self.client.get(
            f"/api/v1/properties/properties/{self.property1.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], "TEST01")

        property1_data = {
            "code": "TEST01",
            "max_guests": 3,
            "n_bathrooms": 1,
            "is_pet_friendly": True,
            "clean_price": "100.00",
            "activation_date": "01-12-2022",
        }
        response = self.client.put(
            f"/api/v1/properties/properties/{self.property1.id}/",
            property1_data,
            "application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f"/api/v1/properties/properties/{self.property1.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], "TEST01")
        self.assertEqual(response.data["max_guests"], 3)
        self.assertEqual(response.data["clean_price"], "100.00")
        self.assertEqual(response.data["activation_date"], "01/12/2022")


class AnnouncementsTestCase(TestCase):
    def setUp(self):
        self.property1 = Property.objects.create(
            code="TEST01",
            max_guests=2,
            n_bathrooms=1,
            is_pet_friendly=True,
            clean_price="200.00",
            activation_date="2020-01-01",
        )
        self.property2 = Property.objects.create(
            code="TEST02",
            max_guests=5,
            n_bathrooms=2,
            is_pet_friendly=False,
            clean_price="50.00",
            activation_date="2023-01-01",
        )
        Announcement.objects.create(
            property=self.property1,
            platform=Announcement.AIRBNB,
            platform_fee="10.00",
        )
        Announcement.objects.create(
            property=self.property2,
            platform=Announcement.BOOKING,
            platform_fee="20.00",
        )

    def test_add_announcement(self):
        announcement_data = {
            "property_id": self.property1.id,
            "platform": Announcement.SEAZONE,
            "platform_fee": "20.00",
        }
        response = self.client.post(
            "/api/v1/properties/announcements/", announcement_data
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v1/properties/announcements/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(response.data["results"][2]["platform"], Announcement.BOOKING)

    def test_add_with_missing_field(self):
        announcement_data = {
            "property_id": self.property1.id,
            "platform": Announcement.SEAZONE,
        }
        response = self.client.post(
            "/api/v1/properties/announcements/", announcement_data
        )
        self.assertEqual(response.status_code, 400)

    def test_fail_remove_announcement(self):
        announcement1 = Announcement.objects.get(platform=Announcement.AIRBNB)
        response = self.client.delete(
            f"/api/v1/properties/announcements/{announcement1.id}/"
        )
        self.assertEqual(response.status_code, 405)

    def test_add_announcement_to_non_existing_property(self):
        announcement_data = {
            "property_id": "ec0faa1e-68a2-485a-a8ca-25e02f44a4e4",
            "platform": Announcement.SEAZONE,
            "platform_fee": "20.00",
        }
        response = self.client.post(
            "/api/v1/properties/announcements/", announcement_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"property_id": "Property does not exist"})

    def test_platform_filter(self):
        response = self.client.get("/api/v1/properties/announcements/?platform=airbnb")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["platform"], Announcement.AIRBNB)

        response = self.client.get("/api/v1/properties/announcements/?platform=booking")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["platform"], Announcement.BOOKING)

    def test_property_code_filter(self):
        response = self.client.get(
            "/api/v1/properties/announcements/?property__code__icontains=TEST01"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["platform"], Announcement.AIRBNB)

        response = self.client.get(
            "/api/v1/properties/announcements/?property__code__icontains=TEST02"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["platform"], Announcement.BOOKING)

    def test_partial_update(self):
        announcement1 = Announcement.objects.get(platform=Announcement.AIRBNB)
        announcement_data = {"platform_fee": "30.00"}
        response = self.client.patch(
            f"/api/v1/properties/announcements/{announcement1.id}/",
            announcement_data,
            "application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f"/api/v1/properties/announcements/{announcement1.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["platform_fee"], "30.00")

    def test_update(self):
        announcement1 = Announcement.objects.get(platform=Announcement.AIRBNB)
        announcement_data = {
            "property_id": announcement1.property.id,
            "platform": Announcement.BOOKING,
            "platform_fee": "30.00",
        }
        response = self.client.put(
            f"/api/v1/properties/announcements/{announcement1.id}/",
            announcement_data,
            "application/json",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            f"/api/v1/properties/announcements/{announcement1.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["platform"], Announcement.BOOKING)
        self.assertEqual(response.data["platform_fee"], "30.00")
