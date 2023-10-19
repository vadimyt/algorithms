import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header

def send_email(recipients_emails: list, msg_text: str):
    pwr=open(r'mail\Password.txt', "r", encoding='utf-8')
    ml=open(r'mail\Mail.txt', "r", encoding='utf-8')
    login=ml.readline()
    password=pwr.readline()
    pwr.close()
    ml.close()

    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = Header('Промежуточная аттестация', 'utf-8')
    msg['From'] = login
    msg['To'] = ', '.join(recipients_emails)

    server=smtplib.SMTP("smtp.yandex.ru", 587, timeout=10)

    try:
        server.starttls()
        server.login(login,password)
        server.sendmail(msg['From'], recipients_emails, msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        server.quit()

def main():
    send_email(recipients_emails=[], msg_text='Test')

if __name__ == "__main__":
    main()