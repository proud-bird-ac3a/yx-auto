import requests, os
from datetime import datetime, timedelta

def country_to_flag(code):
    if not code or len(code) != 2:
        return '🏳️'
    return chr(ord(code[0]) + 127397) + chr(ord(code[1]) + 127397)

def process(raw_file, output_file, limit=10):
    if not os.path.exists(raw_file):
        print(f"{raw_file} not found, skipping.")
        return

    with open(raw_file, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for ip_with_port in ips:
        ip = ip_with_port.split(':')[0].strip('[]')
        try:
            r = requests.get(f"https://ipinfo.io/{ip}/json", headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                country = data.get('country', '')
                city = data.get('city', '')
                if city:
                    comment = f"{country_to_flag(country)} {city}"
                else:
                    comment = country_to_flag(country)
            else:
                comment = country_to_flag('')
        except Exception:
            comment = country_to_flag('')
        results.append((ip_with_port, comment))

    beijing_time = datetime.utcnow() + timedelta(hours=8)
    timestamp_full = beijing_time.strftime('%Y-%m-%d %H:%M:%S')

    top = results[:limit]

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"ipTop10.list.updated.at#Upd{timestamp_full}\n")
        for ip, comment in top:
            f.write(f"{ip}#{comment}\n")

    print(f"Written {len(top)} entries to {output_file}")

if __name__ == '__main__':
    process('raw_ipv4.txt', 'ipv4.txt')
    process('raw_ipv6.txt', 'ipv6.txt')