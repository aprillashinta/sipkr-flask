from flask import request, render_template, redirect, url_for, session

def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'admin' and password == 'admin':
        session['user'] = username
        return redirect(url_for('web.dashboard'))

    return render_template('login.html', error='Username atau password salah')
