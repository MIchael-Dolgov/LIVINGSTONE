from flask import render_template, Flask, session, request, redirect
from stocks import show_stocks
from checkLogged import check_logged_in, user_status
from DBcm import UseDataBase, DataBaseError
import os
from DBactions import *

app = Flask(__name__)

app.config["dbconfig"] = {"host": os.getenv("dbhostname"),
                          "user": os.getenv("dbusername"),
                          "password": os.getenv("dbpassword"),
                          "database": os.getenv("dbname"), }

stockinfo = show_stocks()


def mail_scheker() -> list:
    with UseDataBase(app.config["dbconfig"]) as cursor:
        _SQL = """SELECT mail FROM mail_subscribes"""
        cursor.execute(_SQL)
        return cursor.fetchall()


def mail_subscribes(mail: str) -> str:
    """subscribe db"""

    if mail:
        with UseDataBase(app.config["dbconfig"]) as cursor:

            # Проверяет наличие логина пользователя в базе данных
            _SQL = """SELECT * FROM mail_subscribes WHERE mail = (%s)"""
            cursor.execute(_SQL, (mail,))
            resultReg = cursor.fetchall()

            if resultReg:
                return "Пользователь с такой почтой уже существует!"
            else:
                _SQL = """INSERT INTO mail_subscribes (mail) VALUES (%s)"""
                cursor.execute(_SQL, (mail,))
                return "Вы подписались на рассылку!"
    else:
        return "Заполните поле"


def login_user(mail: str, password: str):
    """Проводит операции с логином и паролем пользователя"""
    if "logged_in" in session:
        return "Вы уже вошли в аккаунт"

    if mail and password:
        with UseDataBase(app.config["dbconfig"]) as cursor:

            # Проверяет наличие логина пользователя в базе данных
            _SQL = """SELECT * FROM users WHERE mail = (%s)"""
            cursor.execute(_SQL, (mail,))
            resultLog = cursor.fetchall()

            # Проверяет правильность пароля к логину
            if resultLog:
                _SQL = f"""SELECT name FROM users WHERE mail = '{mail}'
                    AND password = '{password}'"""
                cursor.execute(_SQL)
                user = cursor.fetchall()

                if user:
                    # resent name of user
                    session["logged_in"] = user[0][0]
                    return "Вы авторизованы!"

                else:
                    return "Неверный пароль!"

            else:
                return "Такого пользователя не существует"
    else:
        return "Заполните все поля"


def register_user(mail: str, name: str, password: str):
    """Create new user account"""
    if "logged_in" in session:
        return "Вы уже вошли в аккаунт"

    if mail and password and name:
        with UseDataBase(app.config["dbconfig"]) as cursor:

            # Проверяет наличие логина пользователя в базе данных
            _SQL = """SELECT * FROM users WHERE mail = (%s)"""
            cursor.execute(_SQL, (mail,))
            resultReg = cursor.fetchall()

            if resultReg:
                return "Пользователь с такой почтой уже существует!"
            else:
                _SQL = """INSERT INTO users (mail, password, name) VALUES (%s, %s, %s)"""
                cursor.execute(_SQL, (mail, password, name))
                session["logged_in"] = name
                return "Вы создали аккаунт!"
    else:
        return "Заполните все поля"


@app.route('/', methods=['POST', 'GET'])
def mainpage():
    return render_template("main.html",
                           the_title="LIVINGSTONE",
                           the_stocks=f"{stockinfo}",
                           the_user_status=user_status())


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    return render_template("contact.html",
                           the_title="Contact",
                           the_stocks=f"{stockinfo}")


@app.route('/services', methods=['GET'])
def services():
    pass


@app.route('/analytics', methods=['GET'])
def analytics():
    pass


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


@app.route('/analytics/<number_of_post>')
def post_analytics():
    pass


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html",
                           the_title="login")


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


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("register.html",
                           the_tittle="register")


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


@app.route('/logout')
@check_logged_in
def logout():
    session.pop("logged_in")
    return "Вы вышли из аккунта"


@app.route('/admin')
@check_logged_in
def adminpanel():
    pass


app.secret_key = os.getenv("flask_secret_key")


if __name__ == '__main__':
    app.run(debug=True, port=4343)
