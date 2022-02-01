from DBcm import *


def mail_cheker(dbconfig) -> list:
    with UseDataBase(dbconfig) as cursor:
        _SQL = """SELECT mail FROM mail_subscribes"""
        cursor.execute(_SQL)
        return cursor.fetchall()


def mail_subscribes(dbconfig, mail: str) -> str:
    """subscribe db"""

    if mail:
        with UseDataBase(dbconfig) as cursor:

            # Проверяет наличие логина пользователя в базе данных
            _SQL = """SELECT * FROM mail_subscribes WHERE mail = (%s)"""
            cursor.execute(_SQL, (mail, ))
            resultReg = cursor.fetchall()

            if resultReg:
                return "Пользователь с такой почтой уже существует!"
            else:
                _SQL = """INSERT INTO mail_subscribes (mail) VALUES (%s)"""
                cursor.execute(_SQL, (mail, ))
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
            cursor.execute(_SQL, (mail, ))
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
            cursor.execute(_SQL, (mail, ))
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