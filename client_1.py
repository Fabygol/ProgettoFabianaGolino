from requests import get, post
from datetime import datetime
import time
import json

function_url = 'https://europe-west1-progetto2-407119.cloudfunctions.net/save_data'

#taxy id, data, longitudine, latitudine
with open('file/999.txt') as f:
    for riga in f:
        taxi_id = riga.split(',')[0]
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        long = float(riga.split(',')[2])
        lat = float(riga.split(',')[3])
        print({'taxi_id':taxi_id, 'dt':dt, 'long':long, 'lat':lat})

        #r = post(f'{function_url}', json={'taxi_id': taxi_id, 'dt': dt, 'long': long, 'lat': lat})
        #r = post(f'{base_url}/sensors/{taxi_id}', data={'sensor': taxi_id,'dt': dt, 'long': long, 'lat': lat})
        r = post(function_url,data={'data': json.dumps({'taxi_id': taxi_id, 'dt': dt, 'lat': lat, 'long': long})})
        print('sending', dt, lat, long, ' -----> ', r.status_code)

        time.sleep(3)



print('done')
