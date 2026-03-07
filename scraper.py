import requests
from bs4 import BeautifulSoup
import json

def grab_data():
    url = "https://www.srbijasport.net/league/7194" # Link ka ligi petlića
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    # Logika za čitanje tabele i rezultata
    # ... (skripta prolazi kroz HTML i pravi listu) ...
    
    data = {
        "rezultati": [
            {"domacin": "Borac 1926", "gost": "BIP", "rezultat": "2:1"},
            {"domacin": "Ares", "gost": "Sloboda", "rezultat": "0:0"}
        ],
        "tabela": [
            {"pozicija": 1, "klub": "Borac 1926", "bodovi": 28},
            {"pozicija": 2, "klub": "BIP", "bodovi": 21}
        ]
    }

    with open('podaci.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

grab_data()