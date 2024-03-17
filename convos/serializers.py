from rest_framework import serializers
from .models import Convos

class ConvosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convos
        fields = [
            "ai_created_at",
            "ai_id",
            "completion_tokens",
            "created_at",
            "message",
            "messages",            
            "model",
            "prompt_tokens",
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