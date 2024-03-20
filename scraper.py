import httpx
from bs4 import BeautifulSoup

def get_hero_info(hero_name):
    url = f"https://ru.dotabuff.com/heroes/{hero_name.replace(' ', '-').lower()}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    r = httpx.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')

    hero_name_element = soup.select_one('h1')

    if r.status_code == 404:
        return {"error": "Герой не найден. Проверьте корректность ввода имени героя."}
    
    hero_name = hero_name_element.get_text().strip()
    popular_lanes = []

    lanes_table = soup.find('div', class_='col-8').find('table')

    if lanes_table:
        rows = lanes_table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                lane_info = {
                    'lane_name': cols[0].get_text().strip(),
                    'presence': cols[1].get_text().strip().strip('%'),
                    'winrate': cols[2].get_text().strip().strip('%')
                }
                popular_lanes.append(lane_info)
    else:
        return {"error": "Table not found"}

    return {"hero_name": hero_name, "popular_lanes": popular_lanes}


def get_hero_counters(hero_name):
    url = f"https://ru.dotabuff.com/heroes/{hero_name.replace(' ', '-').lower()}/counters"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    r = httpx.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    counters = []

    rows = soup.select('table.sortable tbody tr[data-link-to]')

    for row in rows[:5]:
        cols = row.find_all('td')
        if len(cols) > 2:
            hero_name = cols[1].get_text().strip()
            hero_url = f"https://ru.dotabuff.com{cols[1].find('a')['href']}"
            win_rate = cols[3].get_text().strip('%').strip()
            counters.append({
                "hero_name": hero_name,
                "hero_url": hero_url,
                "win_rate": win_rate
            })
            
    if not counters:
        return {"error": "Герой не найден. Проверьте корректность ввода имени героя."}

    return {"counters": counters}



