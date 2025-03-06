from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import psycopg2
import psycopg2.extras



#seria /user/123/routes
#APIs rest sempre é da esquerda pra direita a "hierarquia"
#sempre /recurso/id/subrecurso


#Creates a flask class instance
app = Flask(__name__)


def db_connection():
    conn = psycopg2.connect(
        dbname = "climb_api_db",
        user = "gschnirmann",
        password = "geleia1924!",
        host = "localhost",
        port = "5432"
    )
    return conn


#main page endpoint
@app.route('/')
def index():
    return render_template('index.html') #renderiza index.html

#endpoint for rendering a login success page
@app.route('/success')
def success():
    username = request.args.get('username')
    return render_template('success.html', username=username)


#endpoint for rendering the register page
@app.route('/register', methods=['GET'])
def show_register_page():
    return render_template('register.html')

#endpoint for rendering the login page (called from the frontend)
@app.route('/login')
def show_login_page():
    return render_template('login.html')


#endpoint for searching an user in the database and rendering the main_menu_page
@app.route('/check_login', methods=['POST'])
def check_login():
    user_id = request.form.get('user_id')
    username = request.form.get('username')

    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s AND username = %s", (user_id, username))
    result = cursor.fetchone() #first result or None

    conn.commit()
    conn.close()
    
    if result:
        #entender se faz sentido passar o username no query parameter ou se faço a busca no bd depois
        #return redirect(url_for('user_page', user_id=user_id))
        #return redirect(url_for('list_sent_routes', user_id=user_id)) usei para listar as vias do usuario
        return render_template('menu_page.html', username=username, user_id=user_id)
    else:
        return "Error: User not found...", 401

    



#crags endpoint POST: redirect for the GET endpoint because the same page is used. So, it's added a route and updated in the same page.
@app.route('/crags', methods=['POST'])
def add_crag():
    #data = request.get_json()
    #cragname = data.get('cragname')
    #country = data.get('country')
    #city = data.get('city')

    cragname = request.form.get('cragname')
    country = request.form.get('country')
    city = request.form.get('city')

    if not cragname or not country or not city:
        return jsonify({'message': 'Enter a valid cragname, country and city'}), 400
    
    
    crag = {'cragname': cragname, 'country': country, 'city': city}
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO crags (cragname, country, city) VALUES (%s,%s,%s)", (crag['cragname'], crag['country'], crag['city']))
    conn.commit()
    conn.close()

    #Redirect to the same page (endpoint /crags GET) with the new crag
    return redirect(url_for('list_crags'))
    #return jsonify({'cragname': crag['cragname'], 'country': crag['country'], 'city': crag['city']}), 201

#render the template where the crags are listed.
@app.route('/crags', methods=['GET'])
def list_crags():
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crags")
    result = cursor.fetchall()
    crags = [{'id': crag_id, 'cragname': cragname, 'country': country, 'city': city} for crag_id, cragname, country, city in result]

    return render_template('crags.html',crags=crags)
    #return jsonify(crags)

#endpoint for adding a new user
@app.route('/users', methods=['POST'])
def add_user():
    if request.content_type == 'application/json':
        data = request.get_json()
        username = data.get('username')
    else:
        username = request.form.get('username')

   
    if not username:
        return jsonify({'message': 'Please enter a username'}), 400
    

    user = {'username': username}
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (user['username'],))
    conn.commit()
    conn.close()
   
    return redirect(url_for('success', username=username))
    #return jsonify({'username': user['username']}), 201




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
    
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 400
    
    cursor.execute('SELECT crag_id FROM crags WHERE crag_id = %s ', (crag_id,))
    crag = cursor.fetchone()
    if not crag:
        return jsonify({"error": "Crag not found"}), 400
    
    cursor.execute('INSERT INTO routes (name,grade,type,user_id,crag_id,description) VALUES (%s,%s,%s,%s,%s,%s)', (name,grade,type,user_id,crag_id,description,))


    conn.commit()
    conn.close()
    
    route = {'name': name, 'grade': grade, 'type': type, 'crag_id': crag_id, 'user_id': user_id, 'description': description}
    
   
    return jsonify({'name': route['name'], 'grade': route['grade'], 'type':route['type'], 'crag_id': route['crag_id'], 'user_id': route['user_id'], 'description': route['description']}), 201


@app.route('/routes', methods=['GET'])
def list_routes():
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    routes = []
    result = ()
    type_filter = request.args.get('type')
    if type_filter:
        cursor.execute('SELECT * FROM routes WHERE type = %s', (type_filter,))
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
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    #conn.row_factory = sqlite3.Row #returns with the columns name in a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM routes WHERE id = %s', (route_id,))
    result = cursor.fetchone()
    route = dict(result)

    conn.commit()
    conn.close()

    if route:
        return jsonify(route)
    else:
        return jsonify({'message': 'Route not found...'}), 404
    



@app.route('/users/<int:user_id>/routes', methods=['POST'])
def add_route_to_user(user_id):
    name = request.form.get('name')
    grade = request.form.get('grade')
    type = request.form.get('type')
    crag_id = request.form.get('crag_id')
    description = request.form.get('description')

    if not name or not grade or not type or not user_id or not crag_id:
        return jsonify({'message': 'Enter a valid name, grade, type, user_id and crag_id'}), 400
    
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 400
    
    cursor.execute('SELECT crag_id FROM crags WHERE crag_id = %s ', (crag_id,))
    crag = cursor.fetchone()
    if not crag:
        return jsonify({"error": "Crag not found"}), 400
    
    cursor.execute('INSERT INTO routes (name,grade,type,user_id,crag_id,description) VALUES (%s,%s,%s,%s,%s,%s)', (name,grade,type,user_id,crag_id,description,))


    conn.commit()
    conn.close()
    
    route = {'name': name, 'grade': grade, 'type': type, 'crag_id': crag_id, 'user_id': user_id, 'description': description}
    
    
    return redirect(url_for('list_sent_routes', user_id=user_id))
    #return jsonify({'name': route['name'], 'grade': route['grade'], 'type':route['type'], 'crag_id': route['crag_id'], 'user_id': route['user_id'], 'description': route['description']}), 201



@app.route('/users/<int:user_id>/routes', methods=['GET'])
def list_sent_routes(user_id):
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    #conn.row_factory = sqlite3.Row #returns with the columns name in a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    routes = []
   
    type_filter = request.args.get("type")
    if type_filter:
        cursor.execute('SELECT * FROM routes WHERE user_id = %s and type = %s', (user_id, type_filter,))
        result = cursor.fetchall()
        routes = [dict(row) for row in result]
    else:
        cursor.execute('SELECT * FROM routes WHERE user_id = %s', (user_id,))
        result = cursor.fetchall()
        routes = [dict(row) for row in result]
    conn.commit()
    conn.close()
    
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone() #first result or None
    username = result[0]

    crags = []
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    #conn.row_factory = sqlite3.Row #returns with the columns name in a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT crag_id,cragname FROM crags")
    result = cursor.fetchall()
    crags = [dict(row) for row in result]

    conn.commit()
    conn.close()

    if routes:
        #return jsonify(routes)
        return render_template('routes_page.html',routes=routes, username=username, crags=crags, user_id=user_id)
    else:
        return jsonify({'message': 'Routes not found'}), 404  

    


@app.route('/users', methods=['GET'])
def list_users():

    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
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
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return jsonify({'delete':'success'}), 200
    else:
        return jsonify({'error': 'not deleted'}), 404
    

#methods = 'DELETE'
@app.route('/routes/<int:route_id>', methods=['POST'])
def remove_route(route_id):
    user_id = request.args.get('user_id')
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM routes WHERE id = %s', (route_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return redirect(url_for('list_sent_routes', user_id=user_id))
        #return jsonify({'delete':'success'}), 200
    else:
        return jsonify({'error': 'not deleted'}), 404

#here should be 'DELETE' but a http request doesn't support a DELETE request from a form html.
@app.route('/crags/<int:crag_id>', methods=['POST'])
def remove_crag(crag_id):
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM crags WHERE crag_id = %s', (crag_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return redirect(url_for('list_crags'))
        #return jsonify({'delete':'success'}), 200
    else:
        return jsonify({'error': 'not deleted'}), 404


#PUT endpoints
@app.route('/routes/edit/<int:user_id>/<int:route_id>', methods=['GET'])
def show_edit_route(user_id, route_id):
    
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    #conn.row_factory = sqlite3.Row #returns with the columns name in a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM routes WHERE id = %s', (route_id,))
    route = dict(cursor.fetchone())

    cursor.execute('SELECT username FROM users WHERE user_id = %s ', (user_id,))
    result = cursor.fetchone()
    username = result[0]

    crags = []
    #conn.row_factory = sqlite3.Row #returns with the columns name in a dictionary
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT crag_id,cragname FROM crags")
    result = cursor.fetchall()
    crags = [dict(row) for row in result]


    conn.commit()
    conn.close()

    if route:
        return render_template('edit_route.html', username=username, route=route, crags=crags, user_id=user_id)

@app.route('/routes/edit/<int:user_id>/<int:route_id>', methods=['POST'])
def edit_route(user_id, route_id):
    #conn = sqlite3.connect('climb_API_db')
    conn = db_connection()
    cursor = conn.cursor()
    name = request.form.get('name')
    grade = request.form.get('grade')
    status = request.form.get('type')
    crag_id = request.form.get('crag_id')
    description = request.form.get('description')


    cursor.execute('UPDATE routes SET name = %s, grade = %s, type = %s, crag_id = %s, description = %s WHERE id = %s',(name, grade, status, crag_id, description, route_id))

    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return redirect(url_for('list_sent_routes', user_id=user_id))
    else:
        return jsonify({'error': 'not updated'}), 404

if __name__ == '__main__':
    app.run(debug=True)