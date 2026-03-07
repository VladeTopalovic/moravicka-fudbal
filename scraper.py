import requests
from bs4 import BeautifulSoup
import json

def skeniraj_srbijasport(url, naziv_lige):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    rezultati = []
    tabela = []
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        # 1. ČUPANJE REZULTATA (Tražimo redove gde su Gaučosi)
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

        # 2. ČUPANJE TABELE
        rows = soup.select('.table-responsive table tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) > 8:
                tabela.append({
                    "poz": cols[0].text.strip(),
                    "klub": cols[1].text.strip(),
                    "bod": cols[-1].text.strip()
                })
    except Exception as e:
        print(f"Greška na {naziv_lige}: {e}")
    
    return {"rezultati": rezultati, "tabela": tabela}

def scrape():
    # Linkovi ka SrbijaSportu (Proveri da li su ovo tačni linkovi za tvoje lige)
    # Petlići Moravička okružna: https://www.srbijasport.net/league/7194
    # Fudbal 9 (Pioniri): https://www.srbijasport.net/league/7193 (Primer)
    
    podaci_petlici = skeniraj_srbijasport("https://www.srbijasport.net/league/7194", "Petlici")
    podaci_fudbal9 = skeniraj_srbijasport("https://www.srbijasport.net/league/7193", "Fudbal 9")

    finalni_json = {
        "petlici": podaci_petlici,
        "fudbal9": podaci_fudbal9
    }

    with open('podaci.json', 'w', encoding='utf-8') as f:
        json.dump(finalni_json, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape()
