from multiprocessing.connection import Client
from pickle import TRUE
from django.db import models
from client.models import Client 
from account.models import Technicien

# Create your models here.

class Cpe(models.Model):
    client = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=True)
    technicien = models.ForeignKey(Technicien,on_delete=models.SET_NULL,null=True,blank=True)
    token = models.CharField(max_length=256)
    #location = models.CharField(max_length=255,default='')
    #reboot = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    upload_debit = models.FloatField(default=0.0)
    download_debit = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    cpu_usage = models.FloatField(default=0.0)
    ram_usage = models.FloatField(default=0.0)
    last_update = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"cpe of {self.id}"
