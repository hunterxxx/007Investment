from figo import FigoSession

session = FigoSession("ASHWLIkouP2O6_bgA2wWReRhletgWKHYjLqDaqb0LFfamim9RjexTo22ujRIP_cjLiRiSyQXyt2kM1eXU2XLFZQ0Hro15HikJQT_eNeT_9XQ")

# Print out a list of accounts including its balance
for account in session.accounts:
    print(account.name)
    print(account.balance)

# Print out the list of all transactions on a specific account
for transaction in session.get_account("A1.2").transactions:
    print(transaction)