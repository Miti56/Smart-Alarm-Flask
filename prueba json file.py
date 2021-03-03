import json

data = {}
data['Alarms'] = [alarm_time]


with open('data.json', 'w') as outfile:
    json.dump(data, outfile)