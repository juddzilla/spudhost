from rest_framework import serializers
from .models import ConvoMessages

class ConvoMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvoMessages
        fields = [
            "convo",
            "created_at",
            "body",
            "id",
            "deleted",
            "type",
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