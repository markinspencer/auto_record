import re
import time
import requests
from fake_useragent import UserAgent
from datetime import datetime

OCEANIA = "oce"
KOREA = "kr"
EUROPE_WEST=  "euw"

class account:
    def __init__(self, region, name, summoner):
        self.region = region
        self.name = name
        self.summoner = summoner

def request_recording(region, summoner): 
    ua = UserAgent()
    headers = {'User-Agent': ua.random }
    request_url = 'https://porofessor.gg/partial/live-partial/%s/%s' % (region, summoner)
    response = requests.get(request_url, headers=headers).text
    pattern = r"(?P<url>https?://[^\s]+)"
    arr = re.findall(pattern, response)
    
    if response.find("An Error has occurred, please try again later") != -1:
        print("Can't determine if player is in game.")
        return

    is_recording_url = None
    record_replay_url = None

    for url in arr:
        if is_recording_url != None and record_replay_url != None:
            break
        if url.find("api/is-recording") != -1:
            is_recording_url = url
        if url.find("api/record-replay") != -1:
            record_replay_url = url
    
    if is_recording_url == None and record_replay_url == None:
        print("No game found.")
        return
    
    print("Game found.")
    response = requests.get(is_recording_url, headers=headers)
    
    if response.status_code != 200:
        print("Error: " + str(response.status_code))
        return
    
    data = response.json()
    is_recording = data["isRecording"]

    if(is_recording):
        print("Replay already requested.")
        return
    
    requests.get(record_replay_url, headers=headers)
    print("Replay requested.")


accounts = []
accounts.append(account(KOREA, "Irelking", "이렐아칼리"))
accounts.append(account(KOREA, "Irelking", "aileri"))
accounts.append(account(KOREA, "Irelking", "erilia"))
accounts.append(account(KOREA, "Irelking", "IRELKlNG"))
accounts.append(account(OCEANIA, "Void Daughter", "Void Daughter"))
accounts.append(account(EUROPE_WEST, "Zhong", "zhongoida"))
accounts.append(account(EUROPE_WEST, "Zhong", "zhong"))
accounts.append(account(EUROPE_WEST, "Six10", "Six10 z"))
accounts.append(account(EUROPE_WEST, "Neckless", "Neckiess"))
accounts.append(account(EUROPE_WEST, "Saiel", "Saiel"))

while(True):
    for acc in accounts:
        print("[%s] Requesting replay for %s: account %s, region %s" % (datetime.now(), acc.name, acc.summoner, acc.region))
        request_recording(acc.region, acc.summoner) 
        print("")
        time.sleep(5)

    time.sleep(180)


                                                            