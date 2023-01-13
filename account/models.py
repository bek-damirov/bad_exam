from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fullname = models.CharField(max_length=20)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    register = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.register}'
