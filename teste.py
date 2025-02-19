from flask import Flask, jsonify
import requests

#responsabilidades da API x o que implementar aquiaa



def check_user(user_id: int) -> bool:
    url = "http://127.0.0.1:5000/users"
    response = requests.get(url)
    user_list = response.json()
    for user in user_list:
        if user['id'] == user_id:
            return True
    return False

def check_crag(crag_id: int) -> bool:
    url = "http://127.0.0.1:5000/crags"
    response = requests.get(url)
    crag_list = response.json()
    for crag in crag_list:
        if crag['id'] == crag_id:
            return True
    return False   

def add_user(username: str):
    url = "http://127.0.0.1:5000/users"
    data = {
        'username': username
    }

    response = requests.post(url, json=data)
    if response.status_code == 201:
        print('API Response: ', response.json())
    else:
        print(f'Error: {response.status_code}')
        print('Details: ', response.text)

def list_users():
    url = "http://127.0.0.1:5000/users"
    response = requests.get(url)
    user_list = response.json()
    if response.status_code == 200:
        for user in user_list:
           print(20*'-')
           print(f'|user id: {user['id']}|\n'
                 f'|username: {user['username']}|\n')
    else:
        print(f'Error: {response.status_code}')
        print('Details: ', response.text)
    

def add_route(name: str, grade: str, user_id: str,crag_id: str, type: str, description: str):
    url = "http://127.0.0.1:5000/routes"
    data = {
        'name': name,
        'grade': grade,
        'type': type,
        'crag_id': crag_id,
        'user_id': user_id,
        'description': description

    } 
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print('API Response: ', response.json())
    else:
        print(f'Error: {response.status_code}')
        print('Details: ', response.text)

def list_routes(list_all: bool, user_id: int = 0, status = ''):
    routes_list = []
    crags_list = []
    url = ''
    if list_all:
        url = "http://127.0.0.1:5000/routes"
    else:
        if status == 'sent':
            url = f"http://127.0.0.1:5000/users/{user_id}/routes?type=sent"
        elif status == 'project':
            url = f"http://127.0.0.1:5000/users/{user_id}/routes?type=project"
        else:
            url = f"http://127.0.0.1:5000/users/{user_id}/routes?type=wish"

       
    response = requests.get(url)
    routes_list = response.json()

    #faz sentido carregar os setores aqui?
    url = "http://127.0.0.1:5000/crags"
    response = requests.get(url)
    crags_list = response.json()
    
    

    if routes_list:
        for route in routes_list:
           print(20*'-')
           print(f'|name: {route['name']}|\n'
                 f'|grade: {route['grade']}|\n'
                 f'|status: {route['type']}|\n'
                 f'|crag: {route['crag_id']}|\n'
                 f'|user id: {route['user_id']}|\n')
           

def add_crag(name: str, country: str, city: str):
    url = "http://127.0.0.1:5000/crags"
    data = {
        'cragname': name,
        'country': country,
        'city': city
    } 
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print('API Response: ', response.json())
    else:
        print(f'Error: {response.status_code}')
        print('Details: ', response.text)   


def list_crags():
    url = "http://127.0.0.1:5000/crags"
    response = requests.get(url)
    crag_list = response.json()
    if response.status_code == 200:
        for crag in crag_list:
           print(20*'-')
           print(f'|crag id: {crag['id']}|\n'
                 f'|cragname: {crag['cragname']}|\n'
                 f'|country: {crag['country']}|\n'
                 f'|city: {crag['city']}|\n')
    else:
        print(f'Error: {response.status_code}')
        print('Details: ', response.text)

op = 0
while op != "7":
    op = input( '1 - Add user\n'
                '2 - Add crag\n'
                '3 - Add route\n'
                '4 - List users\n'
                '5 - List routes\n'
                '6 - List crags\n'
                '7 - Close the app...\n')
    if op not in "1234567":
        print("Choose a valid option...")
        continue
    elif op == "7":
        print("Closing the app...")
    elif op == "1":
        username = input("Enter your username:\n")
        add_user(username)
    elif op == "2":
        cragname = input("Enter the crag's name:\n")
        country = input("Enter the crag's country:\n")
        city = input("Enter the crag's city:\n")
        add_crag(cragname, country, city)
    elif op == "3":
        user_id = int(input("Enter a valid user id: "))
        crag_id = int(input('Enter the route\'s crag id:\n'))
        name = input('Enter the route\'s name: ')
        grade = input('Enter the route\'s grade: ')
        type = input('Enter the status (sent, project or wish): ')
        description = input('Enter the description:\n')
        add_route(name, grade, user_id ,crag_id, type, description)

    elif op == "4":
        list_users()
    elif op == "5":
        op_aux = input('1 - List all routes\n'
                       '2 - List by user\n')
        if op_aux not in "12":
            print("Invalid input...")
            continue
        elif op_aux == "1":
            list_routes(True)
        else:
            user_id = int(input('Enter the user ID: '))
            op_status = input(f'1 - List all routes registred for user {user_id}\n'
                       '2 - List sent routes\n'
                       '3 - List project routes\n'
                       '4 - List wish routes\n')
            if op_status not in "1234":
                print('Invalid option...')
                continue
            elif op_status == "1":
                list_routes(False, user_id)
            elif op_status == "2":
                list_routes(False, user_id, status='sent')
            elif op_status == "3":
                list_routes(False, user_id, status='project')
            else:
                list_routes(False, user_id, status='wish')
    elif op == '6':
        list_crags()



