import requests

url = "http://127.0.0.1:5010/weather"  # Add the last two digits with Stephen Alonso's student ID

response = requests.get(url) 

if response.status_code == 200:
    print("Response from server:") 
    print(response.json()) #Print Successful getting weather info from server
else:
    print("Error:", response.status_code) #Print error 
