from flask import Flask, request, jsonify, render_template
import sqlite3



#seria /user/123/routes
#APIs rest sempre é da esquerda pra direita a "hierarquia"
#sempre /recurso/id/subrecurso


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/routes.html')
def routes_page():
    return render_template('routes.html')


@app.route('/crags', methods=['POST'])
def add_crag():
    data = request.get_json()
    cragname = data.get('cragname')
    country = data.get('country')
    city = data.get('city')
    if not cragname or not country or not city:
        return jsonify({'message': 'Enter a valid cragname, country and city'}), 400
    
    
    crag = {'cragname': cragname, 'country': country, 'city': city}
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO crags (cragname, country, city) VALUES (?,?,?)", (crag['cragname'], crag['country'], crag['city']))
    conn.commit()
    conn.close()

    return jsonify({'cragname': crag['cragname'], 'country': crag['country'], 'city': crag['city']}), 201

@app.route('/crags', methods=['GET'])
def list_crags():
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crags")
    result = cursor.fetchall()
    crags = [{'id': crag_id, 'cragname': cragname, 'country': country, 'city': city} for crag_id, cragname, country, city in result]

    return jsonify(crags)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'message': 'Please enter a username'}), 400
    

    user = {'username': username}
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (?)", (user['username'],))
    conn.commit()
    conn.close()
   
    return jsonify({'username': user['username']}), 201



@app.route('/routes', methods=['POST'])
def add_route():
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')
    type = data.get('type')
    user_id = data.get('user_id')
    crag_id = data.get('crag_id')
    description = data.get('description')

    if not name or not grade or not type or not user_id or not crag_id:
        return jsonify({'message': 'Enter a valid name, grade, type, user_id and crag_id'}), 400
    
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 400
    
    cursor.execute('SELECT crag_id FROM crags WHERE crag_id = ? ', (crag_id,))
    crag = cursor.fetchone()
    if not crag:
        return jsonify({"error": "Crag not found"}), 400
    
    cursor.execute('INSERT INTO routes (name,grade,type,user_id,crag_id,description) VALUES (?,?,?,?,?,?)', (name,grade,type,user_id,crag_id,description,))


    conn.commit()
    conn.close()
    
    route = {'name': name, 'grade': grade, 'type': type, 'crag_id': crag_id, 'user_id': user_id, 'description': description}
    
   
    return jsonify({'name': route['name'], 'grade': route['grade'], 'type':route['type'], 'crag_id': route['crag_id'], 'user_id': route['user_id'], 'description': route['description']}), 201


@app.route('/routes', methods=['GET'])
def list_routes():
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    routes = []
    result = ()
    type_filter = request.args.get('type')
    if type_filter:
        cursor.execute('SELECT * FROM routes WHERE type = ?', (type_filter,))
        result = cursor.fetchall()

    else:
        cursor.execute('SELECT * FROM routes')
        result = cursor.fetchall()
    

    conn.commit()
    conn.close()

    routes = [{'id': id, 'name': name, 'grade': grade, 'user_id': user_id, 'crag_id': crag_id, 'type': type, 'description': description} for id,name,grade,user_id,crag_id,type,description in result]
    if routes:
        return jsonify(routes)
    else:
        return jsonify({'message': 'Routes not found'}), 404

    

  
@app.route('/routes/<int:route_id>', methods=['GET'])
def find_route(route_id):
    conn = sqlite3.connect('climb_API_db')
    conn.row_factory = sqlite3.Row #returns with the columns name in a dictionary
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM routes WHERE id = ?', (route_id,))
    result = cursor.fetchone()
    route = dict(result)

    conn.commit()
    conn.close()

    if route:
        return jsonify(route)
    else:
        return jsonify({'message': 'Route not found...'}), 404
    



@app.route('/users/<int:user_id>/routes', methods=['GET'])
def list_sent_routes(user_id):
    conn = sqlite3.connect('climb_API_db')
    conn.row_factory = sqlite3.Row #returns with the columns name in a dictionary
    cursor = conn.cursor()
    routes = []
    type_filter = request.args.get("type")
    if type_filter:
        cursor.execute('SELECT * FROM routes WHERE user_id = ? and type = ?', (user_id, type_filter,))
        result = cursor.fetchall()
        routes = [dict(row) for row in result]
    else:
        cursor.execute('SELECT * FROM routes WHERE user_id = ?', (user_id,))
        result = cursor.fetchall()
        routes = [dict(row) for row in result]
    conn.commit()
    conn.close()

    if routes:
        return jsonify(routes)
    else:
      return jsonify({'message': 'Routes not found'}), 404  

    


@app.route('/users', methods=['GET'])
def list_users():

    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM users")
    result = cursor.fetchall()
    user_list = [{'id': id, 'username': username} for id,username in result]

    conn.commit()
    conn.close()
    #when a set of users was used
    #user_list = [{'id': k, 'username': v['username']} for k,v in users.items()]
    

    return jsonify(user_list)


#delete endpoints
@app.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return jsonify({'delete':'success'}), 200
    else:
        return jsonify({'error': 'not deleted'}), 404

@app.route('/routes/<int:route_id>', methods=['DELETE'])
def remove_route(route_id):
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM routes WHERE id = ?', (route_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return jsonify({'delete':'success'}), 200
    else:
        return jsonify({'error': 'not deleted'}), 404

@app.route('/routes/<int:crag_id>', methods=['DELETE'])
def remove_crag(crag_id):
    conn = sqlite3.connect('climb_API_db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM routes WHERE crag_id = ?', (crag_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return jsonify({'delete':'success'}), 200
    else:
        return jsonify({'error': 'not deleted'}), 404


if __name__ == '__main__':
    app.run(debug=True)