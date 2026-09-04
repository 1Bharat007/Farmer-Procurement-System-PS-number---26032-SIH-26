from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class QueueRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Real-time Queue endpoint ready",
            "module": "queue"
        }, status=status.HTTP_200_OK)
