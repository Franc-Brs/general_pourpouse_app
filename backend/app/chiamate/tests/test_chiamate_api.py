"""
Test for chiamate API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Chiamate
from chiamate.serializers import (
    ChiamateSerializer,
)

from datetime import datetime
import pytz


CHIAMATE_URL = reverse('chiamate:chiamate-list')


def create_chiamata(**params):
    """Helper function: create and return a sample chiamata (one row)"""
    h_now = datetime.now(
                pytz.timezone('Europe/Rome')
    ).isoformat(timespec='seconds')

    defaults = {
        'datetime_creation': f"{h_now}",
        'datetime': f"{h_now}",
        'chiamata': '<XML Sample>',
        'status': 'Sent',
        'server': 'http://localhost:8080',
        'risposta_server_terzo': '200 OK',
    }
    defaults.update(params)

    chiamata = Chiamate.objects.create(**defaults)
    return chiamata


class PublicChiamateAPITest(TestCase):
    """ Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to calla API."""
        res = self.client.get(CHIAMATE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateChiamateAPITest(TestCase):
    """Test authenticated API requests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_chiamate(self):
        """Test retrieving a list of chiamate."""
        create_chiamata()
        create_chiamata()

        res = self.client.get(CHIAMATE_URL)

        # non capisco perchè non gli va bene ordinato
        recipes = Chiamate.objects.all().order_by('id')
        serializer = ChiamateSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)
