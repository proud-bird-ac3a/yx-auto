import requests, os
from datetime import datetime, timedelta

def country_to_flag(code):
    if not code or len(code) != 2:
        return '🏳️'
    return chr(ord(code[0]) + 127397) + chr(ord(code[1]) + 127397)

def process(raw_file, output_file):
    if not os.path.exists(raw_file):
        print(f"{raw_file} not found, skipping.")
        return

    # 读取环境变量中的 API token
    token = os.environ.get('IPINFO_TOKEN', '')
    if not token:
        print("⚠️ 未设置 IPINFO_TOKEN 环境变量，将使用未认证模式（可能有严格限制）")

    with open(raw_file, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    results = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    # 构造带 token 的 URL：https://ipinfo.io/{ip}/json?token=YOUR_TOKEN
    base_url = 'https://ipinfo.io'

    for ip_with_port in ips:
        ip = ip_with_port.split(':')[0].strip('[]')
        try:
            url = f"{base_url}/{ip}/json"
            if token:
                url += f"?token={token}"
            r = requests.get(url, headers=headers, timeout=5)
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
    timestamp = beijing_time.strftime('%Y%m%d_%H:%M')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"ip.list.updated.at#Upd{timestamp}\n")
        for ip, comment in results:
            f.write(f"{ip}#{comment}\n")

    print(f"Written {len(results)} entries to {output_file}")

if __name__ == '__main__':
    process('raw_ipv4.txt', 'ipv4.txt')
    process('raw_ipv6.txt', 'ipv6.txt')
