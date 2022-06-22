import os
from celery import Celery
from django.conf import settings
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'org_backend.settings')

app = Celery('org_backend')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)



@app.task(bind=True)
def cpe_checker(self):
    print("checking !!!!!!!!!!!!!!!!!")
    """
    from cpe.models import Cpe 
    TIMEOUT = 20
    qs = Cpe.objects.all()
    for cpe in qs : 
        if (datetime.now() - cpe.last_update).seconds  > TIMEOUT : 
            cpe.status = False,    
            cpe.upload_debit = 0.0,
            cpe.download_debit = 0.0,
            cpe.temperature = 0.0,
            cpe.cpu_usage = 0.0,
            cpe.ram_usage = 0.0
            cpe.save()
    """
