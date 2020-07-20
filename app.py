from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import json
import requests

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql-python-service'
app.config['MYSQL_USER'] = 'ishan'
app.config['MYSQL_PASSWORD'] = 'ishan'
app.config['MYSQL_DB'] = 'Student'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
url = "http://localhost:5000"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/postdata', methods=["POST"])
def printing_data():
    if request.form:
        req = request.form
    else:
        req = request.get_json()

    name = req['student_name']
    s_id = req['student_id']
    email = req['student_email']
    phone = req['student_phone']
    student_class = req['student_class']

    cur = mysql.connection.cursor()

    if (name or id or email or phone or student_class) != "":
        cur.execute('INSERT INTO Student_Info(student_name,student_id, student_email, student_phone, '
                    'student_class) VALUES ("' + name + '","' + s_id + '","' + email + '","' + phone + '",'
                                                                                                       '"' +
                    student_class + '");')
        mysql.connection.commit()
        cur.close()
        req.update({'success':'data created successfully'})
        return req
    else:
        return jsonify(error=str("error")), 404


@app.route('/getdata', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Student_Info;')
    data = cur.fetchall()
    cur.close()
    student_list = []
    json_obj = json.dumps(data)
    student_info_complete_list = json.loads(json_obj)
    for i in student_info_complete_list:
        temp_dict = {'student_name': i[0],
                     'student_id': i[1],
                     'student_email': i[2],
                     'student_phone': i[3],
                     'student_class': i[4]}
        student_list.append(temp_dict)
    return json.dumps(student_list)


@app.route('/getdatabyname/<name>', methods=['GET'])
def get_data_by_name(name):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Student_Info WHERE student_name ="' + name + '";')
    data = cur.fetchall()
    cur.close()
    student_list = []
    json_obj = json.dumps(data)
    student_info_complete_list = json.loads(json_obj)

    for i in student_info_complete_list:
        temp_dict = {'student_name': i[0],
                     'student_id': i[1],
                     'student_email': i[2],
                     'student_phone': i[3],
                     'student_class': i[4]}
        student_list.append(temp_dict)
    return json.dumps(student_list)



@app.route('/deletedatabyname/<name>', methods=["DELETE"])
def delete_data_by_name(name):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Student_Info WHERE student_name ="' + name + '";')
    mysql.connection.commit()
    cur.close()
    return json.dumps({'success':'data deleted successfully'}), 200, {'ContentType':'application/json'}


@app.route('/updatedatabyname/<name>', methods=["PUT"])
def update_data_name(name):
    data = get_data_by_name(name)
    data = json.loads(data)
    updated_data = request.get_json()
    data_to_be_modified = data[0]
    data_to_be_modified.update(updated_data)
    delete_data_by_name(name)
    requests.post(url + "/postdata", json=data_to_be_modified)
    return json.dumps({'success':'data updated successfully'}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
