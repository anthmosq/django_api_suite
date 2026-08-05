from datetime import datetime

from django.shortcuts import render
from firebase_admin import db
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_items"

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get() or {}
        return Response(
            {
                "name": self.name,
                "collection_name": self.collection_name,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        payload = request.data.get("payload", {})
        generated_text = self._generate_text(payload)
        ref = db.reference(self.collection_name).push(
            {
                "payload": payload,
                "generated_text": generated_text,
                "created_at": datetime.utcnow().isoformat() + "Z",
            }
        )
        return Response(
            {
                "id": ref.key,
                "payload": payload,
                "generated_text": generated_text,
            },
            status=status.HTTP_201_CREATED,
        )

    def _generate_text(self, prompt):
        """Placeholder para un cliente de IAG generativa."""
        return f"Generative response for prompt: {prompt}"
