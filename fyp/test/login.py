from flask import Flask, make_response
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

app = Flask(__name__)


import sqlite3,time

@app.route("/login")
def login():
    while True:
        username=input("Please enter your username: ")
        password=input("Please enter your password: ")
        with sqlite3.connect("Quiz.db") as db:
            cursor=db.cursor()
        find_user = ("SELECT * FROM USER WHERE username = ? AND password = ?")
        cursor.execute(find_user,[(username),(password)])
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Welcome "+i[2])
             #return("exit")
                break

        else:
            print("Username and password not recognised")
            again = input ("Do you want to try again? (y/n): ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                #reutrn("exit")
                break
if __name__ == "__main__":
    app.run(debug=True)             

@app.route("/users")
def newUser():
    found = 0
    while found == 0:
        username = input("Please enter a username: ")
        with sqlite3.connect("Quiz.db") as db:
            cursor=db.cursor()
        find_user = ("SELECT * FROM USER WHERE username =?")
        cursor.execute(find_user,[(username)])

        if cursor.fetchall():
            print("Username Taken, please try again")
        else:
            found = 1

    firstName = input("Enter your first name: ")
    surname = input ("Enter your surname: ")
    password = input ("Please enter your password: ")
    password1 = input ("Please reenter your password: ")
    while password !=password1:
        print ("Your passsword didn't match, please try again")
        password = input ("Please enter your password: ")
        password1 = input ("Please reenter your password: ")
    insertData='''INSERT INTO USER(username,firstname,surname,password) 
    VALUES(?,?,?,?)'''
    cursor.execute(insertData,[(username),(firstName),(surname),(password)])
    db.commit()
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/menu")
def menu():
    while True:
        print ("Welcome to my system ")
        menu=("""
        1 - create new user
        2 - login to system
        3 - Exit system\n""")

        userChoice = input(menu)

        if userChoice =="1":
            newUser()
        elif  userChoice=="2":
            login()
        elif userChoice=="3":
            print("Goodbye")
            SystemExit()
        else:
            print("command not recognised: ")

if __name__ == "__main__":
    app.run(debug=True)



