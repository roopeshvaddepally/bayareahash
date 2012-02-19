import requests, json

def get_upcoming_events():
    resp = requests.get('https://api.meetup.com/2/open_events?key=512d2747301844127348784e541d78&sign=true&state=CA&status=upcoming&city=San Francisco&country=USA&topic=technology&zip=94110&radius=50&order=time&page=30&desc=true')
    parsed = json.loads(resp.content)
    return parsed

