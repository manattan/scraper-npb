import urllib.request
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import re
import socket
import config

def connection():
    return create_engine('postgresql://{}:@localhost/{}'.format(config.username, config.db))
engine = connection()

print(engine)

def insert(id, num, teamname, history):
    engine.execute("insert into allteam2020(id, num,teamname, history) values ('{}', '{}', '{}', '{}')".format(id, num, teamname, history))
    return

def getHistory(num):
    return engine.execute("select * from allteam2020 where num='{}'".format(num)).fetchone()

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# url = 'http://sebango.web.fc2.com/sebangou15/n-fighters-sebangou15.html'

def makeHistory(year, name):
    result = ''

    keyI = 0
    keyName = name[0] + '→'
    for i in range(1, len(year)):
        if not name[i] == keyName:
            if i - keyI == 1:
                result = result + '{}({})'.format(name[keyI], year[keyI]) + '→'
            else:
                result = result + '{}({}~{})'.format(name[keyI], year[keyI], year[i-1]) + '→'
            keyI = i
            keyName = name[i]
        if i == len(name)-1:
            result = result + '{}({}~)'.format(name[keyI], year[keyI])
        
    return result

def getInfomation(url):
    try:
        req = urllib.request.Request(url , headers=headers)
        soup = BeautifulSoup(urllib.request.urlopen(req).read())
        tr = soup.find('table').findAll('tr')

        year = []
        name = []

        for i in range(1,len(tr)):
            el = tr[i].findAll('td')
            yearEl = str(el[0])[4:len(str(el[0]))-5]
            nameEl = str(el[1])[4:len(str(el[1]))-5]

            if nameEl == "　":
                nameEl = "なし"
            if ' ' in nameEl:
                nameEl = re.split(' ', nameEl)
                res = nameEl[0]
                for i in range(1, len(nameEl)):
                    res = res + nameEl[i]
                nameEl = res
            if '　' in nameEl:
                nameEl = re.split('　', nameEl)
                res = nameEl[0]
                for i in range(1, len(nameEl)):
                    res = res + nameEl[i]
                nameEl = res
            if '<br/>' in nameEl:
                nameEl = re.split('<br/>', nameEl)[0] + ',' + re.split('<br/>', nameEl)[1]
            
            year.append(yearEl)
            name.append(nameEl)
        
        history = makeHistory(year, name)
        return history

    except urllib.error.HTTPError as err:
            print(err.code)
    except urllib.error.URLError as err:
            print(err.reason)
    except socket.error as err:
            print("timeout")

def main():
    urlList = ['http://sebango.web.fc2.com/sebangou{}/n-fighters-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/f-d-hawks-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/s-lions-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/c-l-marines-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/o-bluewave-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/t-r-goldeneagles-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/y-baystars-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/y-swallows-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/h-t-carp-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/c-dragons-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/h-tigers-sebangou{}.html', 'http://sebango.web.fc2.com/sebangou{}/y-giants-sebangou{}.html']
    teamList = ['F','H', 'L', 'M', 'Bs', 'E', 'De', 'S', 'C', 'D', 'T', 'G']
    idL = 1
    for i in range(12):
        team = teamList[i]
        for j in range(1, 101):
            url = urlList[i].format(j, j)
            history = getInfomation(url)
            print('背番号{}: {}'.format(j,history))
            insert(idL, j , team, history )
            idL += 1

if __name__=="__main__":
    main()
