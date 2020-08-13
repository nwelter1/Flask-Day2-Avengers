from phonebook import app, db, Message, mail
from flask import render_template, request, redirect, url_for
from phonebook.forms import AvengerInfoForm, AvengerRegisterForm, LoginForm
from phonebook.models import User, Info, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user

#Home route
@app.route('/')
def home():
    return render_template('home.html')

#Add route
@app.route('/addcontact', methods=['GET', 'POST'])
@login_required
def addcontact():
    form = AvengerInfoForm()
    if request.method =='POST' and form.validate():
        name = form.name.data
        email = form.email.data
        phone_number = form.phone_number.data
        address = form.address.data
        print("\n",name, email, phone_number, address)
        content = Info(name, email, phone_number, address, user_id=current_user.email)
        db.session.add(content)
        db.session.commit()
    return render_template("addcontact.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AvengerRegisterForm()
    if request.method =='POST' and form.validate():
        # Get Information
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n",username, password, email)

        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        
        msg = Message(f"Thanks for signing up, {username}!", recipients=[email])
        msg.body = ('Congrats on signing up! Looking forward to adding your submissions to the phonebook!')
        msg.html = ('<h1>Welcome to the Avengers Phonebook!</h1>' '<p>Excited to connect you with other Avengers!</p>')

        mail.send(msg)
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method =='POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))