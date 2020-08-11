from phonebook import app
from flask import render_template, request
from phonebook.forms import AvengerInfoForm

#Home route
@app.route('/')
def home():
    return render_template('home.html')

#Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AvengerInfoForm()
    if request.method =='POST':
        name = form.name.data
        email = form.email.data
        phone_number = form.phone_number.data
        address = form.address.data
        print("\n",name, email, phone_number, address)
    return render_template("register.html", form=form)