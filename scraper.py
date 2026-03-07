import requests
from bs4 import BeautifulSoup
import json

def uzmi_podatke(url, klub_target):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        tables = soup.find_all('table')
        
        rezultati = []
        tabela = []
        
        for table in tables:
            rows = table.find_all('tr')
            # Tražimo rezultate gde su Gaučosi
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3 and (klub_target.lower() in row.text.lower()):
                    rezultati.append({
                        "domacin": cols[0].text.strip(),
                        "gost": cols[2].text.strip(),
                        "rezultat": cols[1].text.strip()
                    })
            
            # Tražimo tabelu gde su Gaučosi
            if klub_target in table.text:
                for row in rows[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        tabela.append({
                            "poz": cols[0].text.strip().replace('.', ''),
                            "klub": cols[1].text.strip(),
                            "bod": cols[-1].text.strip()
                        })
        return {"rezultati": rezultati, "tabela": tabela}
    except:
        return {"rezultati": [], "tabela": []}

def scrape():
    # Grupa B Petlići
    petlici = uzmi_podatke("https://fsmo.info/liga-petlica-b-fsmo/", "Gaučosi")
    # Fudbal 9 (Mlađi pioniri)
    fudbal9 = uzmi_podatke("https://fsmo.info/liga-mladih-pionira-fsmo/", "Gaučosi")

    with open('podaci.json', 'w', encoding='utf-8') as f:
        json.dump({
            "petlici": petlici,
            "fudbal9": fudbal9
        }, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape()
