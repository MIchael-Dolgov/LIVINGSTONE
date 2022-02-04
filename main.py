from flask import render_template, Flask, session, request
from stocks import stockinfo
from checkLogged import check_logged_in, user_status, check_logged_in_for_admin
from DBcm import DataBaseError
from DBactions import *
import os

app = Flask(__name__)

app.config["dbconfig"] = {
    "host": os.getenv("dbhostname"),
    "user": os.getenv("dbusername"),
    "password": os.getenv("dbpassword"),
    "database": os.getenv("dbname"),
}


#==============Main page===================#
@app.route('/', methods=['POST', 'GET'])
def mainpage():
    return render_template("main.html",
                           the_title="LIVINGSTONE",
                           the_stocks=f"{stockinfo}",
                           the_user_status=user_status())


#==============Base===================#


@app.route('/mailsender', methods=["POST"])
def mailsender():
    mail = request.form["mail"]
    try:
        user = mail_subscribes(mail)
        return user
    except DataBaseError as err:
        print("База данных выключена")
    except Exception as err:
        print("Непредвиденное исключение: ", str(err))
    return "Что-то пошло не так"


#==================Contact================#


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    return render_template("contact.html",
                           the_title="Contact",
                           the_stocks=f"{stockinfo}",
                           the_user_status=user_status())


@app.route('/contactus', methods=["POST"])
def contactus():
    name = request.form["name"]
    mail = request.form["mail"]
    phone = request.form["phone"]
    details = request.form["details"]
    rdy_msg = f"Номер телефона: {phone} \n {details}"
    try:
        user = start_sending(mail, rdy_msg, name, user_mail=os.getenv("mailname"))
        return "Good"
    except DataBaseError as err:
        print("База данных выключена")
    except Exception as err:
        print("Непредвиденное исключение: ", str(err))
    return "Что-то пошло не так"

#===================Services=============#


@app.route('/services', methods=['POST', 'GET'])
def services():
    return render_template("services.html",
                           the_title="Services",
                           the_stocks=f"{stockinfo}",
                           the_user_status=user_status())


#================Analytics===========+#

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template("analytics.html",
                           the_title="Analytics",
                           the_stocks=f"{stockinfo}",
                           the_user_status=user_status())

@app.route('/analytics/<number_of_post>')
def post_analytics():
    pass

#============================+======+#

#==============Login=============+#

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html", the_title="login")


@app.route('/auth', methods=["POST"])
def auth_login():
    mail = request.form["mail"]
    password = request.form["password"]
    try:
        user = login_user(mail, password)
        return user
    except DataBaseError as err:
        print("База данных выключена")
    except Exception as err:
        print("Непредвиденное исключение: ", str(err))
    return "Что-то пошло не так"


@app.route('/logout')
@check_logged_in
def logout():
    session.pop("logged_in")
    return "Вы вышли из аккунта"


#==================Registration===================#


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("register.html", the_tittle="register")


@app.route('/registration', methods=['POST'])
def registration():
    mail = request.form["mail"]
    name = request.form["name"]
    password = request.form["password"]
    try:
        user = register_user(mail, name, password)
        return user
    except DataBaseError as err:
        print("База данных выключена")
    except Exception as err:
        print("Непредвиденное исключение: ", str(err))
    return "Error"


#=======================#


@app.route('/admin')
@check_logged_in_for_admin
def adminpanel():
    pass


app.secret_key = os.getenv("flask_secret_key")

if __name__ == '__main__':
    app.run(debug=True, port=4343)
