

from datetime import datetime
from django.conf import settings
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'org_backend.settings')
import sys 

print(sys.path)

settings.configure(
    DATABASE_ENGINE = 'djongo',
    DATABASE_NAME = 'orange',
    DATABASE_HOST = 'mongodb+srv://zied:zied1212001@orangecluster.rjpef.mongodb.net/orange?retryWrites=true&w=majority',
    TIME_ZONE = 'UTC',
)
from datetime import datetime
from cpe.models import Cpe 
for cpe in qs : 
    if (datetime.now() - cpe.last_update).seconds  > TIMEOUT : 
        cpe.status = False,    
        cpe.upload_debit = 0.0,
        cpe.download_debit = 0.0,
        cpe.temperature = 0.0,
        cpe.cpu_usage = 0.0,
        cpe.ram_usage = 0.0
        cpe.save()


