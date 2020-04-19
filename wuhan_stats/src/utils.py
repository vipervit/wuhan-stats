import datetime
import sys

def secs2time(secs):
    """Converts integer number of seconds to a time string of format hh:mm:ss."""
    h = secs//(60*60)
    m = (secs-h*60*60)//60
    s = secs-(h*60*60)-(m*60)
    x = [ h, m, s ]
    for i in range(len(x)):
        if x[i] < 10:
            x[i] = '0' + str(x[i])
        x[i] = str(x[i])
    return ':'.join(x)

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

def str_today():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
