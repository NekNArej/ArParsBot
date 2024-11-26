
import json,os

# Создание дампа
# {clinet_username:[donor_link, main_link]}
def clients(chat_id:int, link: str):
    if not os.path.exists('clients'):
        file=open('clients','w')
    with open('clients','r') as file:
        clients=file.read()
        try:
            clients=json.loads(clients)
        except Exception:
            clients={}
        if str(chat_id) in clients and len(clients.get(str(chat_id)))<2:
            links=clients.get(str(chat_id))
            links.append(link)
            clients[str(chat_id)]=links
        else:
            clients[str(chat_id)]=[link]
            # print(clients)
        clients=json.dumps(clients)
    with open('clients','r+') as file:
        file.write(clients)


def user_database(chat_id: int, username: str):
    if not os.path.exists('user_database'):
        file=open('user_database','w')
    with open('user_database','r') as file:

        database=file.read()
        try:
            database=json.loads(database)
        except Exception:
            database={}
        if f'{chat_id}' in database:
            print("Пользователь уже в базе")
        else:
            database[chat_id]=username
        database=json.dumps(database)
    with open('user_database','r+') as file:
        file.write(database)





