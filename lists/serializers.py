from rest_framework import serializers
from .models import Lists
# from list_items.models import ListItems

class ListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lists
        fields = [
            "created_at",
            "deleted",
            "title",
            "user",
            "uuid",
            "updated_at",
        ] 

    def to_representation(self, instance):
        # Get the serialized data from the parent class
        data = super().to_representation(instance)
        
        # Add a key to the serialized data
        data['type'] = 'List'

        return data


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lists
        fields = [
            "created_at",
            "deleted",
            "title",
            "user",
            "uuid",
            "updated_at",
        ] 

    def to_representation(self, instance):
        # Get the serialized data from the parent class
        data = super().to_representation(instance)
        
        # Add a key to the serialized data
        data['children'] = []

        return data


# class CompletionPublicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Completions
#         fields = (
#             "created_at",
#             "message",
#             "model",
#         )
    
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)

#         representation['created_at'] = instance.created_at.strftime("%A %B %d, %Y %l:%M %p")

#         return representation