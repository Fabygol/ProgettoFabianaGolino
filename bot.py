#pip install python-telegram-bot v13
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from secret import bot_token
from google.cloud import firestore
import math
from datetime import datetime

db = firestore.Client.from_service_account_json('credentials.json')
coll = 'sensor'

def welcome(update, context):
    msg = '''Welcome in My <b> FabianaBot </b>
    Condividi la tua <b> posizione </b> per 
    visualizzare i 3 taxy più vicini.'''
    update.message.reply_text(msg, parse_mode='HTML')

def process_location(update, context):
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    user_location = message.location

    user = message.from_user
    print(user)
    print(f"You talk with user {user['first_name']} and his user ID: {user['id']}")

    #msg = f'Ti trovi presso lat={user_location.latitude}&lon={user_location.longitude}'
    lat_user = user_location.latitude
    long_user = user_location.longitude
    #print(msg)
    #message.reply_text(msg)

    msg = 'Lista dei 3 taxy più vicini'
    chat_id = update.message.chat.id
    print("chat id:", chat_id)
    dati = []  # lista di dizionari
    for doc in db.collection(coll).stream():
        #accedere all'entità
        entity = db.collection(coll).document(doc.id).get()
        #accedo ai singoli dati
        taxyid = entity.to_dict()['taxi_id']
        longtaxy = entity.to_dict()['long']
        lattaxy = entity.to_dict()['lat']
        dttaxy = entity.to_dict()['dt']
        #print('DATI - > ',taxyid,lattaxy,longtaxy,dttaxy)

        #controllo che i dati siano quelli di oggi
        data1 = datetime.strptime(dttaxy,'%Y-%m-%d %H:%M:%S')
        data1 = data1.strftime("%Y-%m-%d")
        #data1 = datetime.date()
        dataoggi = datetime.now()
        dataoggi = dataoggi.strftime("%Y-%m-%d")
        print(data1)
        print(dataoggi)

        if(data1 == dataoggi):

            #calcolo della distanza
            diflat = pow((lat_user-lattaxy),2)
            diflong = pow((long_user-longtaxy),2)
            dist1 = math.sqrt(diflat+diflong)*0.9996
            #dizionario
            diz_taxy = {"id": taxyid,
                        "dt" : dttaxy,
                        "long": longtaxy,
                        "lat":lattaxy,
                        "dist":dist1
                        }
            #print(diz_taxy)
            dati.append(diz_taxy)

    #ordino il dizionario
    sorted_values = sorted(dati, key=lambda x: x['dist'])

    print("Dizionario ordinato")
    for element in sorted_values:
        print(element)

    msg = "LISTA DEI 3 TAXY PIU' VICINI: \n"
    if len(sorted_values) == 0:
        msg = "Nessun taxy nelle vicinanze."
    else:
        taxy1 = str(sorted_values[0]['id'])
        dist1 = str(sorted_values[0]['dist'])
        taxy2 = str(sorted_values[1]['id'])
        dist2 = str(sorted_values[1]['dist'])
        taxy3 = str(sorted_values[2]['id'])
        dist3 = str(sorted_values[2]['dist'])
        msg = msg + 'taxy: '+ taxy1 + ' distanza -> '+ dist1 +'\n'+'taxy: '+ taxy2 + ' distanza -> '+ dist2 +'\n'+'taxy: '+ taxy3 + ' distanza -> '+ dist3 +'\n'
    print(msg)

    message.reply_text(msg)

def process_chat(update, context):
    print(context)
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    msg = 'Condividere la posizione per visualizzare i tre taxy più vicini'
    message.reply_text(msg)




def main():
   print('bot started')
   upd = Updater(bot_token, use_context=True)
   disp=upd.dispatcher #per gestire le chiamate in arrivo dal bot

   #handler -> ascoltatori di messaggi che arrivano al bot
   disp.add_handler(CommandHandler("start", welcome))
   disp.add_handler(MessageHandler(Filters.regex('^.*$'), process_chat)) #se arriva un msg di testo
   disp.add_handler(MessageHandler(Filters.location, process_location)) #se mando una posizione

   upd.start_polling()
   upd.idle()



if __name__=='__main__':
   main()

