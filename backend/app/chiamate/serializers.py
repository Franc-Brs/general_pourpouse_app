"""
Serializers for chiamate API.
"""
from rest_framework import serializers

from core.models import Chiamate


class ChiamateSerializer(serializers.ModelSerializer):
    """Serializer for chiamate."""

    class Meta:
        model = Chiamate
        fields = [
            'id',
            'datetime_creation',
            'datetime',
            'chiamata',
            'status',
            'server',
            'risposta_server_terzo'
        ]

        read_only_fields = ['id']
