import json
import requests
import datetime
#
import cherrypy

#html request
import requests
from cherrypy.lib import static
import os
from jinja2 import Environment, FileSystemLoader
from figo import FigoSession
import json

session = FigoSession("ASHWLIkouP2O6_bgA2wWReRhletgWKHYjLqDaqb0LFfamim9RjexTo22ujRIP_cjLiRiSyQXyt2kM1eXU2XLFZQ0Hro15HikJQT_eNeT_9XQ")

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

env = Environment(loader=FileSystemLoader('html'))

percentage=-0.01

class Landing_Page(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(name="Apple")

    @cherrypy.expose
    def transactionHistory(self):
        headers = {'Accept': 'application/json'}
        # Rest call towards the "John Snow" mock account on DB
        url = "https://007investment.table.core.windows.net:443/Transaction?sv=2016-05-31&si=Transaction-15EEC51E092&tn=transaction&sig=G%2BAfHj8oMMxKdTwj93q4KiR7tmnIPJdKkjwyHYdggpM%3D"
        response = requests.get(url, headers=headers)
        j = response.json()
        all_transactions= []
        #Make a list of all transactions with the fields below ('Timestamp' etc.)
        for value in j['value']:
                price_paid_long =(float(value['Price'])*float(value['Amount']))
                price_paid ="{0:.2f}".format(price_paid_long)
                time_stamp=datetime.datetime.strptime(value['Timestamp'][0:10], "%Y-%m-%d").strftime("%d.%m.%Y")
                
                single_transaction = {'Timestamp': time_stamp , 'StockId': value['StockId'], 'StockPrice': value['Price'], 'Amount': value['Amount'], 'MoneySpent': price_paid}
                all_transactions.append(single_transaction)

        #Post Request
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        payload = {
            "PartitionKey": "10-2017",
            "RowKey": "55",
            "UserId": "1",
            "StockId": "1",
            "Price": 10.6,
            "Status": "pending",
            "Amount": 100
                }

        r = requests.post("https://007investment.table.core.windows.net:443/Transaction?sv=2016-05-31&si=Transaction-15EEC51E092&tn=transaction&sig=G%2BAfHj8oMMxKdTwj93q4KiR7tmnIPJdKkjwyHYdggpM%3D", data=json.dumps(payload), headers=headers)
        #End Post Request

        tmpl = env.get_template('transactionHistory.html')
        return tmpl.render(seq=all_transactions)

    @cherrypy.expose
    def newTransaction(self):

        companyName=''
        stockName=''
        stockPrice=0
        stockAmount=0
        stockPercentage=0
        transAmount=0
        booking_date=''

        # Print out a list of accounts including its balance
        #for account in session.accounts:
        #    print(account.name)
        #    print(account.balance)

        headers = {'Accept': 'application/json'}
        url = "https://007investment.table.core.windows.net:443/Stock?sv=2016-05-31&si=Stock-15EEC52A495&tn=stock&sig=PbqLEW4Mi0hoNBw5nflEDszu36wzJ%2Bw592%2Bih%2BIfMI0%3D"
        response = requests.get(url, headers=headers)
        print(response.text)
        stocks = response.json()

        # Print out the list of all transactions on a specific account
        for transaction in session.get_account("A1.1").transactions:

            i = -1
            for stock in stocks['value']:
                for name in stock['CompanyName'].split('\n'):
                    i = i+1
                    #print(name.split(' ')[0] + "   "+transaction.name.split(' ')[0])
                    if name.split(' ')[0] == transaction.name.split(' ')[0]:
                        companyName = name.split(' ')[0]
                        stockName = name
                        stockPrice=stocks['value'][i]['Price']
                        stockAmount=(transaction.amount*percentage)
                        stockPercentage=((transaction.amount*percentage)/stocks['value'][i]['Price'])
                        transAmount=transaction.amount
                        booking_date=transaction.booking_date
                        print(str(transaction.amount)+" "+str(i))

        print(companyName+" / "+stockName+" / "+str(stockPrice)+" / "+str(stockPercentage))

        tmpl = env.get_template('newTransaction.html')
        return tmpl.render(companyName=companyName,stockName=stockName,stockPrice=stockPrice,stockPercentage=round(stockPercentage,2),transAmount=transAmount,stockAmount=stockAmount,booking_date=str(booking_date).split(' ')[0])


    @cherrypy.expose
    def myLink(self):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        payload = {
            "PartitionKey": "10-2017",
            "RowKey": "48",
            "UserId": "1",
            "StockId": "1",
            "Price": 10.6,
            "Status": "pending",
            "Amount": 100
                }

        r = requests.post("https://007investment.table.core.windows.net:443/Transaction?sv=2016-05-31&si=Transaction-15EEC51E092&tn=transaction&sig=G%2BAfHj8oMMxKdTwj93q4KiR7tmnIPJdKkjwyHYdggpM%3D", data=json.dumps(payload), headers=headers)
        #print(r.url)
        #print(r.text)
        #print(r.status_code)
        status = r.status_code
        #print(r.headers)
        header = r.headers
        text = r.text
        tmpl = env.get_template('post_success.html')
        return tmpl.render(status=status, header=header, text=text)

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
         'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
         'tools.staticdir.on': True,
         'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(Landing_Page(), '/', config=config)

##json read
