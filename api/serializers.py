from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction

from api.models import Image, Label


class LabelInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        exclude = ('image',)

    def to_internal_value(self, data):
        result_data = {
            'confirmed': data['meta']['confirmed'],
            'confidence_percent': data['meta']['confidence_percent'],
            'id': data['id'],
            'class_id': data['class_id'],
            'surface': data['surface'],
            'end_x': data['shape']['endX'],
            'end_y': data['shape']['endY'],
            'start_x': data['shape']['startX'],
            'start_y': data['shape']['startY'],
        }

        return super().to_internal_value(result_data)

    def to_representation(self, instance):
        return {
            'meta': {
                'confirmed': instance.confirmed,
                'confidence_percent': instance.confidence_percent
            },
            'id': instance.id,
            'class_id': instance.class_id,
            'surface': instance.surface,
            'shape': {
                'endX': instance.end_x,
                'endY': instance.end_y,
                'startY': instance.start_y,
                'startX': instance.start_x,
            }
        }


class LabelExternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        exclude = ('image',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'class_id': instance.class_id,
            'surface': ''.join(instance.surface),
        }


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'labels', 'uuid', )

    image = Base64ImageField(write_only=True)
    labels = LabelInternalSerializer(many=True, write_only=True, required=False)

    @transaction.atomic()
    def create(self, validated_data):
        labels = validated_data.pop('labels', [])
        image = Image.objects.create(**validated_data)

        for label in labels:
            Label.objects.create(image=image, **label)

        return image


class ImageInternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('labels',)

    labels = LabelInternalSerializer(many=True)

    @transaction.atomic()
    def update(self, instance, validated_data):
        labels = validated_data.pop('labels')

        instance.labels.all().delete()

        for label in labels:
            Label.objects.create(image=instance, **label)

        return instance


class ImageExternalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('labels',)

    labels = LabelExternalSerializer(many=True, source='confirmed_labels')
