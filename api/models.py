import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField


class Image(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now=True)

    def confirmed_labels(self):
        return self.labels.filter(confirmed=True)


class Label(models.Model):
    confirmed = models.BooleanField()
    confidence_percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    id = models.UUIDField(primary_key=True)
    class_id = models.TextField()
    surface = ArrayField(models.TextField())
    end_x = models.FloatField(validators=[MinValueValidator(0)])
    end_y = models.FloatField(validators=[MinValueValidator(0)])
    start_x = models.FloatField(validators=[MinValueValidator(0)])
    start_y = models.FloatField(validators=[MinValueValidator(0)])
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='labels')
