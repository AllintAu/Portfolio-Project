import requests
from crypto_api_key import API_KEY1

API_KEY = API_KEY1
BASE_URL = "http://api.coinlayer.com/"
BASE_URL_LIVE = "http://api.coinlayer.com/live"

def get_crypto_price():

    date_param = input("Enter the date you wanna query (format: YYYY-MM-DD): ")
    symbols= input("Enter the crypto symbol use comma as separator if you wanted more than 1 symbol: ").upper()
    target = input("Enter the base currency (fiat only): ").upper()

    url = f"{BASE_URL}/{date_param}"

    params = {
        "access_key": API_KEY,
        "target": target,
        "symbols": symbols
    } 
            
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        # checking if the rate key is present in the data 
        if 'rates' in data:
            print("Crypto Price Data:")
            for symbol in symbols.split(','):
                # Check if the symbol key is present in the 'rates' dictionary
                if symbol in data['rates']:
                    print(f"{symbol}: {data['rates'][symbol]} {target}")
                else:
                    print(f"No data available for {symbol}")
        else:
            print("No data available in the response.")
    else:
        print(f"Error : {response.status_code}")

def calculate_growth():
    start_date = input("Enter the start date (format: YYYY-MM-DD): ")
    end_date = input("Enter the end date (format: YYYY-MM-DD): ")
    symbols_input = input("Enter the crypto symbols(s) using a comma as separator: ").upper()
    target = input("Enter the base currency (fiat only): ").upper()

    # strip and strip symbols input
    symbols = [symbol.strip("'") for symbol in symbols_input.split(',')]

    # Query data from start date
    start_url = f"{BASE_URL}/{start_date}"
    start_params = {
        "access_key": API_KEY,
        "target": target,
        "symbol": ",".join(symbols)
    }
    start_response = requests.get(start_url, params=start_params)

    # Query data from end date 
    end_url = f"{BASE_URL}/{end_date}"
    end_params = {
        "access_key": API_KEY,
        "target": target,
        "symbol": ",".join(symbols)
    }
    end_response = requests.get(end_url, params=end_params)

    if start_response.status_code == 200 and end_response.status_code == 200:
        start_data = start_response.json()
        end_data = end_response.json()

        print("Crypto Price Data:")
        for symbol in symbols:
            if symbol in start_data['rates'] and symbol and end_data['rates']:
                start_price = start_data['rates'][symbol]
                end_price = end_data['rates'][symbol]
                changes_percent = ((end_price - start_price) / start_price * 100)
                changes_pip = (end_price - start_price)
                print(f"{symbol}: Start Price: {start_price} {target}, End Price: {end_price} {target}, Changes: {changes_pip} {target} or {changes_percent:.2f}%")

            else:
                print(f"Symbol '{symbol}' not found in the response.")
            
        else:
            print(f"Error: {start_response.status_code} (Start Date), {end_response.status_code} (End Date)")

def current_price():
    base_cur = input("Enter base currency: ").upper()
    crypto = input("Enter crypto currency: ").upper()

    params = {
        "access_key": API_KEY,
        "target": base_cur,
        "symbols": crypto

    }
    response = requests.get(BASE_URL_LIVE, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'rates' in data:
            print("Crypto Price Data:")
            for symbol in crypto.split(','):
                    # Check if the symbol key is present in the 'rates' dictionary
                if symbol in data['rates']:
                        print(f"{symbol}: {data['rates'][symbol]} {base_cur}")
                else:
                        print(f"No data available for {symbol}")
        else:
                print("No data available in the response.")
    else:
            print(f"Error : {response.status_code}")

def calculate_ex_rate():
    cal_base_cur = input("Enter based currency you wanna calculate: ").upper()
    cal_symbol = input("Enter crypto symbol you wanna calculate: ").upper()
    cal_amount = float(input("Enter amount of crypto currencies: "))

    params = {
            "access_key": API_KEY,
            "target": cal_base_cur,
            "symbols": cal_symbol 
    }

    response = requests.get(BASE_URL_LIVE, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'rates' in data:
          cal_rate = data['rates'][cal_symbol] # Access the rates of specific symbol
          calculation = cal_rate * cal_amount
          print(f"{cal_amount} {cal_symbol} Is Equal to {calculation} {cal_base_cur}")
        else:
            print("No data for the specified symbol")
    else:
         print(f"Error {response.status_code}")



while True:
    print("Choose a feature: ")
    print("1. Query Crypto Live Rate")
    print("2. Query Crypto Price")
    print("3. Calculate Crypto Growth")
    print("4. Calculate Conversion (Crypto to Fiat)")
    print("5. Exit")

    option = input("Enter your choice (1, 2, 3, 4, 5): ")

    if option == '1':
        print("Let's see today price!")
        current_price()

    elif option == '2':
        print("Let's query crypto price!!")
        get_crypto_price()

    elif option == '3':
        print("Let's see how its changes!!")
        calculate_growth()

    elif option == '4':
        print("Let's convert!")
        calculate_ex_rate()

    elif option == '5':
        print("Bye!")
        break
