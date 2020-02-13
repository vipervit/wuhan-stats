# wuhan_stats
Simple alert for updates of Wuhan virus statistics.

Generates alert using the Notifications feature on Mac or Windows as soon as new statistics are available on https://www.worldometers.info/coronavirus/  

![Alert sample](snapshot.jpeg)

Dependencies:
requests
BeautifulSoup
plyer

To install:
'pip install wuhan_stats' (see dependencies above)
or
'pip install wuhan_stats -r requirements.txt'

To run:
'nohup python -m wuhan-stats &' (Mac)
'pythonw -m wuhan_stats'  (Windows)

Polling period is 1 hour (hardcoded).
Alert is generated only if there is a new timestamp on the source site in 'Last updated' field.
For Mac, the alert stays in Notifications until deleted manually.
For Windows, the message disappears after 1 hour (as currently hardcoded).  
