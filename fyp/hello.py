from flask import Flask
from flask import jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort, g
import os
from hashlib import md5
from sqlalchemy.orm import sessionmaker
import simplejson as json

import ssl
import json
import ctypes  # An included library with Python install.
import MySQLdb
import datetime
import time
import pymysql
import re
import csv
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
from flask import send_from_directory

from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS, PozyxRegisters, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister)
from pypozyx.tools.version_check import perform_latest_version_check
from threading import Thread

UPLOAD_FOLDER1 = 'static/videos'
CSV_FOLDER = 'static/students/'
POINTS_FOLDER = 'static/bbCourtHeat/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webm'])
ALLOWED_EXTENSIONS1 = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER1

# MySQL VRIABLES############################################
host = "172.20.129.227"
port = 3306
topic = "tagsLive" 
user = "admin1"
passwd="Sportapassword12"
db="Sportadb"
RID=0
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

        query2=("SELECT * FROM matchinfo WHERE MatchID=%s")
        mycursor.execute(query2,MID)
        players = mycursor.fetchall()

        print ("players")
        print (players)
        data = {'rowss': rowss, 'matchNotes': matchNotes[0], 'matchData': matchNotes, 'matchID': matchID, 'players': players}

        return render_template('match.html', data=data)
    else:
        return render_template('login.html')

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
        # cur1 = conn.cursor()
        # cur1.execute('SELECT student.studentName, teamstudent.teamId FROM student INNER JOIN teamstudent ON student.studentID = teamstudent.studentID')
        # playerListResult = cur1.fetchall()
        #print playerListResult
        cur2 = conn.cursor()
        cur2.execute('SELECT * FROM tags WHERE TagId IS NOT NULL')
        tagList = cur2.fetchall()
        # print tagList
        cur.close()
        cur2.close()
        return render_template('create-match.html', **locals())
    else:
        return redirect('/')

@app.route("/create-match/<team>")
def create_match_select(team):
    cur2 = conn.cursor()
    teamName = team
    #print "teamname in create match: "+teamName
    query = 'SELECT student.studentName FROM student INNER JOIN teamstudent ON student.studentID = teamstudent.studentID WHERE teamstudent.teamId = %s'
    cur2.execute(query, [teamName])
    playerNames = cur2.fetchall()
    #print playerNames
    cur2.close()
    return jsonify(playerNames)

@app.route("/createStudent/uploadStuds", methods = ['GET', 'POST'])
def upload_students():
    if request.method == 'POST':
        if 'studList' not in request.files:
            setStudentStatus(1, "No file selected. Please select a .csv file to upload.")
            return redirect('/students')
        file = request.files['studList']
        #if studFile.filename == '':
        #    flash('No selected file')
        #    return redirect('/students')
        if not allowed_csv(file.filename):
            setStudentStatus(1, "File selected is not a .csv file. Please select a .csv file to upload.")
            return redirect('/students')
        if file and allowed_csv(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(CSV_FOLDER, filename))
            # flash('New student list has been uploaded')
            return redirect(url_for('uploaded_csv',
                                            filename=filename))

@app.route("/createStudent/uploadBallers", methods = ['GET', 'POST'])
def upload_ballers():
    if request.method == 'POST':
        if 'ballList' not in request.files:
            setStudentStatus(1, "No file selected. Please select a .csv file to upload.")
            return redirect('/students')
        file = request.files['ballList']
        #if studFile.filename == '':
        #    flash('No selected file')
        #    return redirect('/students')
        if not allowed_csv(file.filename):
            setStudentStatus(1, "File selected is not a .csv file. Please select a .csv file to upload.")
            return redirect('/students')
        if file and allowed_csv(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(CSV_FOLDER, filename))
            # flash('New student list has been uploaded')
            return redirect(url_for('uploadedballer_csv',
                                            filename=filename))



def allowed_csv(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1

@app.route("/students/<filename>")
def uploaded_csv(filename):  
    CSV_LOCATION = CSV_FOLDER + filename
    sqlDrop = 'DROP TABLE IF EXISTS student'
    sqlCreate = '''CREATE TABLE student (studentID varchar(20) NOT NULL PRIMARY KEY, studentName varchar(50) NOT NULL, uploadedDTG DATETIME NOT NULL, uploadedBy varchar(50) NOT NULL)'''
    cur = conn.cursor()
    cur.execute(sqlDrop)
    cur.close()
    cur = conn.cursor()
    cur.execute(sqlCreate)
    cur.close()
    sqlDropTeam = 'DROP TABLE IF EXISTS teamstudent'
    sqlCreateTeam = '''CREATE TABLE teamstudent (teamId varchar(20) NOT NULL, studentID varchar(20) NOT NULL, PRIMARY KEY (studentID, teamId))'''
    cur = conn.cursor()
    cur.execute(sqlDropTeam)
    cur.close()
    cur = conn.cursor()
    cur.execute(sqlCreateTeam)
    cur.close()
    sqlDropTeamsTable = 'DROP TABLE IF EXISTS team'
    sqlCreateTeamsTable = '''CREATE TABLE team (teamId varchar(20) NOT NULL PRIMARY KEY, createdDTG DATETIME NOT NULL, createdBy varchar(50) NOT NULL)'''
    cur = conn.cursor()
    cur.execute(sqlDropTeamsTable)
    cur.close()
    cur = conn.cursor()
    cur.execute(sqlCreateTeamsTable)
    cur.close()
    # sqlDropTeamTable = 'DROP TABLE IF EXISTS team'
    with open(CSV_LOCATION) as newStudList:
        updatedStuds = csv.reader(newStudList, delimiter=',')
        lineNum = 0
        teamsInTable = ['Basketball']
        for row in updatedStuds:
            if lineNum <= 9:
                # print row
                lineNum += 1
            else:
                sqlPushStudents = "INSERT INTO student(studentID, studentName, uploadedDTG, uploadedBy) VALUES (%s, %s, %s, %s)"
                cur1 = conn.cursor()
                cur1.executemany(sqlPushStudents,[(row[5], row[6], datetime.datetime.now(), session['username'])]) # studentID, studentName columns in csv file
                sqlPushTeam = "INSERT INTO teamstudent(teamId, studentID) VALUES (%s, %s)"
                cur2 = conn.cursor()
                cur2.executemany(sqlPushTeam,[(row[1], row[5])]) # class, studentID columns in csv file
                conn.commit()
                if row[1] not in teamsInTable:
                    teamsInTable.append(row[1])
                print(teamsInTable[0])
        for teams in teamsInTable:
            print(teams)
            sqlPushTeamTable = "INSERT INTO team(teamId, createdDTG, createdBy) VALUES (%s, %s, %s)"
            cur3 = conn.cursor()
            cur3.executemany(sqlPushTeamTable,[(teams, datetime.datetime.now(), session['username'])])
            conn.commit()
    setStudentStatus(0, "New student list has been uploaded")
    cur1.close()
    cur2.close()
    cur3.close()
    return redirect("/students")

@app.route("/ballers/<filename>")
def uploadedballer_csv(filename):
    CSV_LOCATION = CSV_FOLDER + filename
    sqlDeleteBB = "DELETE FROM teamstudent WHERE teamId = 'Basketball'"
    cur1 = conn.cursor()
    cur1.execute(sqlDeleteBB)
    with open(CSV_LOCATION) as newBallerList:
        updatedStuds = csv.reader(newBallerList, delimiter=',')
        lineNum = 0
        for row in updatedStuds:
            if lineNum == 0:
                # print row
                lineNum += 1
            else:
                sqlPushTeam = "INSERT INTO teamstudent(teamId, studentID) VALUES (%s, %s)"
                cur2 = conn.cursor()
                cur2.executemany(sqlPushTeam,[(row[1], row[5])]) # class, studentID columns in csv file
                conn.commit()
    setStudentStatus(0, "New basketball team list has been uploaded")
    cur1.close()
    cur2.close()
    return redirect("/students")
 

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
                if (j[1] == i[0]):
                    if counterj is not 0:
                        inTeamsConcat = inTeamsConcat + ", "
                    inTeamsConcat = inTeamsConcat + j[0]
                    k.append(j[0])
                    counterj += 1
            rows.append((i[0], i[1], inTeamsConcat, i[2], i[3]))
            inTeams[i[1]] = k

        studentStatusType = session.get('studentStatusType')
        studentStatusMessage = session.get('studentStatusMessage')

        session['studentStatusType'] = ''
        session['studentStatusMessage'] = ''
        return render_template('student.html', **locals())
    else:
        return redirect('/')

def setStudentStatus(status, message):
    session['studentStatusType'] = status
    session['studentStatusMessage'] = message


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
        cur2 = conn.cursor()
        cur2.execute('SELECT * FROM tags')
        tags = cur2.fetchall()
        return render_template('tag.html', **locals())
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
    POST_tagNum = str(request.form['tagnum'])
    POST_tagid = str(request.form['tagid'])
    tagDecimal = int(POST_tagid, 16)
    updatetag = (tagDecimal, POST_tagNum)
    tag = "UPDATE tags SET TagId =%s WHERE TagNumber =%s"
    mycursor = conn.cursor()
    mycursor.execute(tag, updatetag)
    updatetime = (datetime.datetime.now(), POST_tagNum)
    tag1 = "UPDATE tags SET LastUpdated =%s WHERE TagNumber =%s"
    mycursor.execute(tag1, updatetime)
    try:
        conn.commit()
    except Exception as e: 
        print(e)
    mycursor.close()
    return tagpage()

@app.route('/createMatch', methods=['POST'])
def createMatch():
    # data from form
    POST_matchname = str(request.form['matchname'])
    POST_matchdate = str(request.form['matchdate'])
    POST_administrator = session['username']
    POST_matchnotes = str(request.form['matchnotes'])
    POST_courtsize = str(request.form['courtsize'])
    
    # create match data# 
    matchData = (POST_matchname, POST_matchdate, POST_administrator, POST_matchnotes, POST_courtsize)

    #SQL statement
    sql = ''' INSERT INTO matches(matchname, matchdate, administrator, matchnotes, courtsize)
              VALUES(%s,%s,%s,%s,%s) '''
              
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
    overlayQuery = 'INSERT INTO `sportadb`.`overlay` (`matchID`, `overlayData`) VALUES (%s, \'[]\');'

    insertPlayer = []
    for players in POST_allPlayers:
        if players[2] != "" and players[3] != "" and players[4] != "":
            insertPlayer.append(players)
    print(insertPlayer)

    curPost = conn.cursor()
    curPost.executemany(postingQuery, insertPlayer)
    curPost.execute(overlayQuery, [matchid])

    try:
        conn.commit()
    except Exception as e:
        print(e)

    return displayTable()

    

@app.route('/createStudent', methods=['POST'])
def createStudent():
    #SQL statement
    sql = ''' INSERT INTO teamstudent (`teamId`, `studentId`) 
              VALUES (%s, %s) '''
    sql2 = ''' INSERT INTO student (`studentId`, `studentName`, `uploadedDTG`, `uploadedBy`) 
               VALUES (%s, %s, %s, %s) '''
    sql3 = ''' UPDATE student SET `uploadedDTG` = %s, `uploadedBy` = %s WHERE (`studentId` = %s) '''

    try:          
        cur = conn.cursor()
        cur.execute(sql, ([str(request.form['teamId'])], [str(request.form['studentId'])]))

        cur.execute("select studentId from student where studentId = %s", [str(request.form['studentId'])])
        tmp = cur.fetchall()
        if tmp:
            cur.execute(sql3, (datetime.datetime.now(), session['username'], [str(request.form['studentId'])]))
            setStudentStatus(0, "The student that you are trying to add already exists. The student has been assigned to the team alongside the student's existing teams")
        else:
            cur.execute(sql2, ([str(request.form['studentId'])], [str(request.form['studentName'])], datetime.datetime.now(), session['username']))
            setStudentStatus(0, "The student has been successfully added and assigned to the team")
        conn.commit()
    except MySQLdb.IntegrityError as ie: # Student-Team pair is already found in database
            setStudentStatus(1, "The student that you are trying to add already exists and was already assigned into the given team")
    except Exception as e:
        print(e)
    return redirect('students')

@app.route('/editStudent/<studentId>/<studentName>', methods=['POST'])
def editStudent(studentId, studentName):
    sql = '''SELECT teamId FROM teamStudent WHERE (`studentId` = %s)'''
    sql2 = '''UPDATE student SET `studentName` = %s, `uploadedDTG` = %s, `uploadedBy` = %s WHERE (`studentId` = %s);'''
    sql3 = '''DELETE FROM teamstudent WHERE (`teamId` = %s) and (`studentId` = %s);'''

    cur = conn.cursor()
    cur.execute(sql, [studentId])
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
        setStudentStatus(1, "You are trying to remove the student from all assigned teams. The student needs to have at least one assigned team")
        return redirect('students')

    if not (str(request.form['editStudentName']) == studentName):
        cur.execute(sql2, ([str(request.form['editStudentName'])], datetime.datetime.now(), session['username'], studentId))
    
    for t in teams:
        try:
            if request.form[t[0]] == 'on':
                cur.execute(sql3, ([str(t[0])], studentId))
                cur.execute(sql2, (studentName, datetime.datetime.now(), session['username'], studentId))
        except BadRequestKeyError:
            print('') # Do nothing
    conn.commit()
    setStudentStatus(0, "The edits made to the student has been saved successfully")
    return redirect('students')

@app.route('/deleteStudent/<studentId>')
def deleteStudent(studentId):
    sql = '''DELETE FROM student WHERE (`studentId` = %s);'''
    sql2 = '''DELETE FROM teamstudent WHERE (`studentId` = %s);'''

    try:          
        cur = conn.cursor()
        cur.execute(sql, [studentId])
        cur.execute(sql2, [studentId])

        setStudentStatus(0, "The student has been removed from the teams that he or she is part of and was deleted successfully")
        conn.commit()
    except Exception as e: # Something went wrong
        setStudentStatus(1, "Unable to delete the student. Please try again later")
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
            print()
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

@app.route('/heat')
def heatmap():
    cur = conn.cursor()
    matches = ("SELECT DISTINCT matchID, matchname FROM matchinfo")
    cur.execute(matches)
    matchList = cur.fetchall()
    match = []
    for y in matchList:
        if y[0] not in match:
            match.append(y)
    return render_template('heatmap.html', **locals())

@app.route('/heat/<matchID>')
def getTagId(matchID):
    cur2 = conn.cursor()
    matchNum = matchID
    # print(matchNum)
    sqlTags = ("SELECT tagID, studentName FROM matchinfo WHERE matchID = %s")
    cur2.execute(sqlTags, [matchNum])
    tags = cur2.fetchall()
    # print(tags)
    cur2.close()
    return jsonify(tags)

@app.route('/heats/<matchID>')
def getRID(matchID):
    cur3 = conn.cursor()
    matchNum = matchID
    sqlRID = ("SELECT RecordingID FROM recordings WHERE Match_ID = %s")
    cur3.execute(sqlRID, [matchNum])
    rids = cur3.fetchall()
    print(rids)
    cur3.close()
    return jsonify(rids)


@app.route("/replay")
def viewreplay():
    mycursor = conn.cursor()
    my_var = session.get('my_var', None)
    print("RID videos = ")
    print(my_var)
    my_var1 = session.get('my_var1', None)
    rid2 = my_var
    mid = my_var1
    hello =("SELECT saveFile FROM recordings WHERE RecordingID = %s")
    mycursor.execute(hello, [rid2])
    results = mycursor.fetchone()

    # video = "videos/" + results
    # print("result video =")
    # print(results[0])

    video = "videos/" + str(results[0])
    print("result video =")
    print(video)

    


    my_var2 = session.get('my_var2', None)
    print("my_var2 = ")
    print(my_var2)
    mid2 = my_var2
    print(mid2)
    matchdetail=("SELECT * FROM matches WHERE MatchID=%s")
    mycursor.execute(matchdetail, [mid2])
    matchNotes = mycursor.fetchall()
    print("matchnotes == ")
    print(matchNotes)


    matchdetails=("SELECT * FROM matchinfo WHERE MatchID=%s")
    mycursor.execute(matchdetails, [mid2])
    tagDetails = mycursor.fetchall()


    coord =("SELECT tagId,timestamp,coordinates_x,coordinates_y FROM projects WHERE RecordingID = %s")
    mycursor.execute(coord, [rid2])
    coords = mycursor.fetchall()
    tagslist = []
    for y in coords:
        if y[0] not in tagslist:
            tagslist.append(y[0])
    print(tagslist)
    coordsData = [['tagId', 'timestamp', 'coordinates_x', 'coordinates_y']]
    for x in coords:
        coordsData.append(x)
    filename = 'coords.csv'
    coordFile = open(os.path.join(POINTS_FOLDER, filename), 'w', newline='')
    with coordFile as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(coordsData)
    
    csvFile.close()


    overlaySql = ("SELECT overlayData FROM overlay where matchID = %s")
    mycursor.execute(overlaySql, [mid2])
    overlays = mycursor.fetchall()
    overlays = overlays[0][0]

    data1 = {'video': video, 'coords': coords, 'matchNotes': matchNotes, 'tagDetails' : tagDetails }
    return render_template('replay.html', **locals())

@app.route('/overlay/<matchID>')
def overlay_page(matchID):
    sql = ("SELECT overlayData FROM overlay where matchID = %s")
    sql2 = ("SELECT courtsize FROM matches WHERE MatchID = %s")

    cur = conn.cursor()
    cur.execute(sql, [matchID])
    overlays = cur.fetchall()
    cur.execute(sql2, [matchID])
    isHalfCourt = cur.fetchall()

    overlays = str(overlays[0][0])
    isHalfCourt = str(isHalfCourt[0][0])

    return render_template('overlay.html', **locals())

@app.route('/saveOverlay', methods=['POST'])
def saveOverlay():
    sql = ("INSERT INTO overlay (`matchID`, `overlayData`) VALUES (%s, %s)")
    sql2 = ("UPDATE overlay SET `overlayData` = %s WHERE (matchID = %s);")

    cur = conn.cursor()
    try:
        cur.execute(sql, (request.form['matchID'], request.form['overlayData']))
    except MySQLdb.IntegrityError as ie:
        cur.execute(sql2, (request.form['overlayData'], request.form['matchID']))
    conn.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/videos/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER1,
                               filename)

def create_point(point):
    """
    Create a new point
    :param conn:
    :param point:
    :return:
    """
    #print("123")
    #print(point)
    sql = ''' INSERT INTO projects(tagId, RecordingID, timestamp, coordinates_x, coordinates_y)
              VALUES(%s,%s,%s,%s,%s) '''
    cur = conn.cursor()
    try:
        print("insert Point")
        cur.execute(sql, point)
        conn.commit()
    except Exception as e: 
        print(e)
    
    return cur.lastrowid

################################################ BEGIN POZYX CODE ################################################

# IDs of the tags to position, add None to position the local tag as well.
tag_ids = [0x697d, 0x6946, 0x6973, 0x6969, 0x6960, 0x6e65]

# necessary data for calibration
anchors = [DeviceCoordinates(0x6932, 1, Coordinates(0, 0, 0)),
            DeviceCoordinates(0x6e58, 1, Coordinates(7700, 0, 0)),
            DeviceCoordinates(0x6e10, 1, Coordinates(0, 5440, 0)),
            DeviceCoordinates(0x6e59, 1, Coordinates(7700, 5760, 0))]

# positioning algorithm to use, other is PozyxConstants.POSITIONING_ALGORITHM_TRACKING
algorithm = PozyxConstants.POSITIONING_ALGORITHM_TRACKING
# positioning dimension. Others are PozyxConstants.DIMENSION_2D, PozyxConstants.DIMENSION_2_5D
dimension = PozyxConstants.DIMENSION_3D
# height of device, required in 2.5D positioning
height = 1000

pozyxThread = None

global isRecording
isRecording = False

###### Start recording here ###############
@app.route("/start")
def startRecording():
    if get_first_pozyx_serial_port() is None:
        return json.dumps({'success':False, 'errorType':'NO_POZYX_CONNECTED'}), 200, {'ContentType':'application/json'}

    my_var1 = session.get('my_var1', None)
    mid1 = my_var1
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

    global isRecording
    isRecording = True
    pozyxThread = PozyxThread()
    pozyxThread.start()
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

###### Stop recording here ###############
@app.route("/stop")
def stopRecording():
    print("Stop recording")
    global isRecording
    isRecording = False
    global RID
    # if statement
    if RID == 0:
        print("stopped")
        return recordpage()
    # update endTime in the recording
    # 1) where is the RID stored? in the global variable called RID
    # 2) Take that RID, and do an update statement: update endTime = now where RecordingID = RID that was store
    now1 = datetime.datetime.now()
    sql = '''UPDATE recordings SET endTime = %s WHERE RecordingID = %s'''
    print("RID before stop=")
    print(RID)
    recordingData = (now1, RID)
    cur = conn.cursor()
    cur.execute(sql, recordingData)
    conn.commit()
    # clear RID and now1
    now1 = None
    # RID = 0L
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

class PozyxThread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)
        self.isRecording = True
        self.RID = RID
 
    def run(self):
        pozyx = PozyxSerial(get_first_pozyx_serial_port())

        global RID

        r = PozyxControl(pozyx, tag_ids, anchors, RID, algorithm, dimension, height)
        r.setup()

        while isRecording:
            r.loop()

class PozyxControl(object):
    """Continuously performs multitag positioning"""

    def __init__(self, pozyx, tag_ids, anchors, RID, algorithm=PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY,
                 dimension=PozyxConstants.DIMENSION_3D, height=1000):
        self.pozyx = pozyx

        self.tag_ids = tag_ids
        self.anchors = anchors
        self.RID = RID
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.x = 0
        self.y = 0

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")
        print(" - System will manually calibrate the tags")
        print("")
        print(" - System will then auto start positioning")
        print("")
        if None in self.tag_ids:
            for device_id in self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [None] + self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        print("")
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")

        self.setAnchorsManual(save_to_flash=False)

    def loop(self):
        """Performs positioning and prints the results."""
        for tag_id in self.tag_ids:
            position = Coordinates()
            status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=tag_id)
            if status == POZYX_SUCCESS:
                self.printPublishPosition(position, tag_id)
            #else:
                #self.printPublishErrorCode("positioning", tag_id)

    def printPublishPosition(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        # s = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}".format("0x%0.4x" % network_id,
        #                                                         position.x, position.y, position.z)
        #if position.x is not 0:
        #    self.x = position.x
        #if position.y is not 0:
        #    self.y = position.y
        #point = (tagId, RID, timestamp, coordinates_x, coordinates_y)
        point = (network_id, self.RID, time.time(), position.x, position.y)
        print(point)
        create_point(point)

    def setAnchorsManual(self, save_to_flash=False):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag_id in self.tag_ids:
            status = self.pozyx.clearDevices(tag_id)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag_id)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(anchors), remote_id=tag_id)
            # enable these if you want to save the configuration to the devices.
            if save_to_flash:
                self.pozyx.saveAnchorIds(tag_id)
                self.pozyx.saveRegisters([PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], tag_id)

            self.printPublishConfigurationResult(status, tag_id)

    def printPublishConfigurationResult(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.printPublishErrorCode("configuration", tag_id)

    def printPublishErrorCode(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, network_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, %s" %
                  (operation, "0x%0.4x" % network_id, self.pozyx.getErrorMessage(error_code)))
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))

################################################ END POZYX CODE ################################################

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=8000)
