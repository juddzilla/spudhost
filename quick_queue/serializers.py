from rest_framework import serializers
from .models import Quick_Queue
# from list_items.models import ListItems

class QuickQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quick_Queue
        fields = [
            "created_at",
            "deleted",
            "body",
            "user",
            "uuid",
        ] 

    def to_representation(self, instance):
        # Get the serialized data from the parent class
        data = super().to_representation(instance)
        
        # Add a key to the serialized data
        data['type'] = 'Queue'
        data['headline'] = instance.body

        return data


# class QuickQueueItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lists
#         fields = [
#             "created_at",
#             "deleted",
#             "body",
#             "user",
#             "uuid",
#             "updated_at",
#         ] 

#     def to_representation(self, instance):
#         # Get the serialized data from the parent class
#         data = super().to_representation(instance)
        
#         # Add a key to the serialized data
#         data['children'] = []

#         return data
