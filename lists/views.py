from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from utils.sort_params import sort_params

from .models import Lists
from .serializers import (GetListsSerializer, ListSerializer, ListsSerializer, ListUpdateSerializer)

from list_items.models import ListItems
from list_items.serializers import (ListItemUpdateSerializer, ListItemsSerializer)

def get_user_list(request, uuid):
    return Lists.objects.get(user=request.user.id, uuid=uuid)

def get_list_items(list):
    return list.listitems_set

class ListsView(APIView):
    def get(self, request, *args, **kwargs):  
        query_params = sort_params(request.query_params)                              
        filter_args = {
            'user': request.user.id
        }

        if query_params['search'] is not None:
            filter_args['title__icontains'] = query_params['search']

        lists = Lists.objects.filter(**filter_args).exclude(deleted=True).order_by(query_params['order_by'])        
        serialized = GetListsSerializer(lists, many=True)
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
    def get(self, request, uuid, *args, **kwargs):        
        list = get_user_list(request, uuid)
        
        sort_direction = request.query_params.get('sortDirection')
        sort_property = request.query_params.get('sortProperty')
        search = request.query_params.get('search')
        show_completed = request.query_params.get('completed')
        
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

    def delete(self, request, uuid, *args, **kwargs):
        list = get_user_list(request, uuid)
                
        try:
            list.delete()
            return Response(
                {'removed': True}, 
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:            
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uuid, *args, **kwargs):
        list = get_user_list(request, uuid)
        list_items = list.listitems_set.all().exclude(deleted=True)
        data = {            
            'body': request.data.get('body'),
            'list': list.id,
            'order': list_items.count()
        }
        
        serialized = ListItemsSerializer(data=data, partial=True)    

        if serialized.is_valid():
            list.save()
            serialized.save()
            return Response(
                {'results': serialized.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, uuid, *args, **kwargs):
        data = {            
            'title': request.data.get('title'),            
        }

        list = get_user_list(request, uuid)          
        serialized = ListUpdateSerializer(list, data=data, partial=True)        

        if serialized.is_valid():
            list.save()
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_200_OK)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ListItemsView(APIView):
    def put(self, request, uuid, *args, **kwargs):
        list = get_user_list(request, uuid)        
        list_items_order = request.data.get('order')

        for index, item_id in enumerate(list_items_order):            
            list_item = list.listitems_set.get(list_id=list.id, id=item_id)
            list_item.order = index
            list_item.save()

        list_items = list.listitems_set.all().exclude(deleted=True)
        serialized = ListItemsSerializer(list_items, many=True)

        if serialized.is_valid():
            list.save()
            response = {
                'results': serialized.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ListItemView(APIView):
    def put(self, request, uuid, item_id, *args, **kwargs):
        list = get_user_list(request, uuid)
        list_item = list.listitems_set.get(id=item_id)
        serialized = ListItemUpdateSerializer(list_item, data=request.data, partial=True)

        if serialized.is_valid():
            list.save()
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_202_ACCEPTED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, uuid, item_id, *args, **kwargs):
        list = get_user_list(request, uuid)
        
        list_item = list.listitems_set.get(id=item_id)
        
        try:
            list_item.delete()
            list.save()
            return Response(
                {'removed': True}, 
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        
