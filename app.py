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
        return tmpl.render()
    
    @cherrypy.expose
    def newTransaction(self):
        
        companyName=''
        stockName=''
        stockPrice=0
        stockAmount=0
        stockPercentage=0
        
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
                        print(str(transaction.amount)+" "+str(i))
                        
        print(companyName+" / "+stockName+" / "+str(stockPrice)+" / "+str(stockPercentage))
            
        tmpl = env.get_template('newTransaction.html')
        return tmpl.render()


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