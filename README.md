# wuhan-stats
Selenium-based alert for updates of Wuhan virus statistics.

Currently for Mac only. Generates alert using Mac Notifications as soon as new statistics are available on https://www.worldometers.info/coronavirus/  

![Alert sample](snapshot.jpeg)

The very first version.
To install: 'pip install wuhan-stats'
To run: 'python -O -m wuhan-stats &'
Do not omit '-O', without it the script runs in debug mode.
Polling period is currently hardcoded to be 1 hour.
Requires viperdriver package.
More functionality including a Windows version may be added in later versions.
