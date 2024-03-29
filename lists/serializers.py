from rest_framework import serializers
from .models import Lists
from list_items.models import ListItems
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
        
        data['headline'] = instance.title
        data['subheadline'] = "0 Items"

        return data

class GetListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lists
        fields = [
            "title",            
            "uuid",
            "updated_at",
        ] 

    def to_representation(self, instance):
        # Get the serialized data from the parent class
        data = super().to_representation(instance)
        
        # Add a key to the serialized data
        data['type'] = 'List'
        
        data['headline'] = instance.title
        data['subheadline'] = f"{instance.listitems_set.exclude(deleted=True).count()} Items"

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


class ListUpdateSerializer(serializers.ModelSerializer):
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