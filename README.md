# wuhan_stats
Simple alert for updates of Wuhan virus statistics.

Currently for Mac only. Generates alert using Mac Notifications as soon as new statistics are available on https://www.worldometers.info/coronavirus/  

![Alert sample](snapshot.jpeg)

To install: 'pip install wuhan_stats'

To run: 'python -m wuhan-stats &'

Polling period is 1 hour. Alert is generated only if there is a new timestamp on the source site in 'Last updated' field.

Dependencies:

requests
BeautifulSoup

More functionality including a Windows version is planned to be added in later versions.
