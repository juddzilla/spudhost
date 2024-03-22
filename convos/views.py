import json
import uuid

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import Convos
from convo_messages.models import ConvoMessages
from convo_messages.serializers import ConvoMessageSerializer
from .serializers import (ConvosSerializer)

def get_user_convo(request, uuid):
    return Convos.objects.get(user=request.user.id, uuid=uuid)

class ConvosView(APIView):
    def get(self, request, *args, **kwargs):
    
        sort_direction = request.query_params.get('sortDirection', 'desc')
        sort_property = request.query_params.get('sortProperty', 'updated_at')
        search = request.query_params.get('search', None)
        
        order_by = sort_property
        if sort_direction == 'desc':
            order_by = f"-{order_by}"           

        convos = Convos.objects.filter(user=request.user.id).exclude(deleted=True).order_by(order_by)

        if search is not None:
            convos = convos.filter(title__icontains=search)
        
        serialized = ConvosSerializer(convos, many=True)
        
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

        serialized = ConvosSerializer(data=data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ConvoView(APIView):
        def get(self, request,uuid,  *args, **kwargs):
            convo = get_user_convo(request, uuid)
            messages = convo.convomessages_set.all()
            
            serialized = ConvosSerializer(convo)
            serialized_messages = ConvoMessageSerializer(messages, many=True)

            response = {
                **serialized.data,
                'messages': serialized_messages.data
            }
            
            return Response(response, status=status.HTTP_200_OK)
        
        def post(self, request,uuid,  *args, **kwargs):
            convo = get_user_convo(request, uuid)
            
            data = {
                'body': request.data.get('body'),
                'convo': convo.id,
                'deleted': False,
                'type': 'user',
                'user': request.user.id,
            }

            serialized = ConvoMessageSerializer(data=data, partial=True)

            if serialized.is_valid():
                serialized.save()
                return Response({
                    **serialized.data,
                }, status=status.HTTP_200_OK)

            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)      

            # ConvoMessages
        def put(self, request, uuid, *args, **kwargs):
            convo = get_user_convo(request, uuid)
            serialized = ConvosSerializer(convo, data=request.data, partial=True)

            if serialized.is_valid():                
                serialized.save()
                return Response({
                    **serialized.data,
                }, status=status.HTTP_200_OK)

            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)        
        
        def delete(self, request, uuid, *args, **kwargs):
            convo = get_user_convo(request, uuid)    
            
            try:
                convo.delete()
                return Response(
                    {'removed': True}, 
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:                      
                return Response(
                    json.dumps({
                        'error_type': 'TypeError',
                        'error_message': str(e),
                        # You can include additional information if needed
                    }),
                    status=status.HTTP_400_BAD_REQUEST
                )