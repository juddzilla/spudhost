from rest_framework import serializers
from .models import ListItems

class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItems
        fields = [
            "id",
            "body",
            "completed",
            "created_at",
            "deleted",
            "list",
            "order",
            "updated_at",
        ] 

class ListItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItems
        fields = [            
            "id",
            "body",
            "completed",
            "deleted",
            "list",
            "order",
        ]         


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