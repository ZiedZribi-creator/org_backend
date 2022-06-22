
import json
from pickle import TRUE
import requests
import time
import random
import decimal
import multiprocessing



base_end_point = 'https://1154-102-157-119-127.eu.ngrok.io/api'
cpe_update_endpoint = lambda cpe_id : f"/cpe/{cpe_id}/update"
cpe_status_endpoint = lambda cpe_id : f"/cpe/{cpe_id}/status"

cpe_list = [
{'id' : 23,'token':'yczmodxojgstxavcgwqbamoizcjuvknvcwgdttqbehldiqgmtg'},
{'id' : 24,'token':'pivvsetaxoesvvozredzoctmlbowjwsejanrrqjhpuomrishsb'}
]
cpe_processes = [

]

def get_random_float(): 
    return float(round(random.uniform(1.0, 100.0), 2))

def update_cpe(cpe_id,cpe_token):
    full_cpe_update_endpoint = base_end_point + cpe_update_endpoint(cpe_id)
    headers = {'Content-Type':'application/json'}
    cpe_body = {'token':cpe_token,'status':True,
                    'upload_debit':get_random_float(),
                    'download_debit':get_random_float(),
                    'temperature':get_random_float(),
                    'cpu_usage':get_random_float(),
                    'ram_usage':get_random_float()
                    }
    r = requests.put(full_cpe_update_endpoint,data=json.dumps(cpe_body),headers=headers)
    print(cpe_id)
    print(r.json())
    while True : 

        # GET cpe status
        full_cpe_status_endpoint = base_end_point + cpe_status_endpoint(cpe_id)
        cpe_body = {'token':cpe_token}
        r = requests.get(full_cpe_status_endpoint,data=json.dumps(cpe_body),headers=headers)
        print(cpe_id)
        print(r.json())
        cpe_status = r.json()['status']

        # REBOOT cpe 
        if not cpe_status : 
            print('REBOOT the cpe')
            time.sleep(30)
            update_cpe(cpe_id,cpe_token)

        # UPDATE cpe
        cpe_body = {'token':cpe_token,'status':True,
                    'upload_debit':get_random_float(),
                    'download_debit':get_random_float(),
                    'temperature':get_random_float(),
                    'cpu_usage':get_random_float(),
                    'ram_usage':get_random_float()
                    }
        r = requests.put(full_cpe_update_endpoint,data=json.dumps(cpe_body),headers=headers)
        print(cpe_id)
        print(r.json())
        
        
        """
        cpe_body = {'token':cpe_token,'status':True,
                    'upload_debit':get_random_float(),
                    'download_debit':get_random_float(),
                    'temperature':get_random_float(),
                    'cpu_usage':get_random_float(),
                    'ram_usage':get_random_float()
                    }
        print(cpe_body)
        
        r = requests.put(full_cpe_update_endpoint,data=json.dumps(cpe_body),headers=headers)
        print(r.json())"""
        time.sleep(10)


for cpe in cpe_list : 
    cpe_proc = multiprocessing.Process(target=update_cpe, args=(cpe['id'],cpe['token'] ))
    cpe_processes.append(cpe_proc)

for cpe_proc in cpe_processes : 
    cpe_proc.start()

for cpe_proc in cpe_processes : 
    cpe_proc.join()

print('processes are completed')






