import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from DBactions import mail_selecter
import threading

#=================Your html form=================#


def formathtml(title: str, text,) -> str:
    html = """
    <!doctype html>
    <html>
        <head>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                }

                .header {
                    font-family: 'Cormorant Garamond', serif;
                    background-color: #000;
                    width: 100%;
                    margin-bottom: 10px;
                    text-align: center;
                }

                .header a{
                    margin: 0px auto;
                    font-size: 50px;
                    text-decoration: none;
                    color: #fff;
                }
                
                .maininfo {
                    text-align: center;
                    margin: 0 auto;
                    width: 80%;
                    font-size: 22px;
                }
                
                .maininfo h2 {
                    margin-bottom: 30px; 
                    margin-top: 5px;
                }

                .pp {
                    font-family: "Jost", sans-serif;
                    color: #fff; 
                    font-size:22px;
                }
                
                .footer {
                    margin-top: 30px;
                }

                .footer-bottom{
                    font-family: "Jost", sans-serif;
                    padding: 8px;
                    text-align: center;
                    background-color: #000;
                    color: #fff;
                }
                .pre-footer{
                    padding-top: 8px;
                    padding-bottom: 8px;
                    text-align: center;
                    width: 100%;
                    background-color: rgb(46, 45, 45);
                }
                .pre-footer a{
                    margin-top: 5px;
                    font-size: 20px;
                    color: rgba(255, 255, 255, 0.719);
                    margin: 10px 10px;
                }
                .footer-bottom p{
                    color: #fff;
                    margin: 10px 10px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <a href="#">LIVINGSTONE</a>
            </div>
            <div class="maininfo"i>
                <h2>""" + title + """</h2>
                """ + text + """"
            </div>
            <div class="footer">
                <div class="pre-footer">
                    <p class=pp>Возникли вопросы? Напишите нам!</p>
                    <a class="maillink" href="mailto:team@livingstoneinvest.com">team@livingstoneinvest.com</a>
                </div>
                <div class="footer-bottom">
                    <p>copyright &copy;2022 LIVINGSTONE. Designed by <span>Michael Dolgov</span></p>
                </div>
            </div>
        </body>
    </html>
    """
    return html


#=================End html form=================#


def message_sender(title: str, text: str, message_theme: str, file=None, port=587,) -> None:
    smtp_server = smtplib.SMTP("smtp.gmail.com", port)
    smtp_server.ehlo()
    smtp_server.starttls()
    msg = MIMEMultipart()
    msg["From"] = "LIVINGSTONE"
    msg["Subject"] = message_theme
    msg.attach(MIMEText(formathtml(title, text), "html"))
    if file:
        msg.attach(MIMEText(file, "pdf"))

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


def start_sending(title: str, text: str, message_theme: str, file=None, port=587,) -> None:
    threading.Thread(target=message_sender, args=(title, text, message_theme, file, port,)).start()
    print("Запуск потока:")

