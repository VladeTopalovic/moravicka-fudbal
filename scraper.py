import requests
from bs4 import BeautifulSoup
import json

def skeniraj_ligu(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    rezultati = []
    tabela = []
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # TABELA
        rows = soup.select('.table-responsive table tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 8:
                # Ime kluba je u drugom polju (index 1), obično unutar <a> taga
                klub_td = cols[1]
                link = klub_td.find('a')
                ime = link.text.strip() if link else klub_td.text.strip()
                
                tabela.append({
                    "poz": cols[0].text.strip(),
                    "klub": ime,
                    "bod": cols[-1].text.strip()
                })

        # REZULTATI (Tražimo Gaučose)
        matches = soup.select('.n_utakmica')
        for m in matches:
            if "gauč" in m.text.lower() or "gauc" in m.text.lower():
                timovi = m.select('.n_tim_naziv')
                rez = m.select_one('.n_rezultat')
                if len(timovi) >= 2 and rez:
                    rezultati.append({
                        "domacin": timovi[0].text.strip(),
                        "gost": timovi[1].text.strip(),
                        "rezultat": rez.text.strip()
                    })
    except Exception as e:
        print(f"Greška: {e}")
    return {"rezultati": rezultati, "tabela": tabela}

def scrape():
    # Linkovi za Petliće (7194) i Fudbal 9 (7193)
    petlici_data = skeniraj_ligu("https://www.srbijasport.net/league/7194")
    fudbal9_data = skeniraj_ligu("https://www.srbijasport.net/league/7193")

    with open('podaci.json', 'w', encoding='utf-8') as f:
        json.dump({
            "petlici": petlici_data,
            "fudbal9": fudbal9_data
        }, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape()
