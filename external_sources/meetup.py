import requests, json
from common.db import add_data
from datetime import datetime

def get_upcoming_events():
    resp = requests.get('https://api.meetup.com/2/open_events?key=512d2747301844127348784e541d78&sign=true&state=CA&status=upcoming&city=San Francisco&country=USA&time=,1w&topic=technology&zip=94110&radius=50&order=time&page=30&desc=true')
    parsed = json.loads(resp.content)
    return parsed


def populate_meetup_data():
    meetup_data_list = get_upcoming_events()["results"]
    formatted_meetup_list = []
    for meetup in meetup_data_list:
        formatted_meetup_list.append(dict(category="meetup",
                                          url=meetup["event_url"],
                                          title=meetup["name"],
                                          description=meetup["description"],
                                          thumbnail="http://i.imgur.com/PYfMX.png",
                                          meetup_date=meetup["time"]))
    add_data(datetime.now(), formatted_meetup_list)
