from main import session, app
from DBcm import UseDataBase
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading
from mailform import formathtml


def login_user(mail: str, password: str):
    """Проводит операции с логином и паролем пользователя"""
    if len(mail.split("@")) < 2:
        return ("Неккоректная почта")

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
    if len(mail.split("@")) < 2:
        return ("Неккоректная почта")

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


def mail_selecter() -> list:
    with UseDataBase(app.config["dbconfig"]) as cursor:
        _SQL = """SELECT mail FROM mail_subscribes"""
        cursor.execute(_SQL)
        yield cursor.fetchall()


def mail_subscribes(mail: str) -> str:
    """subscribe db"""

    if len(mail.split("@")) < 2:
        return ("Неккоректная почта")

    if mail:
        with UseDataBase(app.config["dbconfig"]) as cursor:

            # Проверяет наличие логина пользователя в базе данных
            _SQL = """SELECT * FROM mail_subscribes WHERE mail = (%s)"""
            cursor.execute(_SQL, (mail, ))
            resultReg = cursor.fetchall()

            if resultReg:
                return "Пользователь с такой почтой уже существует!"
            else:
                _SQL = """INSERT INTO mail_subscribes (mail) VALUES (%s)"""
                cursor.execute(_SQL, (mail, ))
                start_sending("Спасибо, что подписались на рассылку!", "Искренне ваши LIVINGSTONE", 
                              "Подписка на рассылку", file=None, port=587, user_mail=mail)
                return "Вы подписались на рассылку!"
    else:
        return "Заполните поле"


def message_sender(title: str, text: str, message_theme: str, file=None, port=587, user_mail=None) -> None:
    smtp_server = smtplib.SMTP("smtp.gmail.com", port)
    smtp_server.ehlo()
    smtp_server.starttls()
    msg = MIMEMultipart()
    msg["From"] = "LIVINGSTONE"
    msg["Subject"] = message_theme
    msg.attach(MIMEText(formathtml(title, text), "html"))
    if file:
        msg.attach(MIMEText(file, "pdf"))

    if user_mail:
        try:
            smtp_server.login(os.getenv("mailname"), os.getenv("mailpasswd"))
            smtp_server.sendmail(os.getenv("mailname"), user_mail, msg.as_string())
            time.sleep(1 / 100)
            print(f"Mail sended to: {user_mail}")

            smtp_server.close()
        except Exception as err:
            print("Что-то пошло не так: ", err)
    else:
        try:
            smtp_server.login(os.getenv("mailname"), os.getenv("mailpasswd"))
            for usermail in mail_selecter():
                smtp_server.sendmail(os.getenv("mailname"), usermail,
                                    msg.as_string())
                time.sleep(1 / 100)
                print(f"Mail sended to: {usermail}")

            smtp_server.close()
        except Exception as err:
            print("Что-то пошло не так: ", err)


def start_sending(title: str, text: str, message_theme: str, file=None, port=587, user_mail=None) -> None:
    threading.Thread(target=message_sender, args=(title, text, message_theme, file, port, user_mail)).start()
    print("Запуск потока:")
