from random import randint

from django.core.management.base import BaseCommand
from django.core.files import File
from faker import Faker

from api.models import Image, Label


class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **options):
        faker = Faker()

        fake_pic = open('./fake.jpg', 'r+b')
        file = File(fake_pic)

        for image_idx in range(100):
            label_count = randint(0, 5)

            image = Image()
            image.save()

            for label_idx in range(label_count):
                label = Label(
                    confirmed=faker.boolean(),
                    confidence_percent=faker.pyfloat(min_value=0, max_value=1),
                    id=faker.uuid4(),
                    class_id=faker.bs(),
                    surface=faker.random_choices(),
                    end_x=faker.pyfloat(min_value=0, max_value=200),
                    end_y=faker.pyfloat(min_value=0, max_value=200),
                    start_x=faker.pyfloat(min_value=0, max_value=200),
                    start_y=faker.pyfloat(min_value=0, max_value=200),
                    image=image,
                )

                label.save()
                image.labels.add(label)

            image.image.save(f'{image_idx}.jpg', file)

        self.stdout.write(self.style.SUCCESS('Successfully populated!'))
