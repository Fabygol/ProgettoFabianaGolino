#cloud function http
def save_data(request):
    from google.cloud import firestore
    import json

    if request.method == 'OPTIONS':
        print('------ options')
        # Allows GET and POST requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    msg = json.loads(request.values['data'])
    print('--------------------------')
    print(msg)
    coll = 'sensor'
    db = firestore.Client()
    doc_ref = db.collection(coll).document(msg['taxi_id'])
    doc_ref.set({'taxi_id':msg['taxi_id'],'dt': msg['dt'], 'lat': msg['lat'], 'long': msg['long']})

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return ('ok', 200, headers)








