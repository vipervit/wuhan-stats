import sys
import os
import keyring

from bs4 import BeautifulSoup
import requests
import plyer
import smtplib

from wuhan_stats import __version__, SITES, WIN_NOTIFICATION_TIMEOUT, EMAIL_ATTRIBS
from wuhan_stats.src.utils import get_platform, str_today

class site:

    class _desktop_alert:

        def __init__(self, site):
            self._site = site
            self._soup = None
            self._text = None
            self._stats = None
            self._timestamp = None

        @property
        def text(self):
            return self._text

        @property
        def timestamp(self):
            return self._timestamp

        @timestamp.setter
        def timestamp(self, val):
            self._timestamp = val

        def __make__(self, soup):
            self._soup = soup
            if self._site == 'Worldometer':
                self.__worldometer_parse_stats__()
                self.__compose__()

        def __worldometer_parse_stats__(self):
                tmp = self._soup.title.string.split(' ')
                total = tmp[3]
                deaths = tmp[6]
                active = str(self._soup.find_all('div', class_='number-table-main')).split('>')[1].split('<')[0]
                critical = self._soup.text.split('Serious or Critical')[0].split('Mild Condition')[1].replace(' ', '')
                critical = ' ('.join(critical.split('('))
                new = str(self._soup.find('tr', class_='total_row')).split(';">')[1].split('<')[0]
                self._stats = {'Cases Total': total, 'Cases New': new, 'Cases Active': active, 'Deaths': deaths, 'Critical': critical }

        def __compose__(self):
            info = self._stats
            i_deaths = int(info['Deaths'].replace(',',''))
            i_cases_total = int(info['Cases Total'].replace(',',''))
            rate = round( 100 * i_deaths / i_cases_total, 2)
            ln1 = 'Cases: ' + info['Cases Active']  + ' (' + info['Cases Total'] + ')  +' + info['Cases New'] + '\n'
            ln2 = 'Deaths: ' + info['Deaths'] + ' (' + str(rate) + '%)' + '\n'
            ln3 = 'Critical: ' + info['Critical']
            self._text =  ln1 + ln2 + ln3

        def send(self):
            header = 'COVID-19 ' + self.timestamp
            platform = get_platform()
            if platform == 'Mac':
                os.system('osascript -e \'display notification \"' + self._text + '\" with title \"' + header + '\"\'')
            elif platform == 'Win':
                plyer.notification.notify(header, self._text, timeout=WIN_NOTIFICATION_TIMEOUT)
            elif platform == 'Linux':
                os.system('notify-send \"' + header + '\" \"' + self._text + '\"')

    class _email_alert:

        def __init__(self, site):
            self._site = site

        def __worldometer_get_latest__(self):
            alert_img = '/images/alert.png'
            self._latest_update_html = str(self._soup).split('<div id=\"newsdate' + str_today() + '\">')[1]
            self._latest_update_html = self._latest_update_html.split('button')[0]
            self._latest_update_html = self._latest_update_html.replace(alert_img, SITES[self._site]['home'] + alert_img)

        def __make__(self, soup, timestamp):
            self._timestamp = timestamp
            self._soup = soup
            if self._site == 'Worldometer':
                self.__worldometer_get_latest__()

        def send(self):
            import smtplib, ssl
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            sender_email = EMAIL_ATTRIBS.from_
            receiver_email = EMAIL_ATTRIBS.to
            password = keyring.get_password(EMAIL_ATTRIBS.keyring_service, EMAIL_ATTRIBS.keyring_uid)
            message = MIMEMultipart("alternative")
            message["Subject"] = "COVID-19 latest " + self._timestamp
            message["From"] = sender_email
            message["To"] = receiver_email
            text = self._latest_update_html
            html = self._latest_update_html
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )

    def __init__(self, sitename):
        self._site = sitename
        self._url_home = SITES[sitename]['home']
        self._url_updates = SITES[sitename]['home'] + SITES[sitename]['updates']
        self._desk = self._desktop_alert(self._site)
        self._emal = self._email_alert(self._site)
        self._soup = None
        self._last_updated = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self._desk
        del self._emal

    @property
    def site(self):
        return self._site

    @property
    def soup(self):
        return self._soup

    @property
    def last_updated(self):
        return self._last_updated

    @property
    def desktop(self):
        return self._desk

    @property
    def email(self):
        return self._emal

    def get(self):
        r = requests.get(self._url_updates)
        self._soup = BeautifulSoup(r.text, features="html.parser")
        if self._site == 'Worldometer':
            self._last_updated =  self.soup.text.split('Last updated: ')[1].split('GMT')[0] + ' GMT'
        self.desktop.timestamp = self.last_updated
        self.desktop.__make__(self._soup)
        self.email.__make__(self._soup, self.desktop.timestamp)
