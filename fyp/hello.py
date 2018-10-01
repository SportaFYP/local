from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, g
import os
from hashlib import md5
from sqlalchemy.orm import sessionmaker
from tabledef import *
# import sqlite3
# from sqlite3 import Error
import paho.mqtt.client as mqtt
import ssl
import json
import ctypes  # An included library with Python install.
import MySQLdb
import datetime

  
# MQTT variables############################################
hostMQTT = "localhost"
portMQTT = 1883
# topic = "tagsLive" 
client = mqtt.Client()
# MQTT variables END#######################################



# conn = sqlite3.connect("C:\Users\L31304\Desktop\MQTT\MQTT\db\mqtt1.db")
# engine = create_engine('sqlite:///tutorial.db', echo=True)

# MySQL VRIABLWS############################################
host = "localhost"
port = 3306
topic = "tagsLive" 
user = "root"
passwd="Sportapassword12"
db="Sportadb"
conn = MySQLdb.connect(host,
                  user,
                  passwd,
                  db)
# MySQL VRIABLWS END#######################################
class ServerError(Exception):pass
# client = mqtt.Client(transport="websockets")
# hostMQTT = "mqtt.cloud.pozyxlabs.com"
# portMQTT = 443
# topic = "5b165a3953760e60306a0a8c"  # your mqtt topic
# username = "5b165a3953760e60306a0a8c"  # your mqtt username
# password = "3f0ac6f0-2938-4270-b49b-5a77157993dc"  # your generated api key
# set callbacks
# client.username_pw_set(username, password=password)
# sets the secure context, enabling the WSS protocol
# client.tls_set_context(context=ssl.create_default_context())

def create_connection(db_file):
    """ create a database connection to the MySQL database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    # try:
    conn = MySQLdb.connect(db_file)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    # try:
    c = conn.cursor()
    c.execute(create_table_sql)

def main():
    #conn = create_connection(database)
   sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        number INTEGER AUTO_INCREMENT PRIMARY KEY,
                                        version INTEGER ,
                                        tagId INTEGER NOT NULL,
                                        success INTEGER,
                                        timestamp DECIMAL,
                                        magnetic_x DECIMAL,
                                        magnetic_y DECIMAL,
                                        magnetic_z DECIMAL,
                                        quaternion_x DECIMAL,
                                        quaternion_y DECIMAL,
                                        quaternion_z DECIMAL,
                                        quaternion_w DECIMAL,
                                        linearAcceleration_x INTEGER,
                                        linearAcceleration_y INTEGER,
                                        linearAcceleration_z INTEGER,
                                        pressure DECIMAL,
                                        maxLinearAcceleration INTEGER,
                                        anchorData INTEGER,
                                        coordinates_x INTEGER,
                                        coordinates_y INTEGER,
                                        coordinates_z INTEGER,
                                        acceleration_x DECIMAL,
                                        acceleration_y DECIMAL,
                                        acceleration_z DECIMAL,
                                        yaw DECIMAL,
                                        roll DECIMAL,
                                        pitch DECIMAL,
                                        latency TEXT
                                        
                                    ); """                                   
    
   
   if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
   else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

app = Flask(__name__)
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        #add in table
        return displayTable()
    #    / return render_template('home.html')

#@app.route("/tabledisplay")
def displayTable():
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM matches")
    rows = mycursor.fetchall()
    print(str(row) for row in rows)
    
    return '<br>'.join(str(row) for row in rows)


@app.route('/match')
def point():
    if session.get('logged_in'):
        return render_template('point1.html')




## User login
@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    if 'username' in session:
        return redirect(home)
    
    error = None
    try:
        if request.method == 'POST':
            username_form  = request.form['username']
           
            usr = (username_form,)
            sql1="SELECT COUNT(1) FROM users WHERE username = %s"
            cur.execute(sql1, usr)
    

            if not cur.fetchone()[0]:
                print("Invalid username")
                raise ServerError('Invalid username')

            print("Valid username")
            password_form  = request.form['password']
            psd = (password_form,)
            sql2="SELECT password FROM users WHERE password = %s"
            cur.execute(sql2,psd)

            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    print("Valid password")
                    session['logged_in'] = True
                    return home()

            print("invalid password")
            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)

    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/create")
def create():
    if session.get('logged_in'):
        return render_template('create.html')

@app.route('/createMatch', methods=['POST'])
def create_matches():
    # data from form
    POST_matchname = str(request.form['matchname'])
    POST_matchdate = str(request.form['matchdate'])
    POST_administrator = str(request.form['administrator'])
    POST_matchnotes = str(request.form['matchnotes'])
    # create match data# 
    matchData = (POST_matchname, POST_matchdate, POST_administrator, POST_matchnotes)
    #SQL statement
    sql = ''' INSERT INTO matches(matchname, matchdate, administrator, matchnotes)
              VALUES(%s,%s,%s,%s) '''
              
    cur = conn.cursor()
    cur.execute(sql, matchData)
    try:
        conn.commit()
    except Exception as e: 
        print(e)
    return home()


###### MQTT start here ###############
@app.route("/start")
def startMQTT():
    print("Start recording!avc")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    #try and catch
    client.connect(hostMQTT, port=portMQTT)
    client.subscribe(topic)
    print("before client!")
    # print(client)
    #works blocking, other, non-blocking, clients are available too.
    client.loop_start()
    print("after client!")
    return home()

###### MQTT stop here ###############
@app.route("/stop")
def stopMQTT():
    print("Stop recording")
    client.loop_stop()
    return home()


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")
 #   SQL connection code here
 #   how to connect database here



#To connect to MQTT queue
def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    print(mqtt.connack_string(rc))



# callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
 print("Positioning update:", msg.payload.decode())
 #return;

 result = json.loads(msg.payload)  # result is now a dict
 print '"version":', result['version']
 version = result['version']
 
 print '"tagId":', result['tagId']
 tagId = result['tagId']

 print '"success":', result['success']
 success = result['success']

 print '"timestamp":', result['timestamp']
 timestamp = result['timestamp']

 print '"magnetic_x":', result['data']['tagData']['magnetic']['x']
 magnetic_x = result['data']['tagData']['magnetic']['x']

 print '"magnetic_y":', result['data']['tagData']['magnetic']['y']
 magnetic_y = result['data']['tagData']['magnetic']['y']

 print '"magnetic_z":', result['data']['tagData']['magnetic']['z']
 magnetic_z = result['data']['tagData']['magnetic']['z']

 print '"coordinates_x":', result['data']['coordinates']['x']
 coordinates_x = result['data']['coordinates']['x']

 print '"coordinates_y":', result['data']['coordinates']['y']
 coordinates_y = result['data']['coordinates']['y']

 print '"coordinates_z":', result['data']['coordinates']['z']
 coordinates_z = result['data']['coordinates']['z']

 print '"acceleration_x":', result['data']['acceleration']['x']
 acceleration_x = result['data']['acceleration']['x']

 print '"acceleration_y":', result['data']['acceleration']['y']
 acceleration_y = result['data']['acceleration']['y']

 print '"acceleration_z":', result['data']['acceleration']['z']
 acceleration_z = result['data']['acceleration']['z']

 print '"yaw":', result['data']['orientation']['yaw']
 yaw = result['data']['orientation']['yaw']

 print '"roll":', result['data']['orientation']['roll']
 roll = result['data']['orientation']['roll']

 print '"pitch":', result['data']['orientation']['pitch']
 pitch = result['data']['orientation']['pitch']

#  create the point in database
 point = (version, tagId, success, timestamp, magnetic_x, magnetic_y, magnetic_z, coordinates_x, coordinates_y, coordinates_z, acceleration_x, acceleration_y, acceleration_z, yaw, roll, pitch)
 create_point(point)

 return
 
def create_point(point):
    """
    Create a new point
    :param conn:
    :param point:
    :return:
    """
 
    sql = ''' INSERT INTO projects(version, tagId, success, timestamp, magnetic_x, magnetic_y, magnetic_z, coordinates_x, coordinates_y, coordinates_z, acceleration_x, acceleration_y, acceleration_z, yaw, roll, pitch)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
    cur = conn.cursor()
    cur.execute(sql, point)
    conn.commit()
    return cur.lastrowid



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=8000)
