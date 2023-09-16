import requests

# URL và header của request


def send_request(username):
    payload = {
        "username": username,
        "password": "dungco2006",
        "server": "1",
        "accept": "on",
    }

    url = "https://ngocrongaz.online/dang-ky"
    headers = {
        "authority": "ngocrongaz.online",
        "method": "POST",
        "path": "/dang-ky",
        "scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Cache-Control": "max-age=0",
        "Content-Length": "48",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "PHPSESSID=mvgc6g6l7i36n0sudrp440ldit",
        "Origin": "https://ngocrongaz.online",
        "Referer": "https://ngocrongaz.online/dang-ky",
        "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.0.0",
    }
        # Thực hiện POST request
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        print(f'Success {i}')
    else:
        print(f'Error {i}')

import threading


# Tạo danh sách các luồng
threads = []

start_index = 1001
end_index = 10000

for i in range(start_index, end_index + 1):
    username = f"Kaioken{i}"
    thread = threading.Thread(target=send_request, args=(username,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Hoàn thành tất cả request")