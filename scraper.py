import requests
from bs4 import BeautifulSoup
import json

def scrape():
    url = "https://fsmo.info/liga-petlica-b-fsmo/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rezultati = []
        tabela = []
        tables = soup.find_all('table')

        # TRAŽENJE REZULTATA GAUČOSA
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    text = row.text.lower()
                    # Ako se u redu pominju Gaučosi, uzmi taj rezultat
                    if "gauč" in text or "gauc" in text:
                        rezultati.append({
                            "domacin": cols[0].text.strip(),
                            "gost": cols[2].text.strip(),
                            "rezultat": cols[1].text.strip()
                        })

        # TRAŽENJE TABELE (tražimo onu gde su Gaučosi na listi)
        for table in tables:
            if "Gaučosi" in table.text or "Gaucosi" in table.text:
                rows = table.find_all('tr')
                for row in rows[1:]: # Preskoči naslov
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        tabela.append({
                            "poz": cols[0].text.strip().replace('.', ''),
                            "klub": cols[1].text.strip(),
                            "bod": cols[-1].text.strip()
                        })
                break # Kad nađe tabelu sa Gaučosima, stani

        # Ako nema trenutnih utakmica, stavi info
        if not rezultati:
            rezultati = [{"domacin": "Gaučosi", "gost": "Čekaju termin", "rezultat": "v"}]

        with open('podaci.json', 'w', encoding='utf-8') as f:
            json.dump({"rezultati": rezultati, "tabela": tabela}, f, ensure_ascii=False, indent=4)
            
        print("Podaci za Gaučose uspešno osveženi!")
            
    except Exception as e:
        print(f"Greška: {e}")

if __name__ == "__main__":
    scrape()
