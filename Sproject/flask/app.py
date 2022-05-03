# import flask libries
from os import abort
from flask import Flask, render_template, session, redirect, request
from flask_mail import Mail, Message
from config import mail_username, mail_password
from flask_sqlalchemy import SQLAlchemy  # model of database
from datetime import datetime
from flask_admin import Admin  # model for admin department
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)


# connect database url in folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order.db'
# import os os.urandom(12).hex()
app.config['SECRET_KEY'] = 'd80db4dbd59c47883067c672'
db = SQLAlchemy(app)

# gmail access
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info.alsalamforlivestock@gmail.com'
app.config['MAIL_PASSWORD'] = '167obifeblake2020Abada'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# classs for order
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(50), nullable=False)
    numberp = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(400), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # return string format
        return '<Name %r>' % self.name

# classs for Contact


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(400), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # return string format
        return '<Name %r>' % self.name


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rev_name = db.Column(db.String(70), nullable=False)
    rev_msg = db.Column(db.String(400), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # return string format
        return '<Name %r>' % self.name

# secure admin page not allow user to enter


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

# admin view
app.config['FLASK_ADMIN_SWATCH'] = 'Slate'
admin = Admin(app, name='AlSalam Admin', template_mode='bootstrap3')
admin.add_view(SecureModelView(Order, db.session))
admin.add_view(SecureModelView(Contact, db.session))
admin.add_view(SecureModelView(Reviews, db.session))

# home page
@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/product', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        rev_name = request.form['rev_name']
        rev_msg = request.form['rev_msg']
        new_rev = Reviews(rev_name=rev_name,
                          rev_msg=rev_msg)
        db.session.add(new_rev)
        db.session.commit()
        return redirect('/product')
    else:
        all_rev = Reviews.query.order_by(Reviews.date_added).all()
        return render_template("product.html", posts=all_rev)


# admin login popout form
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.form.get("username") == "walidkhaled" and request.form.get("password") == "walid":
            session['logged_in'] = True
            return redirect("/adminv")
        else:
            return render_template("index.html", failed=True)
    return render_template("index.html")

# page admin
@app.route('/adminv')
def adminv():
    return render_template('adminv.html')




# logout admin
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# show product page
"""
route get and post data;
get data from add.html by user;
post data to email and database sqlite;
autoemail to user email;
"""
# page is  not found error
@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        user_phone = request.form['phone']
        user_country = request.form['country']
        user_product = request.form['product']
        user_numberp = request.form['numberp']
        user_message = request.form['message']
        # insert to database
        new_user = Order(name=user_name, email=user_email,
                         phone=user_phone, country=user_country, product=user_product, numberp=user_numberp, message=user_message)
        db.session.add(new_user)
        db.session.commit()
        # email
        message = Message(
            subject=f"Client Order From : {user_name}",
            body=f"Client Name : {user_name}\n\n Client E-mail : {user_email}\n\n Client Phone :{user_phone} \n\nClient Located : {user_country} \n\nClient Product : {user_product} \t{user_numberp} \n\n\nClient Message : {user_message}",
            sender='info.alsalamforlivestock@gmail.com',
            recipients=['info.alsalamforlivestock@gmail.com'])
        automessage = Message(
            subject=f"Automatic Message AlSalam CO",
            body=f"Dear: {user_name}\n Your registration file is in our team right now we will reply to you as soon as possible \n Thank You \nBy Al Salam For LiveStock",
            sender='info.alsalamforlivestock@gmail.com',
            recipients=[user_email])

        mail.send(message)
        mail.send(automessage)

        return redirect('/product')
    else:
        # in case we want to show data
        all_user = Order.query.order_by(Order.date_added).all()
        return render_template('product.html', user=all_user)


"""
route get and post data;
get data from index.html input user;
post email automatic tp user and data to server
return success messsage
"""


@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        new_contact = Contact(name=name, email=email,
                              message=msg)
        db.session.add(new_contact)
        db.session.commit()

        message = Message(
            subject=f"Mail from {name}",
            body=f"Name: {name}\nE-Mail: {email}\n\n\n{msg}",
            sender='info.alsalamforlivestock@gmail.com',
            recipients=['info.alsalamforlivestock@gmail.com'])
        automessage = Message(
            subject=f"Automatic Message",
            body=f"Dear: {name}\n We will reply to you as soon as possible \n Thank You \n Al Salam For LiveStock",
            sender='info.alsalamforlivestock@gmail.com',
            recipients=[email])

        mail.send(message)
        mail.send(automessage)
        success = 'Message send'
        return render_template('index.html', success=success)


# page is  not found error
@app.errorhandler(404)
def invalid_404(e):
    return render_template('404.html')

# forbidden page not allowed


@app.errorhandler(403)
def invalid_403(e):
    return render_template('404.html')

# Internal Server Error connection overload


@app.errorhandler(500)
def invalid_500(e):
    return render_template('500.html')

# page is  not found error
@app.errorhandler(400)
def invalid_400(e):
    return render_template('404.html')


# control over script’s behavior
if __name__ == '__main__':
    app.debug = True  # show error in webpage
    app.run()
