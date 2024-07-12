import json

import requests
from selenium import webdriver


response = requests.get('https://booking.ctm.ma/api/fr-fr/journeys/search?departureDate=2024-07-10&isPartOfRoundtrip'
                        '=false&currency=CURRENCY.MAD&fareClasses=BONUS_SCHEME_GROUP.ADULT%2C1&originCityId=5618'
                        '&destinationCityId=5589&IsOutbound=true&CheckPaxSoldTogetherRules=true')
with open('result.json', 'w') as outfile:
    json.dump(response.json(), outfile, indent=4)


s = 'https://booking.ctm.ma/journeys?oCity=5618&dCity=5589&oDate=2024-07-10&fareClasses=BONUS_SCHEME_GROUP.ADULT,1'