from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
import uuid

from .models import Quick_Queue
from .serializers import (QuickQueueSerializer)

# Create your views here.
class QuickQueuesView(APIView):
    def get(self, request, *args, **kwargs):
    
        sort_direction = request.query_params.get('sortDirection', 'desc')
        sort_property = request.query_params.get('sortProperty', 'created_at')
        search = request.query_params.get('search', None)
        
        order_by = sort_property
        if sort_direction == 'desc':
            order_by = f"-{order_by}"           

        queue = Quick_Queue.objects.filter(user=request.user.id).exclude(deleted=True).order_by(order_by)

        # if search is not None:
        #     queue = queue.filter(Q(body__icontains=search) | Q(title__icontains=search))
        
        serialized = QuickQueueSerializer(queue, many=True)
        
        print(queue)
        # TODO total
        response = {
            'total': 100, 
            'results': serialized.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'uuid': uuid.uuid4(),
            'body': request.data.get('body'),
            'user': request.user.id,
        }

        serialized = QuickQueueSerializer(data=data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class QuickQueueItemView(APIView):
    def post(self, request, uuid, *args, **kwargs):
        queue = Quick_Queue.objects.get(user=request.user.id, uuid=uuid)
        # convert to something
        return Response(
                {'convert': True}, 
                status=status.HTTP_202_ACCEPTED
            )

