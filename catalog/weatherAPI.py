#!/bin/python
# weatheroffice interface

## REWRITE THIS WITH OOP SO YOU CAN USE IT WITH DJANGO VIEWS ##


import requests
import bs4
import sys
import time
import random


def toF(c):
    F = (c * (9 / 5)) + 32
    return int(F)


def fortune():
    ''' Fortunes '''
    fortunes = ['Godly luck.',
                'Your wisdom makes you superior to others.',
                'Error: Fortune not found.',
                'An interesting medical opportunity is in your near future.',
                'Today will be yesterday tomorrow.']

    n = random.randint(0, len(fortunes) - 1)
    print('Your fortune:', fortunes[n] + '\n')


# download the web page
res = requests.get('https://weather.gc.ca/forecast/hourly/ns-21_metric_e.html')
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
    sys.exit()

# create beautiful soup
soup = bs4.BeautifulSoup(res.text, features='lxml')


temperatures = soup.select('td[headers="header2"]')
summaries = soup.select('td div p')
currentTemp = int(temperatures[0].getText())
currentTempF = toF(currentTemp)
laterTemp = int(temperatures[4].getText())
laterTempF = toF(laterTemp)
summ1 = summaries[0].getText()
summ2 = summaries[4].getText().lower()

timeObject = time.localtime()

if timeObject.tm_hour > 12:
    hours = str(timeObject.tm_hour - 12)
    suffix = ' PM'
elif timeObject.tm_hour == 0:
    hours = '12'
    suffix = ' AM'
else:
    hours = str(timeObject.tm_hour)
    suffix = ' AM'


if timeObject.tm_min < 10:
    minutes = '0' + str(timeObject.tm_min)
else:
    minutes = str(timeObject.tm_min)

time = hours + ':' + minutes + suffix

months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
month = months[timeObject.tm_mon]
day = str(timeObject.tm_mday)
date = month + ' ' + day

# display the values in a meaningful way

if __name__ == '__main__':
    print('''
It is {} and the time is {}.

{}, the current temperature is {}ºC / {}ºF.
In a few hours it will have changed to {}ºC / {}ºF and {}.
'''.format(date, time, summ1, currentTemp, currentTempF, laterTemp,
           laterTempF, summ2))
    fortune()