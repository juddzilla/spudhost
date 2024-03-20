from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
import json

from .models import Lists
from .serializers import (ListSerializer, ListsSerializer, ListUpdateSerializer)

from list_items.models import ListItems
from list_items.serializers import (ListItemUpdateSerializer, ListItemsSerializer)
# Create your views here.

def get_user_list(request, uuid):
    return Lists.objects.get(user=request.user.id, uuid=uuid)

def get_list_items(list):
    return list.listitems_set

class ListsView(APIView):
    def get(self, request, *args, **kwargs):        
        lists = Lists.objects.filter(user=request.user.id).exclude(deleted=True).order_by('-created_at')
        # list_items_count = get_list_items(list).all().exclude(deleted=True)
        serialized = ListsSerializer(lists, many=True)
        response = {
            'total': 100,
            'results': serialized.data
        }
        return Response(response, status=status.HTTP_200_OK)
        
        # return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def post(self, request, *args, **kwargs):
        data = {
            'uuid': uuid.uuid4(),
            'title': request.data.get('title'),
            'user': request.user.id,
        }

        serialized = ListsSerializer(data=data)

        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListView(APIView):
    def get(self, request, id, *args, **kwargs):        
        list = get_user_list(request, id)
        
        sort_direction = request.query_params.get('sortDirection')
        sort_property = request.query_params.get('sortProperty')
        search = request.query_params.get('search')
        show_completed = request.query_params.get('showCompleted')
        
        order_by = sort_property
        if sort_direction == 'desc':
            order_by = f"-{order_by}"        
        
        filter_args = {
            'deleted': False,
        }
        if search:
            filter_args['body__icontains'] = search

        if show_completed.lower() != 'null':
            filter_args['completed'] = show_completed.lower() == 'true'
        
        
        items = list.listitems_set.filter(**filter_args).order_by(order_by)
        serialized = ListSerializer(list)
        
        serialized_items = ListItemsSerializer(items, many=True)
        response = {
            **serialized.data,
            'children': serialized_items.data
        }
        return Response(response, status=status.HTTP_200_OK)
        # return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        list = get_user_list(request, id)
                
        try:
            list.delete()
            return Response(
                {'removed': True}, 
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id, *args, **kwargs):
        list = get_user_list(request, id)
        data = {            
            'body': request.data.get('body'),
            'list': list.id,
            'order': request.data.get('order'),
        }
        
        serialized = ListItemsSerializer(list, data=data, partial=True)    

        if serialized.is_valid():
            serialized.save()
            list_items = list.listitems_set.all().exclude(deleted=True)
            # serialized_list_items = ListItemsSerializer(list_items, many=True)
            # print(serialized_list_items.data)
            return Response(
                {'results': serialized.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, id, *args, **kwargs):
        data = {
            'uuid': uuid.uuid4(),
            'title': request.data.get('title'),
            'user': request.user.id,
        }

        list = get_user_list(request, id)          
        serialized = ListUpdateSerializer(list, data=data, partial=True)        

        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_200_OK)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListItemsView(APIView):
    def put(self, request, id, *args, **kwargs):
        list = get_user_list(request, id)        
        list_items_order = request.data.get('order')

        for index, item_id in enumerate(list_items_order):            
            list_item = list.listitems_set.get(list_id=list.id, id=item_id)
            list_item.order = index
            list_item.save()

        list_items = list.listitems_set.all().exclude(deleted=True)
        serialized = ListItemsSerializer(list_items, many=True)

        if serialized.is_valid():
            response = {
                'results': serialized.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ListItemView(APIView):
    def put(self, request, id, item_id, *args, **kwargs):
        list = get_user_list(request, id)
        list_item = list.listitems_set.get(id=item_id)
        serialized = ListItemUpdateSerializer(list_item, data=request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, item_id, *args, **kwargs):
        list = get_user_list(request, id)
        list_item = ListItems.objects.get(list_id=list.id, id=item_id)
        
        try:
            list_item.delete()
            return Response(
                {'removed': True}, 
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        
