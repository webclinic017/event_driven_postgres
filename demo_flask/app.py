import json

from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/widgets')
def get_widgets():
    conn = psycopg2.connect(
        host="postgresdb",
        database="inventory",
        user="postgres",
        password="p@ssw0rd1"
    )

    conn.set_session(autocommit=True)

    cur = conn.cursor()

    cur.execute("SELECT * FROM widgets;")

    results = cur.fetchall()
    
    cur.close()

    conn.close()

    json_data = {}
    result_id = 0
    for result in results:
        temp_result = {'name': result[0], 'tag': result[1]}
        json_data[result_id] = temp_result
        result_id += 1

    return json.dumps(json_data)

@app.route('/add_widget/<name>/<tag>')
def add_widgets(name, tag):

    sql = """INSERT INTO widgets(name, description)
            VALUES(%s, %s);"""

    conn = psycopg2.connect(
        host="postgresdb",
        database="inventory",
        user="postgres",
        password="p@ssw0rd1"
    )

    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute(sql, (name, tag,))
 
    cur.close()
    conn.close()

    return 'Success'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
