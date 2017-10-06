import json
import requests

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

payload = {  
			"PartitionKey": "10-2017",
            "RowKey": "35",
            "UserId": "1",
            "StockId": "1",
            "Price": 10.6,
            "Status": "pending"
           }

r = requests.post("https://007investment.table.core.windows.net:443/Transaction?sv=2016-05-31&si=Transaction-15EEC51E092&tn=transaction&sig=G%2BAfHj8oMMxKdTwj93q4KiR7tmnIPJdKkjwyHYdggpM%3D", data=json.dumps(payload), headers=headers)
#print(r.url)
print(r.text)
print(r.status_code)
print(r.headers)
