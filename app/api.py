import logging

import flask
from flask import request, jsonify
from flask_mysqldb import MySQL

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'my-backend-service'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jsppassword'
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def home():
    return '"[{\"status\": 200},{\"message\":\"_active\"}]"', 200


@app.route('/api/population', methods=['GET'])
def api_population_by_city():
    try:
        cursor = mysql.connection.cursor()
        query_parameters = request.args
        name = query_parameters.get('name')
        if name is not None and name.strip() != '':
            query = "SELECT city_name, population FROM city_population WHERE city_name=\"" + name + "\""
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return jsonify(results), 200
        else:
            return "[]", 200
    except Exception as e:
        logging.exception(e)
    return 'return "[{\"status\": 400},{\"message\":\"Error occurred during api call\"}]"', 400


@app.route('/api/population', methods=['POST'])
def api_insert_or_update_city_population():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            post_data = request.get_json(force=True)
            response = ""
            status_code = 200
            if post_data:
                cursor = mysql.connection.cursor()
                status = False
                for data in post_data:
                    if isinstance(data, str):
                        key = data
                        value = post_data[key]
                        status = insert_or_update(cursor, key, value)
                        if not status:
                            break
                    elif isinstance(data, dict):
                        for key in data:
                            value = data[key]
                            status = insert_or_update(cursor, key, value)
                            if not status:
                                break
                if status:
                    mysql.connection.commit()
                    response = "[{\"status\": 200},{\"message\":\"Records are added/updated successfully\"}]"
                else:
                    response = "[{\"status\": 400},{\"message\":\"There are errors occurred during insert/update\"}]"
                    status_code = 400
                cursor.close()
            return response, status_code
        else:
            return 'return "[{\"status\": 400},{\"message\":\"Content-Type not supported!\"}]"', 400
    except Exception as e:
        logging.exception(e)
    return 'return "[{\"status\": 400},{\"message\":\"Error occurred during api call\"}]"', 400


@app.errorhandler(404)
def page_not_found(e):
    return '"[{\"status\": 404},{\"message\":\"The resource could not be found.\"}]"', 404


def insert_or_update(cursor, key, value):
    try:
        query = "SELECT city_name, population FROM city_population WHERE city_name=\"" + key + "\";"
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            query = "UPDATE city_population SET population=\"" + str(
                value) + "\" WHERE city_name = \"" + key + "\";"
            cursor.execute(query)
            return True
        else:
            query = "INSERT INTO city_population (city_name,population) VALUES (\"" + key + "\",\"" + str(
                value) + "\");"
            cursor.execute(query)
            return True
    except Exception as e:
        logging.exception(e)
        return False


app.run(host='0.0.0.0', port=8080)
