from requests import get, post
import time
import json
from datetime import datetime

function_url = 'https://europe-west1-progettoesamefabianagolino.cloudfunctions.net/save_data'

#taxy id, data, longitudine, latitudine
with open('file/997.txt') as f:
    for riga in f:
        taxi_id = riga.split(',')[0]
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        long = float(riga.split(',')[2])
        lat = float(riga.split(',')[3])
        print({'taxi_id':taxi_id, 'dt':dt, 'long':long, 'lat':lat})

        r = post(function_url,data={'data': json.dumps({'taxi_id': taxi_id, 'dt': dt, 'lat': lat, 'long': long})})
        print('sending', dt, lat, long, ' -----> ', r.status_code)

        time.sleep(3)



print('done')
