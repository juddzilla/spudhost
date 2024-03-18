from rest_framework import serializers
from .models import GroupingItems

class GroupingItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupingItems
        fields = [
            "created_at",
            "deleted",
            "updated_at",
            "content_type",
            "object_id",
            "content_object",
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