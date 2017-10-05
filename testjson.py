import json
import requests

headers = {'Accept': 'application/json'}
url = "https://007investment.table.core.windows.net/User?sv=2016-05-31&si=007InvestmentAdmin&tn=user&sig=U3AKSUEypo1PPt%2B3Wly86DlKkNgnxylwP5hyHrICYiU%3D"
response = requests.get(url, headers=headers)
print(response.text)