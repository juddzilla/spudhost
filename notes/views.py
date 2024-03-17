from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

# Create your views here.
class NotesView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"success": 100}, status=status.HTTP_200_OK)
