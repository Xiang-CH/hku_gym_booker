from bs4 import BeautifulSoup
import requests, time, datetime, os

def extract(page, links):
    gymplace = []
    session = 'test'
    day_from_today = -1
    for i in page:
        if ' (' in i and len(i)<40:
            day_from_today += 1
            gymplace.append({})
            gymplace[day_from_today]['date'] = i
            gymplace[day_from_today]['id'] = day_from_today
        if '-' in i:
            session = i.strip()
            if len(session) < 10:
                try:
                    gymplace[day_from_today]['sessions'].append({'time': session})
                except:
                    gymplace[day_from_today]['sessions'] = [{'time': session}]
        if '/' in i and ' (' not in i:
            available = i.split('/')[0]
            gymplace[day_from_today]['sessions'][-1]['available'] = int(available)
            gymplace[day_from_today]['sessions'][-1]['link'] = links.pop(0).get('href')
        if 'FULL' in i:
            gymplace[day_from_today]['sessions'][-1]['available'] = 0
        
    return gymplace

def removePassedSession(todayTable):
    currentDatetime = datetime.datetime.now()
    for session in todayTable[1:]:
        if session[:2] <= currentDatetime.strftime('%H'):
            todayTable.remove(session)

def notifyAvailableSessionsToday(table):
    title = "Gym available today!"
    text = "https://fcbooking.cse.hku.hk/Form/SignUp"
    available = False
    for line in table:
        # if "2030-2200" in line:
        if "1845-2015" in line:
        # if "1700-1830" in line:
            available = True

    if available:
        os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

        
        

def printTable(table, Gymplace):
    removePassedSession(table[0])
    print(Gymplace)
    notifyAvailableSessionsToday(table[0])
    for oneday in table:
        if len(oneday) == 1:
            print(f'{oneday[0]}:\n    No available session')
        elif oneday != []:
            print(oneday[0]+':')
            for field in oneday[1:]:
                print(f'    {field}')
    print('\n')


def start(interval = 30):
    while True:
        Gym = requests.get('https://fcbooking.cse.hku.hk/')
        soup = BeautifulSoup(Gym.content, "html.parser")
        #CseActive = soup.find(id="c10001Content").text.split("\n")
        B_Active = soup.find(id="c10002Content").text.split("\n")
        B_Active_links = soup.find(id="c10002Content").find_all('a')
        #Stanley_Ho = soup.find(id="c10003Content").text.split("\n")

        # activeMeta = extract(CseActive)
        # printTable(activeMeta, 'CSE Active')
        bactiveMeta = extract(B_Active, B_Active_links)
        print(bactiveMeta)
        # printTable(bactiveMeta, 'B-Active')
        # stanleyMeta = extract(Stanley_Ho)
        # printTable(stanleyMeta, 'Stanley Ho')

        print('https://fcbooking.cse.hku.hk/Form/SignUp')
        print('--------------------------------------')
        time.sleep(interval)
        #https://fcbooking.cse.hku.hk/Form/SignUp

def getMetaData():
    Gym = requests.get('https://fcbooking.cse.hku.hk/')
    soup = BeautifulSoup(Gym.content, "html.parser")
    CseActive = soup.find(id="c10001Content").text.split("\n")
    CseActive_links = soup.find(id="c10001Content").find_all('a')
    B_Active = soup.find(id="c10002Content").text.split("\n")
    B_Active_links = soup.find(id="c10002Content").find_all('a')
    #Stanley_Ho = soup.find(id="c10003Content").text.split("\n")

    activeMeta = extract(CseActive,CseActive_links)
    bactiveMeta = extract(B_Active,B_Active_links)
    # stanleyMeta = extract(Stanley_Ho)
    return {'B-Active':bactiveMeta, 'CSE-Active':activeMeta}

# start(30)