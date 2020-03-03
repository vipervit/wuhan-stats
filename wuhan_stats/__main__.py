import os
import sys
import time
import logging

from bs4 import BeautifulSoup
import requests

import plyer

from . import __version__, logger

if not __debug__:
    logger.setLevel(logging.DEBUG)

SLEEP = 3600
SLEEP_MIN = 900
WIN_NOTIFICATION_TIMEOUT = 3600

SITES = { \
    # 'jh': 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6',\
    'wm': 'https://www.worldometers.info/coronavirus/' \
    }

# ------- Worldometer
def info_get_wm():
    r = requests.get(SITES['wm'])
    soup = BeautifulSoup(r.text, features="html.parser")
    tmp =soup.title.string.split(' ')
    total = tmp[3]
    deaths = tmp[6]
    last_updated = soup.text.split('Last updated: ')[1].split('GMT')[0] + ' GMT'
    active = str(soup.find_all('div', class_='number-table-main')).split('>')[1].split('<')[0]
    critical = soup.text.split('Serious or Critical')[0].split('Mild Condition')[1].replace(' ', '')
    critical = ' ('.join(critical.split('('))
    new = str(soup.find('tr', class_='total_row')).split(';">')[1].split('<')[0]
    return {'Cases Total': total, 'Cases New': new, 'Cases Active': active, 'Deaths': deaths, 'Critical': critical, 'As of': last_updated }

# ---------- Johns Hopkins CSSE
def info_get_jh():
    raise NotImplementedError

def info_get(site):
    if site == 'wm':
        return info_get_wm()
    if site == 'jh':
        return info_get_jh()

def info_collect(sites):
    complete_info = {}
    for site in SITES:
        complete_info.update({site: info_get(site)})
    return complete_info

def alert_wm(info):
    i_deaths = int(info['Deaths'].replace(',',''))
    i_cases_total = int(info['Cases Total'].replace(',',''))
    rate = round( 100 * i_deaths / i_cases_total, 2)
    ln1 = 'Cases: ' + info['Cases Active']  + ' (' + info['Cases Total'] + ')  +' + info['Cases New'] + '\n'
    ln2 = 'Deaths: ' + info['Deaths'] + ' (' + str(rate) + '%)' + '\n'
    ln3 = 'Critical: ' + info['Critical']
    return ln1 + ln2 + ln3

def alert_compose(info):
    for site in info:
        if site == 'wm':
            return alert_wm(info[site])

def get_platform():
    platform = sys.platform
    if platform == 'darwin':
        return 'Mac'
    elif platform == 'win32':
        return 'Win'
    elif platform == 'linux':
        return 'Linux'
    else:
        raise NotImplementedError('Not designed for this platform: ' + platform)

def output(stats, timestamp):
    header = 'COVID-19 ' + timestamp + ' v' + __version__
    platform = get_platform()
    if platform == 'Mac':
        os.system('osascript -e \'display notification \"' + stats + '\" with title \"' + header + '\"\'')
    elif platform == 'Win':
        plyer.notification.notify(header, stats, timeout=WIN_NOTIFICATION_TIMEOUT)
    elif platform == 'Linux':
        os.system('notify-send \"' + header + '\" \"' + stats + '\"')


def main():

    if SLEEP < SLEEP_MIN: # to restrict polling period in order not to abuse the sources
        logger.info('Polling period may not be less than ' + SLEEP_MIN + ' min.')
        raise SystemExit

    prev = ''


    while True:
        info = info_collect(SITES)
        last = info['wm']['As of']
        if  prev < last:
            output(alert_compose(info), last)
        prev = last
        if not __debug__:
            logger.debug('Exiting due to debug mode.')
            sys.exit()
        time.sleep(SLEEP)

if __name__ == '__main__':
    main()
