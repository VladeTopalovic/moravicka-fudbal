import requests
from bs4 import BeautifulSoup
import json

def scrape():
    # Novi link za Moravičku ligu petlića (B grupa)
    url = "https://fsmo.info/liga-petlica-b-fsmo/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8' # Da bi se slova č, ć, š videla lepo
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rezultati = []
        tabela = []

        # 1. ČUPANJE REZULTATA (Tražimo tabelu sa rezultatima)
        # Na fsmo.info rezultati su obično u prvoj tabeli
        tables = soup.find_all('table')
        
        if len(tables) >= 1:
            # Tražimo rezultate (obično su u prvoj ili drugoj tabeli zavisno od kola)
            res_table = tables[0] 
            rows = res_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    domacin = cols[0].text.strip()
                    gost = cols[2].text.strip()
                    rez = cols[1].text.strip()
                    if domacin and gost:
                        rezultati.append({"domacin": domacin, "gost": gost, "rezultat": rez})

        # 2. ČUPANJE TABELE (Tražimo tabelu sa bodovima)
        # Obično je to poslednja tabela na stranici
        if len(tables) >= 2:
            tab_table = tables[-1] 
            rows = tab_table.find_all('tr')
            for row in rows[1:]: # preskačemo zaglavlje
                cols = row.find_all('td')
                if len(cols) >= 4:
                    tabela.append({
                        "poz": cols[0].text.strip().replace('.', ''),
                        "klub": cols[1].text.strip(),
                        "bod": cols[-1].text.strip()
                    })

        # Čuvanje u JSON
        with open('podaci.json', 'w', encoding='utf-8') as f:
            json.dump({"rezultati": rezultati, "tabela": tabela}, f, ensure_ascii=False, indent=4)
            
        print("Podaci uspešno povučeni sa fsmo.info!")
            
    except Exception as e:
        print(f"Greška: {e}")

if __name__ == "__main__":
    scrape()
