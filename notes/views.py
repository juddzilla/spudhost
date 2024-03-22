from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
import uuid

from .models import Notes
from .serializers import (NotesSerializer, NoteUpdateSerializer)

def get_user_note(request, uuid):
    return Notes.objects.get(user=request.user.id, uuid=uuid)

# Create your views here.
class NotesView(APIView):
    def get(self, request, *args, **kwargs):
    
        sort_direction = request.query_params.get('sortDirection', 'desc')
        sort_property = request.query_params.get('sortProperty', 'updated_at')
        search = request.query_params.get('search', None)
        
        order_by = sort_property
        if sort_direction == 'desc':
            order_by = f"-{order_by}"           

        notes = Notes.objects.filter(user=request.user.id).exclude(deleted=True).order_by(order_by)

        if search is not None:
            notes = notes.filter(Q(body__icontains=search) | Q(title__icontains=search))
        
        serialized = NotesSerializer(notes, many=True)
        
        # TODO total
        response = {
            'total': 100, 
            'results': serialized.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'uuid': uuid.uuid4(),
            'title': request.data.get('title'),
            'user': request.user.id,
        }

        serialized = NotesSerializer(data=data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteView(APIView):
        def get(self, request,uuid,  *args, **kwargs):
            note = get_user_note(request, uuid)
            
            serialized = NotesSerializer(note)
            return Response({
                    **serialized.data,
                }, status=status.HTTP_200_OK)
        
        def put(self, request, uuid, *args, **kwargs):
            note = get_user_note(request, uuid)
            serialized = NoteUpdateSerializer(note, data=request.data, partial=True)

            if serialized.is_valid():                
                serialized.save()
                return Response({
                    **serialized.data,
                }, status=status.HTTP_200_OK)

            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)        
        
        def delete(self, request, uuid, *args, **kwargs):
            note = get_user_note(request, uuid)            
                    
            try:
                note.delete()
                return Response(
                    {'removed': True}, 
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:            
                return Response(e, status=status.HTTP_400_BAD_REQUEST)