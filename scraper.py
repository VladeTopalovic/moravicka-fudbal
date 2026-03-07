import requests
from bs4 import BeautifulSoup
import json

def scrape():
    # URL za Moravičku okružnu ligu petlića na Srbijasportu
    url = "https://www.srbijasport.net/league/7194"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rezultati = []
        tabela = []

        # 1. ČUPANJE REZULTATA (poslednje odigrano kolo)
        # Tražimo blok sa rezultatima
        matches = soup.select('.n_utakmica')
        for m in matches:
            timovi = m.select('.n_tim_naziv')
            rez = m.select_one('.n_rezultat')
            if len(timovi) >= 2 and rez:
                rezultati.append({
                    "domacin": timovi[0].text.strip(),
                    "gost": timovi[1].text.strip(),
                    "rezultat": rez.text.strip()
                })

        # 2. ČUPANJE TABELE
        # Tražimo tabelu na stranici
        rows = soup.select('.table-responsive table tr')
        for row in rows[1:]: # preskačemo zaglavlje
            cols = row.find_all('td')
            if len(cols) > 8:
                tabela.append({
                    "poz": cols[0].text.strip(),
                    "klub": cols[1].text.strip(),
                    "bod": cols[-1].text.strip()
                })

        # Ako scraper nije našao ništa (prazna lista), ubacićemo poruku
        if not rezultati:
            rezultati = [{"domacin": "Nema", "gost": "utakmica", "rezultat": "0:0"}]

        # Čuvanje u JSON
        with open('podaci.json', 'w', encoding='utf-8') as f:
            json.dump({"rezultati": rezultati, "tabela": tabela}, f, ensure_ascii=False, indent=4)
            
        print("Podaci uspešno osveženi!")
            
    except Exception as e:
        print(f"Greška pri skrapovanju: {e}")

if __name__ == "__main__":
    scrape()
