import json
import requests

headers = {'Accept': 'application/json'}


url = "https://007investment.table.core.windows.net:443/Transaction?sv=2016-05-31&si=Transaction-15EEC51E092&tn=transaction&sig=G%2BAfHj8oMMxKdTwj93q4KiR7tmnIPJdKkjwyHYdggpM%3D"
response = requests.get(url, headers=headers)
j = response.json()
for value in j['value']:
    print(value['Timestamp'])
    print(value['StockId'])
    print(value['Price'])
    print(value['Amount'])
