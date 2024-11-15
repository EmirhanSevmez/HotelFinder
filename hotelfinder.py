import requests
import json


def web_crawler(city):      
    base_url = f"https://www.otelpuan.com/hotel-search/json/{city}-Otelleri?&sort=OTELPUAN&adult=2&check_in=15.11.2024&check_out=16.11.2024&limit=20&offset=20" # You can change the date and city here
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" # You can change the user agent here
    }
    response = requests.get(base_url, headers=headers) # Get response

    if response.status_code == 200: # if correct                     
        data = json.loads(response.text) 
        return data 
    else:
        print("Please enter real city name") 

def find_max_total_price_with_name(data): # find the hotel with the highest price and its name
    max_price = None  
    max_hotel_name = None  
    if isinstance(data, dict): # if data is a dictionary
        for key, value in data.items(): 
            if key == "hotelPrice" and isinstance(value, dict): 
                total_price = value.get("totalPrice") # get total price
                if total_price is not None:  # if not empty
                    if max_price is None or total_price > max_price: # if max_price is None or total_price is greater than max_price
                        max_price = total_price # new max price
                        max_hotel_name = data.get("name") # get hotel name
            else:
                result_price, result_name = find_max_total_price_with_name(value) # recursive call
                if result_price is not None: # if not empty
                    if max_price is None or result_price > max_price: # if max_price is None or result_price is greater than max_price
                        max_price = result_price # new max price
                        max_hotel_name = result_name # get hotel name
    elif isinstance(data, list): # if data is a list
        for item in data: 
            result_price, result_name = find_max_total_price_with_name(item) # recursive call
            if result_price is not None: # if not empty
                if max_price is None or result_price > max_price: # if max_price is None or result_price is greater than max_price
                    max_price = result_price # new max price
                    max_hotel_name = result_name # get hotel name
    return max_price, max_hotel_name 
        

        

print("Welcome to hotel finder!")
city = input("Enter the city you want to find most expensive hotel in(First letter uppercase, only English words. Example: Istanbul): ")
data = web_crawler(city)
maxPrice = find_max_total_price_with_name(data)
if maxPrice[0] or maxPrice[1] is not None:
    print(f"The most expensive hotel in {city} is {maxPrice[0]} TL and its name is {maxPrice[1]}")
else:
    print(f"No hotel found in {city}")
