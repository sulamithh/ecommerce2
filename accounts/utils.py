import requests

def fetch_location(ip):
    if ip == "127.0.0.1" or ip == "::1":
        return {
            "status": "fail",
            "message": "reserved range",
            "query": ip
        }

    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()
    return data
