# -*- coding: utf-8 -*-

import sys
import os
import flask

from flask import Flask
from flask import render_template
from sqlalchemy import create_engine

from flask import request
from flask import redirect
from flask import session

from datetime import datetime, date, time
from datetime import timedelta
import time

username = 'vzemskova_out'
passwd = 'products-ivr'
db_name = 'products'

engine = create_engine("mysql://" + username + ":" + passwd + "@projectswhynot.site:11459/" + db_name + "?charset=utf8",  pool_size=10, max_overflow=20, echo=True)

app = Flask(__name__)
if __name__ == "__main__":
    app.run()

app.secret_key = b'j_8e9w1mTMpBAZ7q3mO2/'
app.permanent_session_lifetime = timedelta(days=31)


@app.route("/welcome", methods=['GET','POST'])
def sign_in():

    all_users = get_all_users()
    
    cookies = session.get('cookies', default='')
    user_cookies = get_user_id(cookies)
    if cookies != '':
        for i in user_cookies:
            if cookies == i.get('cookies', ''):
                return redirect('/')
    
    memory = [{}]
    memory[0]['login'] = ''
    memory[0]['password'] = ''
    memory[0]['email'] = ''
    memory[0]['gender'] = '---'
    memory[0]['age'] = ''
    memory[0]['num_of_people'] = ''
    memory[0]['income'] = ''
    
    error = [{}]
    error[0]['login_error'] = ''
    error[0]['password_error'] = ''
    error[0]['email_error'] = ''
    
    if request.method == "POST":
        if request.form.get('person_agreed'):
            login = request.form['login']
            memory[0]['login'] = login
            if get_user_login(login) != []:
                error[0]['login_error'] = u'Пользователь с таким логином уже существует'
            password = request.form['password']
            memory[0]['password'] = password
            if len(password) < 8:
                error[0]['password_error'] = u'Пароль должен содержать не менее 8 символов'
            email = request.form['email']
            memory[0]['email'] = email
            if get_user_email(email) != []:
                error[0]['email_error'] = u'Пользователь с такой почтой уже существует'
            gender = request.form['gender']
            memory[0]['gender'] = gender
            age = request.form['age']
            memory[0]['age'] = age
            if age == '':
                age = 'не указан'
            num_of_people = request.form['num_of_people']
            memory[0]['num_of_people'] = num_of_people
            if num_of_people == '':
                num_of_people = 1
            income = request.form['income']
            memory[0]['income'] = income
            if income == '':
                income = 'не указано'
            
            if error[0]['login_error'] == '' and error[0]['password_error'] == '' and error[0]['email_error'] == '':
                if len(all_users) > 0:
                    user_id = int(all_users[-1].get('user_id')) + 1
                else:
                    user_id = 1
                memo = 1
                memo_day = 0
                alert = 1
                days_before_alert = 0
                photo = 'basic.jpg'

                add_user(user_id, password, login, email, gender, age, num_of_people, income, memo, memo_day, alert, days_before_alert, photo)
                return redirect('/log_in')
    return render_template('sign_in.html', 
                                                saved_answers=memory,
                                                error_alert = error,
                          )

def get_all_users():
    connection = engine.connect()
    users_table = connection.execute("select * from user_ivr")
    connection.close()
    all_users = [dict(row) for row in users_table]
    return all_users

def get_user_id(cookies):
    connection = engine.connect()
    user_table = connection.execute("select * from user_cookies where cookies=%s", cookies)
    connection.close()
    user = [dict(row) for row in user_table]
    return user

def get_user_login(login):
    connection = engine.connect()
    user_table = connection.execute("select * from user_ivr where login=%s", login)
    connection.close()
    user = [dict(row) for row in user_table]
    return user

def get_user_email(email):
    connection = engine.connect()
    user_table = connection.execute("select * from user_ivr where email=%s", email)
    connection.close()
    user = [dict(row) for row in user_table]
    return user

def add_user(user_id, password, login, email, gender, age, num_of_people, income, memo, memo_day, alert, days_before_alert, photo):
    connection = engine.connect()
    trans = connection.begin()
    connection.execute("INSERT INTO user_ivr(user_id, password, login, email, gender, age, num_of_people, income, influence, memo, memo_day, alert, days_before_alert, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s, %s, %s, %s)", (user_id, password, login, email, gender, age, num_of_people, income, memo, memo_day, alert, days_before_alert, photo))
    trans.commit()
    connection.close()
    return
