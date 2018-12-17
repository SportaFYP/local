from flask import Flask
from flask import jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort, g
import os
from hashlib import md5
from sqlalchemy.orm import sessionmaker
import simplejson as json

import paho.mqtt.client as mqtt
import ssl
import json
import ctypes  # An included library with Python install.
import MySQLdb
import datetime
import time
import pymysql
import re
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
from flask import send_from_directory

UPLOAD_FOLDER1 = 'static/videos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webm'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1



  
# MQTT variables############################################
hostMQTT = "localhost"
portMQTT = 1883
# topic = "tagsLive" 
client = mqtt.Client()
# MQTT variables END#######################################

# MySQL VRIABLES############################################
host = "172.20.129.227"
port = 3306
topic = "tagsLive" 
user = "admin1"
passwd="Sportapassword12"
db="Sportadb"
RID=0L
matchID=0
conn = MySQLdb.connect(host,
                  user,
                  passwd,
                  db)
# MySQL VRIABLWS END#######################################
class ServerError(Exception):pass


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
    
   
#    if conn is not None:
#         create projects table
#         create_table(conn, sql_create_projects_table)
#    else:
#         print("Error! cannot create the database connection.")

def selectMatch(db, cursor):
    sql="SELECT * FROM matches"
    cursor.execute(sql)
    #fetch the result
    match=cursor.fetchall()
    return match





if __name__ == '__main__':
    main()

app = Flask(__name__)
 

@app.route("/")
def displayTable():
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM matches")
    rows = mycursor.fetchall()

    if not session.get('currentRecordingID'):
        print("currentRecordingID:")
       
    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        return render_template('homepage.html',rows=rows)

@app.route("/name")
def displayTablebyname():
    mycursor = conn.cursor()
    administrator_form  = session['username']
           
    admin = (administrator_form,)
    sql1 = ("SELECT * FROM matches WHERE administrator = %s")
    mycursor.execute(sql1, admin)
    rows = mycursor.fetchall()

    if not session.get('currentRecordingID'):
        print("currentRecordingID:")
       
    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        return render_template('homepage.html', rows=rows)

@app.route("/viewAll")
def viewAllmatches():
    return redirect(url_for('displayTable'))

@app.route('/match/<matchID>')
def viewMatch(matchID):
    if session.get('logged_in'):

        print ('view match')
        MID = (matchID,)
        print(matchID)
        mycursor = conn.cursor()
        query=("SELECT * FROM recordings WHERE Match_ID=%s")
        mycursor.execute(query,MID)
        session['my_var1'] = matchID
        session['my_var2'] = matchID
        rowss = mycursor.fetchall()
        
        query1=("SELECT * FROM matches WHERE MatchID=%s")
        mycursor.execute(query1,MID)

        matchNotes = mycursor.fetchone()
        print ("matchNotes")
        print (matchNotes)
        data = {'rowss': rowss, 'matchNotes': matchNotes[0], 'matchData': matchNotes, 'matchID': matchID}

        return render_template('match.html', data=data, )



@app.route('/recordingview/<matchID>/<RID>')
def viewRecordings(matchID, RID):
    print("RID:")
    print(RID)
    RID1 = (RID,)
    print("123")
    # with RID.... can u finally get the points?
    mycursor = conn.cursor()
    # hello =("SELECT * FROM projects WHERE RecordingID = %s")
    hello =("SELECT tagId,timestamp,coordinates_x,coordinates_y FROM projects WHERE RecordingID = %s")
    mycursor.execute(hello, RID1)
    coords = mycursor.fetchall()
    print(coords)
    session['my_var'] = RID
    session['my_var1'] = matchID
    return redirect(url_for('viewreplay'))

## User login
@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    if 'username' in session:
        print("username still valid")
        print(session['username'])
        return redirect('/')
    
    error = None
    try:
        if request.method == 'POST':
            username_form  = request.form['username']
           
            usr = (username_form,)
            sql1="SELECT COUNT(1) FROM users WHERE username = %s"
            cur.execute(sql1, usr)
    

            if not cur.fetchone()[0]:
                print("Invalid username")
                flash("invalid username/password")
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
                    return redirect('/')

            print("invalid password")
            flash("invalid username/password")
            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)

    return displayTable()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = None
    session.clear()
    return redirect('/')

@app.route("/create-match", methods = ['GET', 'POST'])
def create_match_page():
    if session.get('logged_in'):
        cur = conn.cursor()
        cur.execute('SELECT teamId FROM team')
        teamListResult = cur.fetchall()
        cur1 = conn.cursor()
        cur1.execute('SELECT * FROM teamstudent')
        playerListResult = cur1.fetchall()
        #print playerListResult
        cur2 = conn.cursor()
        cur2.execute('SELECT * FROM tags')
        tagList = cur2.fetchall()
        print tagList
        return render_template('create-match.html', **locals())
    else:
        return redirect('/')

@app.route("/create-match/<team>")
def create_match_select(team):
    cur2 = conn.cursor()
    teamName = team
    #print "teamname in create match: "+teamName
    query = 'SELECT studentName FROM teamstudent WHERE teamId = %s'
    cur2.execute(query, [teamName])
    playerNames = cur2.fetchall()
    #print playerNames
    return jsonify(playerNames)#redirect('/create-match.html', **locals())

@app.route("/students")
def create_student_page():
    if session.get('logged_in'):
        cur = conn.cursor()
        cur.execute('SELECT * FROM student')
        student = cur.fetchall()
        cur.execute('SELECT * FROM team')
        teamIdResult = cur.fetchall()
        cur.execute('SELECT * FROM teamstudent')
        studentInTeam = cur.fetchall()

        rows = []
        inTeams = {}

        for i in student:
            inTeamsConcat = ""
            counterj = 0
            k = []
            for j in studentInTeam:
                if (j[1] == i[1]):
                    if counterj is not 0:
                        inTeamsConcat = inTeamsConcat + ", "
                    inTeamsConcat = inTeamsConcat + j[0]
                    k.append(j[0])
                    counterj += 1
            rows.append((i[0], i[1], i[2], inTeamsConcat))
            inTeams[i[1]] = k

        createStudentStatus = session.get('createStudentStatus')
        editStudentStatus = session.get('editStudentStatus')
        deleteStudentStatus = session.get('deleteStudentStatus')
        session['createStudentStatus'] = ''
        session['editStudentStatus'] = ''
        session['deleteStudentStatus'] = ''
        return render_template('student.html', **locals())
    else:
        return redirect('/')

@app.route("/teams")
def create_team_page():
    if session.get('logged_in'):
        cur = conn.cursor()
        cur.execute('SELECT * FROM team')
        teamrows = cur.fetchall()
        cur.execute('SELECT * FROM teamstudent')
        studentrow = cur.fetchall()

        rows = []
        
        for t in teamrows:
            teamcount = 0
            for s in studentrow:
                if t[0] == s[0]:
                    teamcount += 1
            rows.append([t[0], t[1], t[2], teamcount])
        print(rows)
        createTeamStatus = session.get('createTeamStatus')
        deleteTeamStatus = session.get('deleteTeamStatus')
        session['createTeamStatus'] = ''
        session['deleteTeamStatus'] = ''
        return render_template('team.html', **locals())
    else:
        return redirect('/')

@app.route("/tag")
def tagpage():
    if session.get('logged_in'):
        return render_template('tag.html')
    else:
        return redirect('/')

@app.route("/record")
def recordpage():
    if session.get('logged_in'):
        return render_template('record.html')
    else:
        return redirect('/')

@app.route('/displayData', methods=['POST'])
def disply_data():
    mycursor = conn.cursor()
    show = "SELECT * FROM tags"
    mycursor.execute(show)
    display = mycursor.fetchall()
    return display


@app.route('/updateTag', methods=['POST'])
def update_tag():
    POST_tag1 = str(request.form['tag1'])
    POST_tag2 = str(request.form['tag2'])
    POST_tag3 = str(request.form['tag3'])
    POST_tag4 = str(request.form['tag4'])
    POST_tag5 = str(request.form['tag5'])
    updatetag = (POST_tag1, POST_tag2, POST_tag3, POST_tag4, POST_tag5)
    tag = "UPDATE tags SET tag1 =%s, tag2=%s, tag3=%s, tag4= %s, tag5=%s"
    mycursor = conn.cursor()
    mycursor.execute(tag, updatetag)
    try:
        conn.commit()
    except Exception as e: 
        print(e)
    return tagpage()

@app.route('/createMatch', methods=['POST'])
def createMatch():
    # data from form
    POST_matchname = str(request.form['matchname'])
    POST_matchdate = str(request.form['matchdate'])
    POST_administrator = session['username']
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
    
    #Get the MatchID that was just inserted
    cur1 = conn.cursor()
    cur1.execute('SELECT MatchID FROM matches ORDER BY MatchID DESC LIMIT 1')
    tempNum = str(cur1.fetchall())
    matchid = int(tempNum[2] + tempNum[3])
    #print matchid
    POST_player1 = (matchid, POST_matchname, str(request.form['team1']), str(request.form['play1']), 1, str(request.form['tagNum1']))
    POST_player2 = (matchid, POST_matchname, str(request.form['team2']), str(request.form['play2']), 2, str(request.form['tagNum2']))
    POST_player3 = (matchid, POST_matchname, str(request.form['team3']), str(request.form['play3']), 3, str(request.form['tagNum3']))
    POST_player4 = (matchid, POST_matchname, str(request.form['team4']), str(request.form['play4']), 4, str(request.form['tagNum4']))
    POST_player5 = (matchid, POST_matchname, str(request.form['team5']), str(request.form['play5']), 5, str(request.form['tagNum5']))
    POST_player6 = (matchid, POST_matchname, str(request.form['team6']), str(request.form['play6']), 6, str(request.form['tagNum6']))
    POST_player7 = (matchid, POST_matchname, str(request.form['team7']), str(request.form['play7']), 7, str(request.form['tagNum7']))
    POST_player8 = (matchid, POST_matchname, str(request.form['team8']), str(request.form['play8']), 8, str(request.form['tagNum8']))
    POST_player9 = (matchid, POST_matchname, str(request.form['team9']), str(request.form['play9']), 9, str(request.form['tagNum9']))
    POST_player10 = (matchid, POST_matchname, str(request.form['team10']), str(request.form['play10']), 10, str(request.form['tagNum10']))
    POST_player11 = (matchid, POST_matchname, str(request.form['team11']), str(request.form['play11']), 11, str(request.form['tagNum11']))
    POST_player12 = (matchid, POST_matchname, str(request.form['team12']), str(request.form['play12']), 12, str(request.form['tagNum12']))
    POST_player13 = (matchid, POST_matchname, str(request.form['team13']), str(request.form['play13']), 13, str(request.form['tagNum13']))
    POST_player14 = (matchid, POST_matchname, str(request.form['team14']), str(request.form['play14']), 14, str(request.form['tagNum14']))
    POST_allPlayers = [POST_player1, POST_player2, POST_player3, POST_player4, POST_player5, POST_player6, POST_player7, POST_player8, POST_player9, POST_player10, POST_player11, POST_player12, POST_player13, POST_player14]
    #print POST_allPlayers
    #print "teamName is: " + POST_player1[2] + " Player name is: " + POST_player1[3] + " tag number is: " + POST_player1[4]

    postingQuery = 'INSERT INTO matchinfo(matchID, matchname, teamID, studentName, playerNum, tagID) VALUES(%s, %s, %s, %s, %s, %s)'

    insertPlayer = []
    for players in POST_allPlayers:
        if players[2] != "" and players[3] != "" and players[4] != "":
            insertPlayer.append(players)
    print insertPlayer

    curPost = conn.cursor()
    curPost.executemany(postingQuery, insertPlayer)
    try:
        conn.commit()
    except Exception as e:
        print(e)

    return displayTable()

    

@app.route('/createStudent', methods=['POST'])
def createStudent():
    #SQL statement
    sql = ''' INSERT INTO teamstudent (`teamId`, `studentName`) 
              VALUES (%s, %s) '''
    sql2 = ''' INSERT INTO student (`name`, `gender`) 
               VALUES (%s, %s) '''

    try:          
        cur = conn.cursor()
        cur.execute(sql, ([str(request.form['teamId'])], [str(request.form['studentName'])]))

        cur.execute("select name from student where name = %s", [str(request.form['studentName'])])
        tmp = cur.fetchall()
        if tmp:
            session['createStudentStatus'] = 1 # Student already exists in the database, no need duplicate entries in the student table
        else:
            cur.execute(sql2, ([str(request.form['studentName'])], [str(request.form['studentGender'])]))
            session['createStudentStatus'] = 0
        conn.commit()
    except MySQLdb.IntegrityError as ie: # Student-Team pair is already found in database
        session['createStudentStatus'] = 2
    except Exception as e:
        print(e)
    return redirect('students')

@app.route('/editStudent/<id>/<student>/<gender>', methods=['POST'])
def editStudent(id, student, gender):
    sql = '''SELECT teamId FROM teamStudent WHERE (`studentName` = %s)'''
    sql2 = '''UPDATE student SET `name` = %s WHERE (`id` = %s);'''
    sql3 = '''UPDATE teamstudent SET studentName = REPLACE (studentName, %s, %s)'''
    sql4 = '''UPDATE student SET `gender` = %s WHERE (`id` = %s);'''
    sql5 = '''DELETE FROM teamstudent WHERE (`teamId` = %s) and (`studentName` = %s);'''

    cur = conn.cursor()
    cur.execute(sql, [student])
    teams = cur.fetchall()
    
    # Make sure to check if all the teams are ticked for removal cause that is not allowed
    tickcount = 0
    for t in teams:
        try:
            if request.form[t[0]] == 'on':
                tickcount += 1
        except BadRequestKeyError:
            print('') # Do nothing
    if tickcount == len(teams):
        session['editStudentStatus'] = 1
        return redirect('students')

    if not (str(request.form['editStudentName']) == student):
        cur.execute(sql2, ([str(request.form['editStudentName'])], id))
        cur.execute(sql3, (student, [str(request.form['editStudentName'])]))

    if not (str(request.form['editStudentGender']) == gender):
        cur.execute(sql4, ([str(request.form['editStudentGender'])], id))
    
    for t in teams:
        try:
            if request.form[t[0]] == 'on':
                cur.execute(sql5, ([str(t[0])], [str(request.form['editStudentName'])]))
        except BadRequestKeyError:
            print('') # Do nothing
    conn.commit()
    session['editStudentStatus'] = 0
    return redirect('students')

@app.route('/deleteStudent/<studName>')
def deleteStudent(studName):
    sql = '''DELETE FROM student WHERE (`name` = %s);'''
    sql2 = '''DELETE FROM teamstudent WHERE (`studentName` = %s);'''

    try:          
        cur = conn.cursor()
        cur.execute(sql, [studName])
        cur.execute(sql2, [studName])

        session['deleteStudentStatus'] = 0
        conn.commit()
    except Exception as e: # Something went wrong
        session['deleteStudentStatus'] = 1
        print(e)
    return redirect('students')

@app.route('/createTeam', methods=['POST'])
def createTeam():
    #SQL statement
    sql = ''' INSERT INTO team (`teamid`, `createdDate`, `createdBy`) 
              VALUES (%s, %s, %s) '''

    try:          
        cur = conn.cursor()
        cur.execute(sql, ([str(request.form['teamId'])], datetime.datetime.now(), session['username']))
        conn.commit()
    except MySQLdb.IntegrityError as ie: # Team is already found in database
        session['createTeamStatus'] = 1
    except Exception as e:
        print(e)
    else:
        session['createTeamStatus'] = 0
    return redirect('teams')

@app.route('/deleteTeam/<team>')
def deleteTeam(team):
    #SQL statement
    sql = ''' DELETE FROM team WHERE (`teamid` = %s); '''
         
    cur = conn.cursor()
    cur.execute(sql, [team])
    conn.commit()
    session['deleteTeamStatus'] = 0
    return redirect('teams')


###### Retrive font start ###############
@app.route('/fonts/<fontfile>', methods=["GET"])
def getFont(fontfile):
    print(fontfile)
    return redirect('/static/fonts/' + fontfile)
###### Retrive font end ###############         

###### MQTT start here ###############
@app.route("/start")
def startMQTT():  
    my_var1 = session.get('my_var1', None)
    mid1 = my_var1.decode('unicode-escape')
    now = datetime.datetime.now()
    sql = '''INSERT INTO recordings (Match_ID, startTime) VALUES(%s,%s)'''
    recordingData = ([mid1], now)
    cur = conn.cursor()
    cur.execute(sql, recordingData)
            

    try:
        conn.commit()
        
        global RID
        RID = cur.lastrowid
        print("currentRecordingID after commit: " + str(RID))
    except Exception as e: 
        print(e)
    print("Start recording!avc")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    #try and catch
    client.connect(hostMQTT, port=portMQTT)
    client.subscribe(topic)
    print("before client!")
    #works blocking, other, non-blocking, clients are available too.
    client.loop_start()
    print("after client!")
    return "recordpage()"

###### MQTT stop here ###############
@app.route("/stop")
def stopMQTT():
    print("Stop recording")
    client.loop_stop()
    global RID
    # if statement
    if RID == 0L:
        print("stopped")
        return recordpage()
    # update endTime in the recording
    # 1) where is the RID stored? in the global variable called RID
    # 2) Take that RID, and do an update statement: update endTime = now where RecordingID = RID that was store
    now1 = datetime.datetime.now()
    sql = '''UPDATE recordings SET endTime = %s WHERE RecordingID = %s'''
    print("RID before stop=")
    print (RID)
    recordingData = (now1, RID)
    cur = conn.cursor()
    cur.execute(sql, recordingData)
    conn.commit()
    # clear RID and now1
    now1=None
    # RID = 0L
    return recordpage()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/saveVideo', methods=['GET', 'POST'])
def saveVideo():     
    # try:   
    global RID
    print("savevideo rid = ")
    print(RID)
    if request.method == 'POST':
        print("enter save video")
        filename = request.get_data()
            
        if filename == "exited":
            stopMQTT()
        else:
            print("file name from ajax: "+ request.files['file'].filename)
            file = request.files['file']
            sql = '''UPDATE recordings SET saveFile = %s WHERE RecordingID = %s'''
            print("Savefile = ")
            print(RID)
            print( file.filename)
            recordingData = ( file.filename, RID)
            cur = conn.cursor()
            cur.execute(sql, recordingData)
            conn.commit()
            if file:
                print("allowed file")
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER1, filename))
                return redirect(url_for('uploaded_file',
                                            filename=filename))
    # except Exception as e: 
    #     print("error catch = ")
    #     print(e)
    return render_template('replay.html')

@app.route("/replay")
def viewreplay():
    mycursor = conn.cursor()
    my_var = session.get('my_var', None)
    print("RID videos = ")
    print(my_var)
    my_var1 = session.get('my_var1', None)
    rid2 = my_var.decode('unicode-escape')
    mid = my_var1.decode('unicode-escape')
    hello =("SELECT saveFile FROM recordings WHERE RecordingID = %s")
    mycursor.execute(hello, [rid2])
    results = mycursor.fetchone()

    # video = "videos/" + results
    # print("result video =")
    # print(results[0])

    video = "videos/" + str(results[0])
    print("result video =")
    print(video)

    coord =("SELECT tagId,timestamp,coordinates_x,coordinates_y FROM projects WHERE RecordingID = %s")
    mycursor.execute(coord, [rid2])
    coords = mycursor.fetchall()

    my_var2 = session.get('my_var2', None)
    print("my_var2 = ")
    print(my_var2)
    mid2 = my_var2.decode('unicode-escape')
    print(mid2)
    matchdetail=("SELECT * FROM matches WHERE MatchID=%s")
    mycursor.execute(matchdetail, [mid2])
    matchNotes = mycursor.fetchall()
    print("matchnotes == ")
    print(matchNotes)


    matchdetails=("SELECT * FROM matchinfo WHERE MatchID=%s")
    mycursor.execute(matchdetails, [mid2])
    tagDetails = mycursor.fetchall()
    data1 = {'video': video, 'coords': coords, 'matchNotes': matchNotes, 'tagDetails' : tagDetails }
    return render_template('replay.html', data1 = data1)


@app.route('/videos/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER1,
                               filename)

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
#  print '"version":', result['version']
 version = result['version']
 print("{")
 print '"tagId":', result['tagId']
 tagId = result['tagId']

#  print '"success":', result['success']
 success = result['success']

 print '"timestamp":', result['timestamp']
 timestamp = result['timestamp']

#  print '"magnetic_x":', result['data']['tagData']['magnetic']['x']
 magnetic_x = result['data']['tagData']['magnetic']['x']

#  print '"magnetic_y":', result['data']['tagData']['magnetic']['y']
 magnetic_y = result['data']['tagData']['magnetic']['y']

#  print '"magnetic_z":', result['data']['tagData']['magnetic']['z']
 magnetic_z = result['data']['tagData']['magnetic']['z']

 print '"coordinates_x":', result['data']['coordinates']['x']
 coordinates_x = result['data']['coordinates']['x']

 print '"coordinates_y":', result['data']['coordinates']['y']
 coordinates_y = result['data']['coordinates']['y']

 print("},")
 

#  print '"coordinates_z":', result['data']['coordinates']['z']
 coordinates_z = result['data']['coordinates']['z']

#  print '"acceleration_x":', result['data']['acceleration']['x']
 acceleration_x = result['data']['acceleration']['x']

#  print '"acceleration_y":', result['data']['acceleration']['y']
 acceleration_y = result['data']['acceleration']['y']

#  print '"acceleration_z":', result['data']['acceleration']['z']
 acceleration_z = result['data']['acceleration']['z']

#  print '"yaw":', result['data']['orientation']['yaw']
 yaw = result['data']['orientation']['yaw']

#  print '"roll":', result['data']['orientation']['roll']
 roll = result['data']['orientation']['roll']

#  print '"pitch":', result['data']['orientation']['pitch']
 pitch = result['data']['orientation']['pitch']
 print("before point data creating")
#  create the point in database

 print("before point data creating - RID:"+str(RID))
 point = (version, tagId, RID, success, timestamp, magnetic_x, magnetic_y, magnetic_z, coordinates_x, coordinates_y, coordinates_z, acceleration_x, acceleration_y, acceleration_z, yaw, roll, pitch)
 print("After point data creating")
 create_point(point)

 return
 
def create_point(point):
    """
    Create a new point
    :param conn:
    :param point:
    :return:
    """
    print("123")
    print(point)
    sql = ''' INSERT INTO projects(version, tagId, RecordingID, success, timestamp, magnetic_x, magnetic_y, magnetic_z, coordinates_x, coordinates_y, coordinates_z, acceleration_x, acceleration_y, acceleration_z, yaw, roll, pitch)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
    cur = conn.cursor()
    try:
        print("insert Point")
        cur.execute(sql, point)
        conn.commit()
    except Exception as e: 
        print(e)
    
    return cur.lastrowid



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=8000)
