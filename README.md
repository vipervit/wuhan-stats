# wuhan_stats
Email and desktop alert on updates of COVID-19 pandemic statistics.

Generates alert using the Notifications feature on Mac, Linux or Windows as well as via email for COVID-19 latest statistics as they become available at https://www.worldometers.info/coronavirus/

Email alert can be swtiched off or on and provides deeper coverage. 

The app has a simple interface allowing to set frequency of the alerts and pause them. It also diplays a countdown timer. 

## Snapshots
![Control](https://github.com/vipervit/wuhan_stats/blob/master/img/control.jpeg)


![Alert](https://github.com/vipervit/wuhan_stats/blob/master/img/alert.jpg)


![Email](https://github.com/vipervit/wuhan_stats/blob/master/img/email.jpeg)

## Dependencies:
- requests
- BeautifulSoup
- plyer

## To install:
*'pip install wuhan_stats'*

## Email
The app uses smptlib and needs to have access to an email account.
The password for the account is retrieved from the keychain on the local machine using popular Python 'keyring' package.
All email attributes are provided as CLI keys.
For example, let's say 'gmail' account in the computer's keychain references to Gmail user account called 'foo'. The app will retrieve the password for the account based on command line parameters '-s gmail' and '-u foo'.


## To run:
*'python -m wuhan-stats -t (insert receiver email) -f (insert sender email) -s (insert keyring service name) -u (insert keyring uid)'*

## Notes
For Mac, make sure desired notification style is choosen for Script Editor in System Preferences->Notifications.  
