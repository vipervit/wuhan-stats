# wuhan_stats
Simple alert on updates of Wuhan virus statistics.

Generates alert using the Notifications feature on Mac or Windows as soon as new statistics are available at https://www.worldometers.info/coronavirus/  

![Alert sample](https://github.com/vipervit/wuhan_stats/raw/master/snapshot.jpeg)

## Dependencies:
- requests
- BeautifulSoup
- plyer

## To install:
*'pip install wuhan_stats'*

## To run:

*'nohup python -m wuhan-stats &'* (Mac)

*'pythonw -m wuhan_stats'*        (Windows)

## Notes
Polling period is 1 hour (hardcoded).

Alert is generated only when the script is launched and then only if it finds (while checking hourly) the 'Last updated' field on the source site updated.

For Windows, the notification's timeout is 1 hour.

For Mac, make sure desired notification style is choosen for Script Editor in System Preferences->Notifications.  
