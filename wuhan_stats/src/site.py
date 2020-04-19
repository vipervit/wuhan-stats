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
            # We can total cases and total deaths directly from the title
            cases_total = str(self._soup.title).split()[3]
            deaths_total = str(self._soup.title).split()[6]
            # For some reason using find("tr", class_"total_row_world odd") doesn't work, therefore more trickery is required
            for tag in self._soup.find("table", id="main_table_countries_today").find("thead").next_sibling.next_sibling:
                if "World" in str(tag):
                    data = tag.find_all("td")
            cases_new = data[2].text
            deaths_new = data[4].text
            cases_active = data[6].text
            cases_critical = data[7].text
            self._stats = {'Cases Total': cases_total, 'Deaths': deaths_total, 'Cases New': cases_new, 'Cases Active': cases_active,  'Deaths New': deaths_new, 'Critical': cases_critical }

        def __compose__(self):
            info = self._stats
            i_deaths = int(info['Deaths'].replace(',',''))
            i_cases_total = int(info['Cases Total'].replace(',',''))
            rate_deaths = round( 100 * i_deaths / i_cases_total, 2)
            i_critical = int(info['Critical'].replace(',',''))
            rate_critical = round( 100 * i_critical / i_cases_total, 2)
            ln1 = 'Cases: ' + info['Cases Active']  + ' (' + info['Cases Total'] + ') ' + info['Cases New'] + '\n'
            ln2 = 'Deaths: ' + info['Deaths'] + ' (' + str(rate_deaths) + '%) ' + info['Deaths New'] + '\n'
            ln3 = 'Critical: ' + info['Critical'] + ' (' + str(rate_critical) + '%) '
            self._text =  ln1 + ln2 + ln3

        def contents(self):
            return self._text

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

        def __make__(self, soup, timestamp, brief_stats):
            self._timestamp = timestamp
            self._soup = soup
            def make_header(text):
                spacing = ' .... '
                words = text.split()
                words.insert(4, spacing)
                words.insert(9, spacing)
                return ' '.join(words).upper()
            if self._site == 'Worldometer':
                self.__worldometer_get_latest__()
                self._latest_update_html = make_header(brief_stats) + self._latest_update_html

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
        self.email.__make__(self._soup, self.desktop.timestamp, self.desktop.contents())
