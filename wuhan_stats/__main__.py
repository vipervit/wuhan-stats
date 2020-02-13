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
    cases = tmp[3]
    deaths = tmp[6]
    time = soup.text.split('Last updated: ')[1].split('GMT')[0]
    last_updated = soup.text.split('Last updated: ')[1].split('GMT')[0] + ' GMT'
    critical = soup.text.split('Serious or Critical')[0].split('Mild Condition')[1].replace(' ', '')
    return {'Cases': cases, 'Deaths': deaths, 'Critical': critical, 'As of': last_updated }

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
    txt = ''
    info.pop('As of')
    i_deaths = int(info['Deaths'].replace(',',''))
    i_cases = int(info['Cases'].replace(',',''))
    rate = round( 100 * i_deaths / i_cases, 2)
    info['Deaths'] += '(' + str(rate) + '%)'
    for i in info:
        txt += i + ': ' + info[i] + '\n'
    txt = list(txt)
    txt = ''.join(txt)
    return txt

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
    else:
        raise NotImplementedError('Not desigend for this platform: ' + platform)

def output(stats, timestamp):
    header = 'COVID-19 ' + timestamp + ' v' + __version__
    if not __debug__: # running only once, not in loop
        logger.debug(header + '\n' + stats)
    else: # looped execution
        platform = get_platform()
        if platform == 'Mac':
            os.system('osascript -e \'display notification \"' + stats + '\" with title \"' + header + '\"\'')
        elif platform == 'Win':
            plyer.notification.notify(header, stats, timeout=WIN_NOTIFICATION_TIMEOUT)

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
            break
        time.sleep(SLEEP)

if __name__ == '__main__':
    main()
