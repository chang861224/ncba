import smtplib
from email.mime.text import MIMEText

def sendmail(address, eventid, randomkey):
    gmail_user = 'nccuncba@gmail.com'
    #gmail_user = 'chihung861224@gmail.com'
    gmail_password = 'njnfoccpqevtkhmq'
    #gmail_password = 'pqdosvqsjwiimjfs'
    content = '''
    你好，

    感謝參加政大棒球聯盟的投票活動，此為驗證程序之郵件，請點擊連結（ https://ncba.herokuapp.com/mail/vote/{}/{}/ ）或將此連結複製至瀏覽器上，以完成驗證程序。

    請注意！若未完成驗證程序，投票動作仍尚未完成，票數仍不會列數計算！
    若要重新投票，請勿點選此連結，再去聯盟網站重新投票即可！

    政大棒球聯盟

    （此郵件為系統發送，勿直接回覆！謝謝！）
    '''.format(eventid, randomkey)

    msg = MIMEText(content)
    msg['Subject'] = '投票驗證程序'
    msg['From'] = gmail_user
    msg['To'] = address

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

