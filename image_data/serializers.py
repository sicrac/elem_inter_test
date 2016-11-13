from rest_framework import serializers
from image_data import models


class DataEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ImageData
        fields = '__all__'
