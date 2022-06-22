from django.db import models

# Create your models here.
class Client(models.Model):
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=255)
    tel= models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    client_id = models.IntegerField(default=0,null=True)
    def __str__(self) -> str:
        return self.email
