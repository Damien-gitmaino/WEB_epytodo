from flask import Flask
from flask import Flask, render_template, redirect, url_for, request, Blueprint
from .ges_sql import *
from app import app
import json

@app.route('/create', methods = ['GET', 'POST'])
def create_client():
    error = None
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        if name == '' or password == '':
            error = 'Your name or password is missing. Please try again.'
        elif recup_pass("user", name) != None:
            error = 'This username already exists. Please try again.'
        else:
            add_info_db_user(0, str(name), str(password))
            return redirect(url_for('login'))
    return render_template('create.html', error=error)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        if password != recup_pass("user", name):
            error = 'Error username or password. Please try again.'
        else:
            return redirect(url_for('home', username=name))
    return render_template('login.html', error=error)

@app.route('/user/<username>/create_task', methods = ['GET', 'POST'])
def create_task(username):
    error = None
    if request.method == 'POST':
        user_id = recup_id_user(username)
        name = request.form['name']
        status = request.form['status']
        date = request.form['date_end']
        if name == '' or status == '' or date == '':
            error = 'Your name or status is missing. Please try again.'
        else:
            add_info_db_task(name, date, status, user_id)
            return redirect(url_for('home', username=username))
    return render_template('create_task.html', error = error,
                                                username = username)

@app.route('/user/<username>/account', methods = ['GET', 'POST'])
def account(username):  
    password = recup_pass("user", username)
    error = None
    if request.method == 'POST':
        new_name = request.form['username']
        new_password = request.form['password']
        if new_name == username and new_password == password:
            error = "The account data was not changed. Please try again."
        elif new_name == '' or new_password == '':
            error = 'Your name or password is missing. Please try again.'
        else:
            change_account_data(str(new_password), str(new_name), str(username))
            return redirect(url_for('home', username = new_name))
    return render_template('account.html', title = "account of " + username,
                                        username = username,
                                        password = password,
                                        error = error)

@app.route('/user/<username>/change_task/<name_task>', methods = ['GET', 'POST'])
def change_task(username, name_task, id_task):
    error = None
    i = get_info_task(1)
    name_task = i.get("title")
    end_date = i.get("end")
    status = i.get("status")
    if request.method == 'POST':
        new_name = request.form.name
        new_end_date = request.form.date_end
        new_status = request.form.status
        if new_name == '' or end_date == '' or new_status == '':
            error = 'Your name or status is missing. Please try again.'
        elif name_task == new_name and new_end_date == end_date and new_status == status:
            error = "The task data was not changed. Please try again."
        else:
            return redirect(url_for('home', username = username))
    return render_template('change_taretsk.html', error = error,
    last_name = name_task, last_date_end = end_date, last_statue = status)

@app.route('/user/<username>/delete_login', methods = ['GET'])
def delete_login(username):
    user_id = recup_id_user(username)
    delete_ligne_table_user(user_id)
    return redirect(url_for('login'))

@app.route('/user/<username>', methods = ['GET'])
def home(username):
    res = get_id_user_task(recup_id_user(username))
    i = 0
    tab = 580 * [None]
    if res != None:
        for cle in res.values():
            task = get_info_task(cle)
            if task != None:
                for lij in task.values():
                    tab[i] = lij
                    i = i + 1
    tab[i] = None
    return render_template('user.html', title = "Task of " + username,
                                        task = "Welcome " + username,
                                        username = username, tab = tab)
