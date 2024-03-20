from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

from .models import Lists
from .serializers import (ListSerializer, ListsSerializer)

from list_items.models import ListItems
from list_items.serializers import (ListItemUpdateSerializer, ListItemsSerializer)
# Create your views here.

def get_user_list(request, uuid):
    return Lists.objects.get(user=request.user.id, uuid=uuid)

class ListsView(APIView):
    def get(self, request, *args, **kwargs):        
        lists = Lists.objects.filter(user=request.user.id).exclude(deleted=True).order_by('-created_at')
        serialized = ListsSerializer(lists, many=True)
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
        # print(request.query_params)
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
        
        print(22)
        print(filter_args)
        items = list.listitems_set.filter(**filter_args).order_by(order_by)
        serialized = ListSerializer(list)      
        serialized_items = ListItemsSerializer(items, many=True)
        response = {
            **serialized.data,
            'children': serialized_items.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request, id, *args, **kwargs):
        list = get_user_list(request, id)
        data = {            
            'body': request.data.get('body'),
            'list': list.id,
            'order': request.data.get('order'),
        }

        print(data)

        serialized = ListItemsSerializer(data=data)
        print(serialized.is_valid())
        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_201_CREATED)
            
    def put(self, request, id, *args, **kwargs):
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
    
class ListItemView(APIView):
    def put(self, request, id, item_id, *args, **kwargs):
        list = get_user_list(request, id)
        list_item = ListItems.objects.get(list_id=list.id, id=item_id)
        print(request.data)

        # data = {
        #     **list_item,
        #     **request.data,
        # }
        # print(100)
        # print(data)

        serialized = ListItemUpdateSerializer(list_item, data=request.data, partial=True)
        print(serialized.is_valid())
        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_202_ACCEPTED)
        
    def delete(self, request, id, item_id, *args, **kwargs):
        list = get_user_list(request, id)
        list_item = ListItems.objects.get(list_id=list.id, id=item_id)
        print(list_item)
        list_item.delete()
        return Response({
                'removed': True,
            }, status=status.HTTP_202_ACCEPTED)


# def change_item_order(list_item, new_order):
#     old_order = list_item.order
#     list_item.order = new_order
#     list_item.save()

#     if old_order < new_order:
#         # Move item down, so decrement order for items in between
#         ListItems.objects.filter(list=list_item.list, order__gt=old_order, order__lte=new_order).exclude(pk=list_item.pk).update(order=models.F('order') - 1)
#     elif old_order > new_order:
#         # Move item up, so increment order for items in between
#         ListItems.objects.filter(list=list_item.list, order__lt=old_order, order__gte=new_order).exclude(pk=list_item.pk).update(order=models.F('order') + 1)
