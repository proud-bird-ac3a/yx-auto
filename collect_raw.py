import requests, re, os, ipaddress
from bs4 import BeautifulSoup

# ✅ URL源与简称 (完全保留)
sources = {
    'https://api.uouin.com/cloudflare.html': 'Uouin',
    'https://ip.164746.xyz': 'ZXW',
    'https://ipdb.api.030101.xyz/?type=bestcf': 'IPDB',
    'https://www.wetest.vip/page/cloudflare/address_v6.html': 'WeTestV6',
    'https://ipdb.api.030101.xyz/?type=bestcfv6': 'IPDBv6',
    'https://cf.090227.xyz/CloudFlareYes': 'CFYes',
    'https://ip.haogege.xyz': 'HaoGG',
    'https://vps789.com/openApi/cfIpApi': 'VPS',
    'https://www.wetest.vip/page/cloudflare/address_v4.html': 'WeTest',
    'https://addressesapi.090227.xyz/ct': 'CMLiuss',
    'https://addressesapi.090227.xyz/cmcc-ipv6': 'CMLiussv6',
    'https://raw.githubusercontent.com/xingpingcn/enhanced-FaaS-in-China/refs/heads/main/Cf.json': 'FaaS'
}

PORT = '443'  # 目标端口号

# 正则表达式
ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
ipv6_candidate_pattern = r'([a-fA-F0-9:]{2,39})'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

# 删除旧文件
for file in ['raw_ipv4.txt', 'raw_ipv6.txt']:
    if os.path.exists(file):
        os.remove(file)

# IP 分类存储
ipv4_set = set()
ipv6_set = set()

# 遍历来源
for url, shortname in sources.items():
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        content = response.text

        if url.endswith('.txt'):
            text = content
        else:
            soup = BeautifulSoup(content, 'html.parser')
            elements = soup.find_all('tr') or soup.find_all('li') or soup
            text = '\n'.join(el.get_text() for el in elements)

        # IPv4 提取 (只记IP)
        for ip in re.findall(ipv4_pattern, text):
            try:
                if ipaddress.ip_address(ip).version == 4:
                    ipv4_set.add(f"{ip}:{PORT}")
            except ValueError:
                continue

        # IPv6 提取 (只记IP)
        for ip in re.findall(ipv6_candidate_pattern, text):
            try:
                ip_obj = ipaddress.ip_address(ip)
                if ip_obj.version == 6:
                    ipv6_set.add(f"[{ip_obj.compressed}]:{PORT}")
            except ValueError:
                continue

    except requests.RequestException as e:
        print(f"[请求错误] {url} -> {e}")
    except Exception as e:
        print(f"[解析错误] {url} -> {e}")

# 写入原始 IP 文件 (只有IP，没有注释)
with open('raw_ipv4.txt', 'w') as f4:
    for ip in sorted(ipv4_set):
        f4.write(f"{ip}\n")

with open('raw_ipv6.txt', 'w') as f6:
    for ip in sorted(ipv6_set):
        f6.write(f"{ip}\n")

print(f"✅ 收集到 {len(ipv4_set)} 个 IPv4 地址")
print(f"✅ 收集到 {len(ipv6_set)} 个 IPv6 地址")
