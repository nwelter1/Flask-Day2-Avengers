from phonebook import app, db, Message, mail
from flask import render_template, request, redirect, url_for
from phonebook.forms import AvengerInfoForm, AvengerRegisterForm, LoginForm
from phonebook.models import User, Info, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user

#Home route
@app.route('/')
def home():
    contacts=Info.query.all()
    return render_template('home.html', contacts=contacts)

#Add route for posting
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

# retrieve
@app.route('/contacts/<int:contact_id>')
@login_required
def contact_detail(contact_id):
    contact = Info.query.get_or_404(contact_id)
    return render_template('contact_detail.html', contact=contact)

# updating
@app.route('/contacts/update/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def contact_update(contact_id):
    contact = Info.query.get_or_404(contact_id)
    update_form = AvengerInfoForm()

    if request.method == 'POST' and update_form.validate():
        name = update_form.name.data
        email = update_form.email.data
        phone_number = update_form.phone_number.data
        address = update_form.address.data
        user_id = current_user.id

        # update post with form info
        contact.name = name
        contact.email = email
        contact.phone_number = phone_number
        contact.address = address
        contact.user_id = user_id

        #Commit change to db
        db.session.commit()
        return redirect(url_for('contact_update', contact_id=contact.id))
    return render_template('contact_update.html', update_form=update_form)

#deleting
@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def contact_delete(contact_id):
    contact = Info.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('home'))


#registering
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