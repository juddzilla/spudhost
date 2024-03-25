from rest_framework import serializers
from .models import Groupings

class GroupingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupings
        fields = [
            "created_at",
            "deleted",
            "title",
            "updated_at",
            "user",
            "uuid",
        ] 

    def to_representation(self, instance):
        # Get the serialized data from the parent class
        data = super().to_representation(instance)
        
        # Add a key to the serialized data
        data['type'] = 'Collection'
        data['headline'] = instance.title

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