import ducoapi

api_connection = ducoapi.api_actions()

api_connection.login(username='YourUsername', password='YourPassword')

current_balance = api_connection.balance()
print(current_balance)

api_connection.close()