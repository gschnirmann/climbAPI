from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


#seria /user/123/routes
#APIs rest sempre é da esquerda pra direita a "hierarquia"
#sempre /recurso/id/subrecurso


app = Flask(__name__)

crag_counter = 1
user_counter = 1
route_counter = 1


users = {}
routes = []
crags = []


def check_crag(crag_id: str) -> bool:
    for crag in crags:
        if crag['id'] == crag_id:
            return True
    return False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/routes.html')
def routes_page():
    return render_template('routes.html')


@app.route('/crags', methods=['POST'])
def add_crag():
    global crag_counter
    data = request.get_json()
    cragname = data.get('cragname')
    country = data.get('country')
    city = data.get('city')
    if not cragname or not country or not city:
        return jsonify({'message': 'Enter a valid cragname, country and city'}), 400
    crag = {'id': crag_counter, 'cragname': cragname, 'country': country, 'city': city}
    crags.append(crag)
    crag_counter += 1
    return jsonify({'id': crag['id'], 'cragname': crag['cragname'], 'country': crag['country'], 'city': crag['city']}), 201

@app.route('/crags', methods=['GET'])
def list_crags():
    if crags:
        return jsonify(crags)

@app.route('/users', methods=['POST'])
def add_user():
    global user_counter
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'message': 'Please enter a username'}), 400
    

    user = {'id':user_counter, 'username': username}
    users[user_counter] = user
    user_counter += 1
   
    return jsonify({'id': user['id'], 'username': user['username']}), 201



@app.route('/routes', methods=['POST'])
def add_route():
    global route_counter
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')
    type = data.get('type')
    user_id = data.get('user_id')
    crag_id = data.get('crag_id')

    if not name or not grade or not type or not user_id or not crag_id:
        return jsonify({'message': 'Enter a valid name, grade, type, user_id and crag_id'}), 400
    
    #if user_id not in users:
    #    return jsonify({'message': 'User not found'}), 404
    
    #if not check_crag(crag_id):
    #    return jsonify({'message': f'Crag {crag_id} not found'}), 404 
    
    route = {'id': route_counter, 'name': name, 'grade': grade, 'type': type, 'crag_id': crag_id, 'user_id': user_id}
    routes.append(route)
    route_counter += 1
   
    return jsonify({'id': route['id'], 'name': route['name'], 'grade': route['grade'], 'type':route['type'], 'crag_id': route['crag_id'], 'user_id': route['user_id']}), 201


@app.route('/routes', methods=['GET'])
def list_routes():
    
    if routes:
        type_filter = request.args.get('type')
        if type_filter:
            filtered_routes = [route for route in routes if route['type'] == type_filter]
        else:
            filtered_routes = routes
        return jsonify(filtered_routes)
    
    return jsonify({'message': 'Routes not found'}), 404

  
@app.route('/routes/<int:route_id>', methods=['GET'])
def find_route(route_id):
    for route in routes:
        if route["id"] == route_id:
            return jsonify(route)
    return jsonify({'message': 'Route not found...'}), 404
    



@app.route('/users/<int:user_id>/routes', methods=['GET'])
def list_sent_routes(user_id):
    if routes:
        type_filter = request.args.get("type")
        if type_filter:
            filtered_routes = [route for route in routes if route['type'] == type_filter and route['user_id'] == user_id]
        else:
            filtered_routes = [route for route in routes if route['user_id'] == user_id]
    
        return jsonify(filtered_routes)
    return jsonify({'message': 'Routes not found'}), 404


@app.route('/users', methods=['GET'])
def list_users():
    user_list = [{'id': k, 'username': v['username']} for k,v in users.items()]
    
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)