import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


from .models import Groupings
from .serializers import GroupingsSerializer

# Create your views here.

def get_user_grouping(request, uuid):
    return Groupings.objects.get(user=request.user.id, uuid=uuid)

def get_grouping_items(grouping):
    return grouping.groupingitems_set.exclude(deleted=True)

class GroupingsView(APIView):
    def get(self, request, *args, **kwargs):
        groupings = Groupings.objects.filter(user=request.user.id).exclude(deleted=True)
        serialized = GroupingsSerializer(groupings, many=True)
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

        serialized = GroupingsSerializer(data=data)

        if serialized.is_valid():
            serialized.save()
            return Response({
                **serialized.data,
            }, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)



class GroupingView(APIView):
        def delete(self, request, uuid, *args, **kwargs):
            grouping = get_user_grouping(request, uuid)            
                
            try:
                grouping.delete()
                return Response(
                    {'removed': True}, 
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:            
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

    
        def get(self, request, uuid, *args, **kwargs):        
            grouping = get_user_grouping(request, uuid)                    
        
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
            
            items = grouping.groupingitems_set.filter(**filter_args).order_by(order_by)
            serialized = GroupingsSerializer(list)
            
            serialized_items = GroupingsSerializer(items, many=True)
            response = {
                **serialized_items.data
            }
            return Response(response, status=status.HTTP_200_OK)
            # return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
        def post(self, request, uuid, *args, **kwargs):        
            return Response({"success": 100}, status=status.HTTP_200_OK)
        
        def put(self, request, uuid, *args, **kwargs):        
            return Response({"success": 100}, status=status.HTTP_200_OK)