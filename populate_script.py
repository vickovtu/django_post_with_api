import random

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
django.setup()

from faker import Faker
from post.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


def create_post(N):
    fake = Faker()
    for _ in range(4):
        User.objects.create_user(username=fake.name(), password='testpass123', email=fake.email())

    for _ in range(N):
        title = fake.name()
        status = random.choice(['published', 'draft'])

        Post.objects.create(
            title=f"{title} POST!!!",
            author=User.objects.get(id=random.randint(1, 4)),
            slug='-'.join(title.lower().split()),
            body=fake.text(),
            status=status,
            created=timezone.now(),
            update=timezone.now(),
        )


create_post(10)
print("DATA IS POPULATED SUCCESSFULLY. ")
