import os
import time
import logging

import viperdriver
viperdriver.loggers_set(logging.DEBUG)

from viperdriver import SessionDriver

sleep = 3600
cases = 0
deaths = 0
prev = 0
diff = 0

sites = { \
    'jh': 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6',\
    'wm': 'https://www.worldometers.info/coronavirus/' \
    }

def info_collect(sites):
    complete_info = {}
    drv = pom()
    for site in sites:
        complete_info.update({site: drv.info_get(sites[site])})
    return complete_info

def alert_compose(info):
    txt = ''
    print(info)
    for site in info:
        for each in info[site]:
            txt += each + ' | '
    return txt

def output(str):
    print('Alert: ' + str)
    # os.system('osascript -e \'display notification \"' + str + '\" with title \"Coronavirus Update\"\'')

class pom:

    def __init__(self):
        self._drv = SessionDriver()
        self._url_jh = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6'
        self._url_wm = 'https://www.worldometers.info/coronavirus/'
        self._drv.launch()

    def info_get(self, site):
        info = []
        self._drv.get(self.__site__(site))
        info.append(self._drv.title)
        return info

    def info_final(self):
        return 'works'

    def __site__(self, site):
        assert site is not None, 'Site is not specified'
        if site == self._url_jh: return self._url_jh
        if site == self._url_wm: return self._url_wm
        return None

def main():

    while True:
        output(alert_compose(info_collect(sites)))
        break
        # output(info_final(info_jh, info_wm))
        # time.sleep(sleep)


def main_old():
    with SessionDriver() as x:

        while True:

            x.launch()
            x.get('https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6')
            x.wait_until(10, "title_is('Coronavirus 2019-nCoV')")

            time.sleep(3)

            txt_cases = x.find_elements_by_class_name("responsive-text-label")[1].text
            cases = int(txt_cases.replace(',',''))
            txt_deaths = x.find_elements_by_class_name("responsive-text-label")[3].text
            deaths = int(txt_deaths.replace(',',''))

            rate = round(deaths/cases,2) * 100

            if cases > prev:
                if prev != 0:
                    diff = 100 * round((cases - prev)/cases,2)
                msg = 'Total: ' + str(cases) + '(+' + str(diff) + '%) \nDeaths: ' + str(deaths) + '\nRate: ' + str(rate) + '%'
                output(msg)

            prev = cases

            x.quit()

            time.sleep(sleep)


if __name__ == '__main__':
    main()
