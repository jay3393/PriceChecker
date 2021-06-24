import smtplib
import os

class Email:

    password = os.environ.get('SHEESHBOTPASS')

    to_users = [
        'ipermagt@gmail.com',
        'sheeshbotagent@gmail.com'
    ]

    def __init__(self, data):
        '''
        :return
        '''
        self.data = data

    def send_mail(self):
        '''
        Checks the products that fell and sends the data to users
        '''
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(user='sheeshbotagent@gmail.com', password=self.password)

        subject = 'Prices fell down!'
        body = ''

        for data in self.data:
            name = data['name']
            url = data['url']
            current = data['currentPrice']
            previous = data['previousPrice']
            change = float(current.strip('$')) - float(previous.strip('$'))
            body += name + ' dropped $' + str(round(change,2)) + ' from ' + previous + ' -> ' + current + '\n' + url + '\n'

        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail(
            'sheeshbotagent@gmail.com',
            self.to_users,
            msg
        )

        server.quit()