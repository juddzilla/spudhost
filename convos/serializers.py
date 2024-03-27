from rest_framework import serializers
from .models import Convos

class ConvosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convos
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
        data['type'] = 'Convo'
        data['headline'] = instance.title
        data['subheadline'] = f"{instance.convomessages_set.count()} Messages"

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